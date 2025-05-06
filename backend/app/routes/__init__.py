from app.custom_fastapi import CustmFastAPI

from app.routes.agent import agent_router
from app.routes.project import projects_router

def init_routes(app: CustmFastAPI):
    app.include_router(agent_router)
    app.include_router(projects_router)