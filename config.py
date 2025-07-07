"""
Configuration settings for AI Agent
"""
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class Config:
    """애플리케이션 설정"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    
    # Gemini API 설정
    GEMINI_MODEL = "gemini-2.5-pro"
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    
    # Gemini 2.5 Pro 전용 설정
    GEMINI_THINKING_BUDGET = -1  # 무제한 사고 과정
    
    # API 서버 설정
    API_HOST = os.getenv("API_HOST", "localhost")
    API_PORT = int(os.getenv("API_PORT", 8000))
    
    # 쿼리 증강 프롬프트
    QUERY_ENHANCEMENT_PROMPT = """
    당신은 사용자의 질문을 분석하고 개선하는 전문가입니다.
    주어진 질문을 다음과 같이 분석하고 개선해주세요:

    1. 질문의 핵심 의도 파악
    2. 검색에 효과적인 키워드 추출
    3. 질문을 더 구체적이고 명확하게 재구성
    4. 질문의 복잡도 평가 (1-10 점수)

    원본 질문: {original_query}

    다음 JSON 형태로 응답해주세요:
    {{
        "enhanced_query": "개선된 질문",
        "keywords": ["키워드1", "키워드2", "키워드3"],
        "intent": "질문의 의도",
        "complexity_score": 점수
    }}
    """
    
    # 액션 분류 프롬프트
    ACTION_CLASSIFICATION_PROMPT = """
    다음 증강된 질문을 분석하여 어떤 데이터 소스가 필요한지 판단해주세요:

    증강된 질문: {enhanced_query}
    키워드: {keywords}
    의도: {intent}

    판단 기준:
    - realtime_api: 실시간 데이터나 최신 정보가 필요한 경우
    - web_search: 일반적인 웹 검색이 필요한 경우
    - hybrid: 여러 소스의 정보가 모두 필요한 경우

    다음 JSON 형태로 응답해주세요:
    {{
        "action_type": "선택된_액션",
        "confidence": 신뢰도_점수_0_to_1,
        "reasoning": "선택 이유",
        "parameters": {{"추가_매개변수": "값"}}
    }}
    """
