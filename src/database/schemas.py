from pydantic import BaseModel, Field


class VideoRecord(BaseModel):
    """Schema for storing video records in the database."""

    video_id: str = Field(..., description="Unique identifier for the video")
    title: str = Field(..., description="Title of the video")
    description: str = Field(...,
                             description="Description of the video content")
    published_at: str = Field(...,
                              description="Timestamp when the video was published")
    channel_id: str = Field(...,
                            description="Identifier of the channel that uploaded the video")
    channel_title: str = Field(...,
                               description="Title of the channel that uploaded the video")
    thumbnail_url: str | None = Field(None,
                                      description="URL of the video's thumbnail image")
    view_count: int = Field(
        0, description="Number of views the video has received")
    like_count: int = Field(
        0, description="Number of likes the video has received")
    comment_count: int = Field(
        0, description="Number of comments on the video")
    duration_seconds: int = Field(
        0, description="Duration of the video in seconds")
    tags: list[str] = Field(default_factory=list,
                            description="List of tags associated with the video")
    category_id: str = Field(
        "", description="Category identifier of the video")
    live_broadcast_content: str = Field("none",
                                        description="Live broadcast content status")
    privacy_status: str = Field(
        "public", description="Privacy status of the video")
    notification_received_at: str = Field(...,
                                          description="Timestamp when notification was received")
    last_updated_at: str = Field(...,
                                 description="Timestamp when the record was last updated")
    created_at: str = Field(...,
                            description="Timestamp when the record was created")


class DatabaseResponse(BaseModel):
    """Schema for database operation responses."""

    status: str = Field(..., description="Status of the database operation")
    details: str | None = Field(
        None, description="Additional details about the operation")
