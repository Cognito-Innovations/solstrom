import httpx
import json
from datetime import datetime, UTC
from app.config import FIREBASE_DB_API

HEADERS =  {
    'Content-Type': 'application/json',
}

class DB:
    
    async def track_message(self, response):
        json_str = json.dumps(response, default=str)
        timestamp = datetime.now(UTC).strftime("%d-%b-%Y-%H-%M-%S")
        url = f"{FIREBASE_DB_API}/solstrom/{timestamp}.json"
        async with httpx.AsyncClient() as client:
            response = await client.put(url, headers=HEADERS, json=json_str)
        return {"status": response.status_code, "data": response.json()}
