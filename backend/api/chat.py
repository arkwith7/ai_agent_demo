from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from core.agent import LangChainAgent
from security import get_current_user

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class RecommendationResponse(BaseModel):
    recommendations: List[str]

@router.post("/chat", response_model=RecommendationResponse)
async def chat(query: QueryRequest, current_user: str = Depends(get_current_user)):
    try:
        agent = LangChainAgent()
        recommendations = await agent.process_query(query.question)
        return RecommendationResponse(recommendations=recommendations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))