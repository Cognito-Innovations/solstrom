from app.agent.project import ProjectAgent

class AgentService:
    def __init__(self):
        self.agent = ProjectAgent()

    async def conversation(self, user_message: str):
        """Store checkout product data via handler."""
        return await self.agent.process(user_message)