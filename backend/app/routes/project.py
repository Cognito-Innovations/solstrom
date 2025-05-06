from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import asyncio

from app.utils.projects_utils import process_text_file
from app.utils.app_utils import get_app

projects_router = APIRouter(prefix="/projects", tags=["projects"])

@projects_router.post(
    "/create",
    summary="Store project embeddings in Vector DB",
    responses={
        200: {"description": "Embeddings stored successfully"},
        400: {"description": "Invalid input data"},
        500: {"description": "Internal server error"},
    },
)
async def create(
    file: UploadFile = File(...),
    custom_metadata: Optional[Dict[str, Any]] = None,
    background_tasks: BackgroundTasks = None
):
    try:
        if not file.filename.endswith('.txt'):
            raise HTTPException(
                status_code=400,
                detail="Only .txt files are accepted"
            )
        
        app = get_app()

        content = await file.read()
        text = content.decode('utf-8')

        if background_tasks:
            background_tasks.add_task(
                process_and_store_embeddings,
                app,
                text,
                file.filename,
                custom_metadata
            )
            return JSONResponse(
                content={"status": "processing_started"},
                status_code=202
            )

        try:
            result = await asyncio.wait_for(
                process_and_store_embeddings(app, text, file.filename, custom_metadata),
                timeout=300  # 5 minute timeout
            )
            return JSONResponse(content=result, status_code=200)
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=504,
                detail="Processing timed out"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
    

async def process_and_store_embeddings(app, text, filename, custom_metadata):
    """Encapsulated processing logic"""
    documents = await process_text_file(text, filename)
    return await app.projects_service.create(documents, custom_metadata)