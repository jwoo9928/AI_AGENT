"""
AI Agent Models and Data Structures
"""
from enum import Enum
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ActionType(str, Enum):
    """액션 타입 정의"""
    REALTIME_API = "realtime_api"
    WEB_SEARCH = "web_search"
    HYBRID = "hybrid"  # 여러 액션이 필요한 경우


class QueryRequest(BaseModel):
    """사용자 쿼리 요청 모델"""
    query: str
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class EnhancedQuery(BaseModel):
    """Gemini로 증강된 쿼리"""
    original_query: str
    enhanced_query: str
    keywords: List[str]
    intent: str
    complexity_score: float


class ActionDecision(BaseModel):
    """액션 결정 결과"""
    action_type: ActionType
    confidence: float
    reasoning: str
    parameters: Dict[str, Any]


class SearchResult(BaseModel):
    """검색 결과"""
    source: str
    content: str
    relevance_score: float
    metadata: Dict[str, Any]


class AgentResponse(BaseModel):
    """최종 에이전트 응답"""
    query: str
    enhanced_query: str
    action_taken: ActionType
    results: List[SearchResult]
    final_answer: str
    confidence: float
    processing_time: float
