from app.custom_fastapi import CustmFastAPI

def init_services(app: CustmFastAPI):
    """Initialize services in the app state."""
    from app.services.embeddings_service import EmbeddingService
    from app.services.agent_service import AgentService

    app.embeddings_service = EmbeddingService()
    app.agent_service = AgentService()