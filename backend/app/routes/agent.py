from fastapi import APIRouter

api_url_router = APIRouter(prefix="/api-url", tags=["api_url_router"])

@api_url_router.get("/get")
async def get_api_url():
    app = get_app()
    api_url = await app.api_url_service.get_api_url()
    return {"success": True, "api_url": api_url}