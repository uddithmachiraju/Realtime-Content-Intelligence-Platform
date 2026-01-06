"""A separate API for handling webhooks."""

import feedparser
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse

from src.config.logging import get_logger, setup_logging
from src.config.settings import get_settings

setup_logging()
logger = get_logger("webhook")
settings = get_settings()


app = FastAPI(
    title="Webhook API", description="API for handling incoming webhooks.", version="0.0.1"
)


# /webhook?hub.mode=subscribe&hub.challenge=test123 HTTP/1.1
@app.get("/webhook", tags=["Webhook"], response_class=PlainTextResponse)
async def verify_subscription(request: Request) -> str:
    """Endpoint to verify webhook subscription."""

    params = request.query_params
    mode = params.get("hub.mode")
    topic = params.get("hub.topic")
    challenge = params.get("hub.challenge")

    logger.debug("Received webhook verification request.")

    if topic and not topic.startswith("https://www.youtube.com/xml/feeds/videos.xml"):
        logger.error("Invalid topic parameter in verification request.")
        raise HTTPException(status_code=400, detail="Invalid topic parameter.")

    if mode == "subscribe":
        if not challenge:
            logger.error(
                "Missing challenge parameter in verification request.")
            raise HTTPException(
                status_code=400, detail="Missing challenge parameter.")
        logger.info("Webhook subscription verified.")
        return challenge
    elif mode == "unsubscribe":
        logger.info("Webhook unsubscription verified.")
        return PlainTextResponse("Unsubscribed successfully.")

    else:
        logger.warning("Webhook subscription verification failed.")
        raise HTTPException(status_code=403, detail="Verification failed.")


@app.post("/webhook", tags=["Webhook"], response_class=PlainTextResponse)
async def receive_notification(request: Request) -> str:
    """Endpoint to receive webhook notifications."""

    try:
        body = await request.body()
        logger.info("Received webhook notification.", body=body.decode())

        feed = feedparser.parse(body)

        for entry in feed.entries:
            video_id = entry.yt_videoid
            channel_id = entry.yt_channelid
            published = entry.published

            if not video_id:
                logger.error(
                    "Missing video ID in webhook notification.")
                continue

            logger.info("New video notification received.")

            message = {
                "video_id": video_id,
                "channel_id": channel_id,
                "published": published,
            }

    except Exception as e:
        logger.exception(
            "Error processing webhook notification.", error=str(e))
        raise HTTPException(
            status_code=500, detail="Internal server error.") from e


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """Health check endpoint."""

    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "src.webhook.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )
