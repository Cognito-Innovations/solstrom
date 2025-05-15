import json
import httpx
import regex
from typing import TypeVar, Type, Optional
from pydantic import BaseModel

from app.config import CLAUDE_API_KEY
from app.constants import CLAUDE_API_URL, CLAUDE_MODEL_NAME

T = TypeVar('T', bound=BaseModel)

class ClaudeAIClient:
    """Client for generating structured responses using Pydantic models"""
    
    @staticmethod
    async def generate(
        model_class: Type[T],
        user_message: str,
        system_message: Optional[str] = None,
        temperature: float = 0.3,
        top_p: float = 1.0,
        max_tokens: int = 1000
    ) -> T:
        try:
            headers = {
                "x-api-key": CLAUDE_API_KEY,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            }

            enhanced_message = (
                f"{user_message}\n\n"
                f"IMPORTANT: Respond with valid JSON that matches this schema:\n"
                f"{model_class.model_json_schema()}\n"
                f"Your entire response must be valid JSON only, no other text."
            )

            payload = {
                "model": CLAUDE_MODEL_NAME,
                "system": system_message,
                "messages": [{"role": "user", "content": enhanced_message}],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p
            }
        
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    CLAUDE_API_URL,
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )

                response.raise_for_status()
                json_response = response.json()
                
                content = json_response.get("content", [{}])[0].get("text", "")
                
                try:
                    json_content = json.loads(content)
                except json.JSONDecodeError:
                    json_content = json.loads(ClaudeAIClient._extract_json(content))

                if not isinstance(json_content.get('response'), list):
                    json_content['response'] = ["• Invalid response format received"]
                json_content.setdefault('is_greeting', False)
                json_content.setdefault('exists_in_data', False)
                json_content.setdefault('exists_elsewhere', False)
                json_content.setdefault('relevant_projects', [])
                json_content.setdefault('sources', [])
                
                return model_class.model_validate(json_content)
                
        except httpx.HTTPStatusError as e:
            print(f"API error: {e.response.text}")
            raise ValueError(f"API request failed: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return model_class(
                response=["• Error processing your request"],
                is_greeting=False,
                exists_in_data=False,
                exists_elsewhere=False,
                relevant_projects=[],
                sources=[]
            )

    @staticmethod
    def _extract_json(text: str) -> str:
        """Extract JSON string from API response"""
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        json_match = regex.search(r'\{(?:[^{}]|(?R))*\}', text, regex.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON found in response")
        return json_match.group(0)