from fastapi import APIRouter

from app.api.routes import chat, lookups, places, posts

api_router = APIRouter()
api_router.include_router(lookups.router, tags=["lookups"])
api_router.include_router(places.router, prefix="/places", tags=["places"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
