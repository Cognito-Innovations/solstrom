from app.custom_fastapi import CustmFastAPI

from app.dbhandlers.embeddings_handler import EmbeddingsHandler


def init_handlers(app: 'CustmFastAPI'):
    """Initialize handlers in the app state."""
    app.embeddings_handler = EmbeddingsHandler()
    