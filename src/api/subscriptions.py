"""API endpoints for managing YouTube WebSub subscriptions."""

from fastapi import APIRouter

from src.config.logging import get_logger
from src.webhook.manager import WebSubManager

logger = get_logger("subscription_api")
router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post("/subscribe/{channel_id}")
async def subscribe_to_channel(channel_id: str) -> dict:
    """Subscribe to a YouTube channel's updates."""

    manager = WebSubManager()
    try:
        result = await manager.subscribe(channel_id)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Subscription failed for {channel_id}")
        return {"success": False, "message": str(e)}


@router.post("/unsubscribe/{channel_id}")
async def unsubscribe_from_channel(channel_id: str) -> dict:
    """Unsubscribe from a YouTube channel's updates."""

    manager = WebSubManager()
    try:
        result = await manager.unsubscribe(channel_id)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error("Unsubscription failed",
                     channel_id=channel_id, error=str(e))
        return {"success": False, "message": str(e)}
