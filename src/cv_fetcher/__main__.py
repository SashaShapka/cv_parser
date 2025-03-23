import uvicorn

from cv_fetcher.config import SETTINGS


if __name__ == "__main__":
    uvicorn.run(
        "cv_fetcher.app:app",
        host=SETTINGS.server_host,
        port=SETTINGS.server_port,
        reload=True
    )


