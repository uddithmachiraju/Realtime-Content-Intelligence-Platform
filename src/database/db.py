from collections.abc import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.config.logging import LoggerMixin
from src.config.settings import get_settings
from src.database.schemas import DatabaseResponse, VideoRecord

get_settings()


class MongoDB(LoggerMixin):
    _client: AsyncIOMotorClient | None = None
    _database: AsyncIOMotorDatabase | None = None

    @property
    def videos(self) -> AsyncIOMotorDatabase:
        """Get the 'videos' collection from the MongoDB database."""

        if self._database is None:
            raise ValueError("Database connection is not established.")
        return self._database.videos

    @property
    def db(self) -> AsyncIOMotorDatabase:
        """Get the MongoDB database instance."""

        if self._database is None:
            raise ValueError("Database connection is not established.")
        return self._database

    def __init__(self) -> None:
        """Initialize the MongoDB client and database."""

        self.settings = get_settings()
        self.uri = self.settings.mongodb_uri
        self.db_name = self.settings.mongodb_db_name

    async def connect(self) -> None:
        """Establish a connection to the MongoDB database."""

        try:
            self._client = AsyncIOMotorClient(
                self.uri,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=50,
                minPoolSize=10,
            )

            self._database = self._client[self.db_name]

            # Test the connection
            await self._client.admin.command("ping")
            self.logger.info("Successfully connected to MongoDB")

        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise e

    async def close(self) -> None:
        """Close the connection to the MongoDB database."""

        if self._client:
            self._client.close()
            self.logger.info("MongoDB connection closed")

    async def upsert_video_data(self, video_data: VideoRecord) -> None:
        """Upsert video data into the MongoDB collection."""

        if self._database is None:
            raise ValueError("Database connection is not established.")

        try:
            videos_collection = self._database.videos
            filter_query = {"video_id": video_data.video_id}
            update_query = {"$set": video_data.model_dump()}

            await videos_collection.update_one(
                filter_query,
                update_query,
                upsert=True,
            )
        except Exception as e:
            self.logger.error(f"Error upserting video data: {e}")
            raise e

    async def is_healthy(self) -> DatabaseResponse:
        """Check if the MongoDB connection is healthy."""

        try:
            await self._client.admin.command("ping")
            return DatabaseResponse(
                status="healthy",
                details=None,
            )
        except Exception as e:
            self.logger.error(f"MongoDB health check failed: {e}")
            return DatabaseResponse(
                status="unhealthy",
                details=str(e),
            )


async def get_database() -> AsyncGenerator[MongoDB, None]:
    """Get a MongoDB database instance."""

    db = MongoDB()
    await db.connect()
    try:
        yield db
    finally:
        await db.close()
