import json
from pathlib import Path
from typing import Dict, Any

from app.services.embeddings_service import EmbeddingService
from app.external_services.claude_ai_client import ClaudeAIClient
from app.models.api.agent_router import ProjectResponse
from app.utils.projects_utils import format_context_texts

class ProjectAgent:
    """Handles project-related queries using embeddings and vector DB matching"""
    def __init__(self):
        prompt_path = Path(__file__).parent / "prompt" / "project_prompt.json"
        with open(prompt_path) as f:
            self.prompt_config = json.load(f)['project_agent_prompt']
    
    async def process(self, user_message: str) -> Dict[str, Any]:
        try:
            user_message_embeddings = EmbeddingService.create_embeddings(user_message)
            
            query_response = await EmbeddingService.get_embeddings(
                vector=user_message_embeddings
            )
            
            if query_response and isinstance(query_response[0], dict):
                context_texts = [
                    item['metadata']['text']
                    for item in query_response
                    if 'metadata' in item and 'text' in item['metadata']
                ]
            else:
                context_texts = format_context_texts(query_response)
            
            system_message = self.prompt_config['base_system_message']
            formatted_user_message = self.prompt_config['user_message_template'].format(
                user_message=user_message,
                context="\n".join(context_texts[:3]) # Limit to top 3 most relevant chunks
            )
            
            result = await ClaudeAIClient.generate(
                model_class=ProjectResponse,
                user_message=formatted_user_message,
                system_message=system_message,
                temperature=self.prompt_config['parameters']['temperature'],
                max_tokens=self.prompt_config['parameters']['max_tokens']
            )
            print(f"Result: {result}")
            
            return {
                "response": result.response,
                "confidence_score": result.confidence_score,
                "relevant_projects": result.relevant_projects
            }

        except Exception as e:
            print(f"Processing error: {str(e)}")
            return {
                "response": self.prompt_config['response_structure']['fallback_response'],
                "confidence_score": 0.0,
                "relevant_projects": []
            }