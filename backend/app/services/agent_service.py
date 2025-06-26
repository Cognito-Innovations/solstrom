from app.agent.project import ProjectAgent
from app.external_services.db import DB

class AgentService:
    def __init__(self):
        self.agent = ProjectAgent()

    async def conversation(self, user_message: str, db):
        """Store checkout product data via handler."""
        response = await self.agent.process(user_message)
        await db.track_message({**response, 'user_message': user_message})
        return response