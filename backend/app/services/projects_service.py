from concurrent.futures import ThreadPoolExecutor
from fastapi import HTTPException
from typing import Dict, Any, List, Optional
import asyncio

from app.dbhandlers.embeddings_handler import EmbeddingsHandler
from app.utils.projects_utils import embedding_consumer, process_batch

class ProjectsService:  
    def __init__(self):
        self.embeddings_handler = EmbeddingsHandler()
        self.executor = ThreadPoolExecutor(max_workers=8)
        self.embedding_queue = asyncio.Queue(maxsize=100)
        self.stop_event = asyncio.Event()

    async def create(
        self,
        documents: List[Dict],
        custom_metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Generate and store embeddings for text chunks"""
        try:
            if not documents or not isinstance(documents, list):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid documents format - expected list"
                )

            total_docs = len(documents)
            stats = {
                'chunks_processed': 0,
                'embeddings_generated': 0,
                'stored_embeddings': 0,
                'failed_embeddings': 0,
                'failed_storage': 0
            }

            consumers = [
                asyncio.create_task(
                    embedding_consumer(
                        custom_metadata, 
                        stats,
                        self.embedding_queue,
                        self.stop_event,
                        self.executor,
                        self.embeddings_handler
                    )
                )
                for _ in range(4)
            ]

            batch_size = 50
            for i in range(0, total_docs, batch_size):
                batch = documents[i:i + batch_size]
                await process_batch(
                    batch, 
                    stats, 
                    self.embedding_queue
                )
                
            self.stop_event.set()
            await asyncio.gather(*consumers)

            return {
                "status": "success",
                "stats": stats,
                "message": f"Processed {stats['embeddings_generated']}/{total_docs} embeddings, stored {stats['stored_embeddings']}"
            }
        except HTTPException:
            raise 
        except Exception as error:
            print(f"Critical error in project creation: {error}")
            raise HTTPException(
                status_code=500,
                detail=f"Project processing failed: {str(error)}"
            )