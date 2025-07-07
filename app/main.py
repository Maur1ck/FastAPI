from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.api.hotels import router as router_hotels
from app.api.auth import router as router_auth
from app.api.rooms import router as router_rooms
from app.api.bookings import router as router_bookings
from app.api.facilities import router as router_facilities

app = FastAPI()
app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)