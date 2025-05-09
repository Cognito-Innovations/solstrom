import os
from dotenv import load_dotenv

load_dotenv()

#QDRANT
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_API_URL = os.getenv("QDRANT_API_URL")

#CLUADE
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")