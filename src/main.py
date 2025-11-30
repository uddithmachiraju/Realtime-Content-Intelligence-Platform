import uvicorn

from src.api.app import app
from src.config.settings import get_settings

settings = get_settings()

if __name__ == "__main__":
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
