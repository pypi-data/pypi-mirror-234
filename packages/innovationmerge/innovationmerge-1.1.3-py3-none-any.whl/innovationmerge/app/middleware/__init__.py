from fastapi.middleware.cors import CORSMiddleware
from fastapi import Response
import uuid
import time

# Custom imports
from innovationmerge.app.logger import logger


def middleware_init(app):
    # Cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_request(request, call_next):
        start_time = time.time()
        request_id = str(uuid.uuid4().hex)
        logger.info(
            f"{request_id} {request.client.host} \
            {request.method} {request.url}"
        )
        response = await call_next(request)
        if response.status_code != 200:
            logger.error(f"{request_id} {response.status_code}")
        else:
            logger.info(f"{request_id} {response.status_code}")
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        process_time = (time.time() - start_time) * 1000
        response.headers["X-Process-Time-ms"] = str(process_time)
        return Response(
            content=body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
