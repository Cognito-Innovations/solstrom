from fastapi import FastAPI

class CustmFastAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        from app.services.embeddings_service import EmbeddingService
        from app.services.agent_service import AgentService
        from app.services.projects_service import ProjectsService
        
        from app.dbhandlers.embeddings_handler import EmbeddingsHandler

        self.embeddings_service = EmbeddingService()
        self.agent_service = AgentService()
        self.projects_service = ProjectsService()
        self.embeddings_handler = EmbeddingsHandler()
