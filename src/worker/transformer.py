import re
from datetime import datetime


class VideoTransformer:
    """Transforms raw video data into structured format."""

    @staticmethod
    def transform(video_data: dict) -> dict:
        """Transform raw video data into structured format."""
        snippet = video_data.get("snippet", {})
        statistics = video_data.get("statistics", {})
        content_details = video_data.get("contentDetails", {})

        return {
            "video_id": video_data.get("id"),
            "title": VideoTransformer._clean_text(snippet.get("title", "")),
            "description": VideoTransformer._clean_text(snippet.get("description", "")),
            "published_at": VideoTransformer._parse_datetime(snippet.get("publishedAt", "")),
            "channel_id": snippet.get("channelId"),
            "channel_title": VideoTransformer._clean_text(snippet.get("channelTitle", "")),
            "thumbnail_url": VideoTransformer._get_thumbnail(snippet),
            "view_count": int(statistics.get("viewCount", 0)),
            "like_count": int(statistics.get("likeCount", 0)),
            "comment_count": int(statistics.get("commentCount", 0)),
            "duration_seconds": VideoTransformer._parse_duration(
                content_details.get("duration", "")
            ),
            "tags": snippet.get("tags", [])[:50],  # Limit to first 50 tags
            "category_id": snippet.get("categoryId", ""),
            "live_broadcast_content": snippet.get("liveBroadcastContent", "none"),
            "privacy_status": video_data.get("status", {}).get("privacyStatus", "public"),
            "notification_received_at": datetime.utcnow(),
            "last_updated_at": datetime.utcnow(),
            "created_at": datetime.utcnow(),
        }

    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean text by removing unwanted characters."""

        text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @staticmethod
    def _parse_duration(duration: str) -> int:
        """Parse ISO 8601 duration to seconds."""
        match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
        if not match:
            return 0
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        return hours * 3600 + minutes * 60 + seconds

    @staticmethod
    def _get_thumbnail(snippet: dict) -> str | None:
        """Get the highest resolution thumbnail URL available."""
        thumbnails = snippet.get("thumbnails", {})
        for quality in ["maxres", "standard", "high", "medium", "default"]:
            if quality in thumbnails:
                return thumbnails[quality].get("url")
        return None

    @staticmethod
    def _parse_datetime(datetime_str: str) -> datetime:
        """Parse ISO 8601 datetime string to datetime object."""

        try:
            return datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
        except ValueError:
            return datetime.utcnow()
