import json
from pathlib import Path
from typing import Dict, Any

from app.services.embeddings_service import EmbeddingService
from app.external_services.claude_ai_client import ClaudeAIClient
from app.models.api.agent_router import ProjectResponse
from app.utils.projects_utils import format_context_texts, extract_source_info

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
            
            available_sources = set()
            if query_response and isinstance(query_response[0], dict):
                context_texts = []
                for item in query_response:
                    if 'metadata' in item:
                        item = extract_source_info(item)

                        text = item['metadata'].get('text', '')
                        context_texts.append(text)

                        if 'source_name' in item['metadata'] and 'source_url' in item['metadata']:
                            source = {
                                'source_name': item['metadata']['source_name'],
                                'source_url': item['metadata']['source_url']
                            }
                            available_sources.add(json.dumps(source, sort_keys=True))
            else:
                context_texts = format_context_texts(query_response)

            available_sources = [json.loads(s) for s in available_sources]
            
            system_message = self.prompt_config['base_system_message']
            formatted_user_message = self.prompt_config['user_message_template'].format(
                user_message=user_message,
                context="\n".join(context_texts),
                available_sources=json.dumps(available_sources)
            )
            
            result = await ClaudeAIClient.generate(
                model_class=ProjectResponse,
                user_message=formatted_user_message,
                system_message=system_message,
                temperature=self.prompt_config['parameters']['temperature'],
                max_tokens=self.prompt_config['parameters']['max_tokens']
            )

            valid_sources = []
            if result.sources:
                available_source_keys = {json.dumps(s, sort_keys=True) for s in available_sources}
                for source in result.sources:
                    source_key = json.dumps(source.dict(), sort_keys=True)
                    if source_key in available_source_keys:
                        valid_sources.append(source.dict())
            
            return {
                "response": result.response,
                "confidence_score": result.confidence_score,
                "relevant_projects": result.relevant_projects,
                "suggested_actions": result.suggested_actions,
                "sources": valid_sources
            }

        except Exception as e:
            print(f"Processing error: {str(e)}")
            return {
                "response": self.prompt_config['response_structure']['fallback_response'],
                "confidence_score": 0.0,
                "relevant_projects": [],
                "sources": [] 
            }