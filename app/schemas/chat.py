from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class RecommendedPlace(BaseModel):
    name: str
    id: str
    district: str

class ChatResponse(BaseModel):
    reply: str
    recommendedPlaces: list[RecommendedPlace] = []