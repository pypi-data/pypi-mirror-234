from fastapi import FastAPI

# Custom imports
from innovationmerge.app.logger import log_init, logger
from innovationmerge.app.routers import router_init
from innovationmerge.config import configs
from innovationmerge.app.middleware import middleware_init


def conf_init(app):
    logger.info(msg=f"Starting app with {configs.ENVIRONMENT} environment")


async def start_event():
    logger.info("API Started")


async def shutdown_event():
    logger.info("API Stopped")


def create_app():
    # Create API 
    app = FastAPI(
        title="innovationmerge API's",
        description="innovationmerge core components",
        version="1.0",
        on_startup=[start_event],
        on_shutdown=[shutdown_event],
    )

    # Enable Logging
    log_init()

    # Load configuration
    conf_init(app)

    # Initialize the middleware
    middleware_init(app)

    # Initialize routing configuration
    router_init(app)

    return app
