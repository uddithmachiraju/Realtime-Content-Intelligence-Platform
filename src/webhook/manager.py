import httpx

from src.config.logging import LoggerMixin
from src.config.settings import get_settings


class WebSubManager(LoggerMixin):
    """Manages WebSub subscriptions and notifications."""

    YOUTUBE_HUB_URL = "https://pubsubhubbub.appspot.com/"
    YOUTUBE_TOPIC = "https://www.youtube.com/xml/feeds/videos.xml?channel_id={channel_id}"
    LEASE_SECONDS = 432000  # 5 days

    def __init__(self):
        self.settings = get_settings()

    def get_callback_url(self) -> str:
        """Construct the callback URL for webhook notifications."""

        protocol = "https" if self.settings.webhook_domain != "localhost" else "http"
        return f"{protocol}://{self.settings.webhook_domain}/webhook"

    async def subscribe(self, channel_id: str) -> dict:
        """Subscribe to a YouTube channel's WebSub feed."""

        topic_url = self.YOUTUBE_TOPIC.format(channel_id=channel_id)
        callback_url = self.get_callback_url()

        data = {
            "hub.mode": "subscribe",
            "hub.topic": topic_url,
            "hub.callback": callback_url,
            "hub.lease_seconds": str(self.LEASE_SECONDS),
            "hub.secret": self.settings.websub_secret,
        }

        self.logger.info("Subscribing to channel.", channel_id=channel_id,
                         topic_url=topic_url, callback_url=callback_url)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.YOUTUBE_HUB_URL, data=data, timeout=10.0)
            response.raise_for_status()
            if response.status_code in (202, 204):
                self.logger.info(
                    "Subscription request accepted.", channel_id=channel_id)
                return {
                    "status": "subscribed",
                    "channel_id": channel_id,
                    "response_code": response.status_code,
                    "response_text": response.text,
                    "expires_at": (httpx.Timestamp.now() + self.LEASE_SECONDS).isoformat()
                }
            else:
                self.logger.warning(
                    "Unexpected response from hub.", channel_id=channel_id,
                    status_code=response.status_code, response_text=response.text)
                return {"status": "error", "channel_id": channel_id, "response_code": response.status_code, "response_text": response.text}
        except httpx.HTTPError as e:
            self.logger.error(
                "HTTP error during subscription.", channel_id=channel_id, error=str(e))
            return {"status": "error", "channel_id": channel_id, "error": str(e)}

    async def unsubscribe(self, channel_id: str) -> dict:
        """Unsubscribe from a YouTube channel's WebSub feed."""

        topic_url = self.YOUTUBE_TOPIC.format(channel_id=channel_id)
        callback_url = self.get_callback_url()

        data = {
            "hub.mode": "unsubscribe",
            "hub.topic": topic_url,
            "hub.callback": callback_url,
            "hub.secret": self.settings.websub_secret,
        }

        self.logger.info("Unsubscribing from channel.", channel_id=channel_id,
                         topic_url=topic_url, callback_url=callback_url)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.YOUTUBE_HUB_URL, data=data, timeout=10.0)
            response.raise_for_status()
            if response.status_code in (202, 204):
                self.logger.info(
                    "Unsubscription request accepted.", channel_id=channel_id)
                return {"status": "unsubscribed", "channel_id": channel_id, "response_code": response.status_code, "response_text": response.text}
            else:
                self.logger.warning(
                    "Unexpected response from hub.", channel_id=channel_id,
                    status_code=response.status_code, response_text=response.text)
                return {"status": "error", "channel_id": channel_id, "response_code": response.status_code, "response_text": response.text}
        except httpx.HTTPError as e:
            self.logger.error(
                "HTTP error during unsubscription.", channel_id=channel_id, error=str(e))
            return {"status": "error", "channel_id": channel_id, "error": str(e)}
