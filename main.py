"""
FastAPI 서버 - AI Agent를 위한 REST API
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, Any

from models import QueryRequest, AgentResponse
from ai_agent import AIAgent
from config import Config

# AI Agent 인스턴스 (전역)
agent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 라이프사이클 관리"""
    # 시작 시
    global agent
    try:
        print("AI Agent 초기화 중...")
        agent = AIAgent()
        print("AI Agent 초기화 완료!")
    except Exception as e:
        print(f"AI Agent 초기화 실패: {e}")
        raise
    
    yield
    
    # 종료 시 (필요한 경우)
    print("AI Agent 종료 중...")


# FastAPI 앱 생성
app = FastAPI(
    title="AI Agent API",
    description="사용자 질의를 받아 Gemini가 증강하고 적절한 액션을 수행하는 지능형 에이전트",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "AI Agent API Server",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    if agent is None:
        raise HTTPException(status_code=503, detail="AI Agent가 초기화되지 않았습니다.")
    
    try:
        health_status = agent.health_check()
        return health_status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"헬스 체크 실패: {str(e)}")


@app.post("/query", response_model=AgentResponse)
async def process_query(request: QueryRequest):
    """
    사용자 쿼리 처리
    
    Args:
        request: 사용자 쿼리 요청
        
    Returns:
        처리된 응답
    """
    if agent is None:
        raise HTTPException(status_code=503, detail="AI Agent가 초기화되지 않았습니다.")
    
    if not request.query or request.query.strip() == "":
        raise HTTPException(status_code=400, detail="쿼리가 비어있습니다.")
    
    try:
        print(f"쿼리 처리 요청: {request.query}")
        response = agent.process_query(request)
        return response
    except Exception as e:
        print(f"쿼리 처리 중 오류: {e}")
        raise HTTPException(status_code=500, detail=f"쿼리 처리 실패: {str(e)}")


@app.get("/demo")
async def demo_queries():
    """데모용 쿼리 예시들"""
    return {
        "demo_queries": [
            {
                "category": "실시간 API",
                "query": "현재 시간을 알려주세요",
                "description": "실시간 시간 정보 조회"
            },
            {
                "category": "실시간 API",
                "query": "비트코인 가격이 궁금해요",
                "description": "실시간 암호화폐 가격 조회"
            },
            {
                "category": "웹 검색",
                "query": "2024년 최신 AI 뉴스를 알려주세요",
                "description": "최신 뉴스 및 정보 검색"
            },
            {
                "category": "웹 검색",
                "query": "Python FastAPI 튜토리얼을 찾아주세요",
                "description": "웹에서 프로그래밍 정보 검색"
            },
            {
                "category": "하이브리드",
                "query": "오늘 날씨와 관련된 최신 뉴스를 알려주세요",
                "description": "실시간 정보 + 웹검색 결합"
            }
        ]
    }


if __name__ == "__main__":
    print("AI Agent API Server 시작 중...")
    print(f"서버 주소: http://{Config.API_HOST}:{Config.API_PORT}")
    print("API 문서: http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",  # import string 형태로 변경
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=True
    )
