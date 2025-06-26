import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app import create_app

app = create_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

port = int(os.getenv("PORT"))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)