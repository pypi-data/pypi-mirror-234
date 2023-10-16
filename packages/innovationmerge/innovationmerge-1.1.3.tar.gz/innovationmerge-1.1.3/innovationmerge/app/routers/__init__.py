import os
from fastapi.staticfiles import StaticFiles
from innovationmerge.app.routers import sample_route, authenticate
from innovationmerge.docs.api_doc import test_api_doc


def router_init(app):
    # Static Path
    static_data_dir = os.path.join("innovationmerge", "data")
    app.mount("/static", StaticFiles(directory=static_data_dir), name="static")


    # Testing route
    @app.get("/", responses=test_api_doc)
    def test_api():
        return {"Status": "Working"}

    # API routers
    app.include_router(authenticate.router, tags=["Security"])
    app.include_router(sample_route.router, tags=["Sample"], prefix="/v1")