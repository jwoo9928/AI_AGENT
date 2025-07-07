#!/bin/bash

# AI Agent 설치 스크립트

echo "🚀 AI Agent 설치를 시작합니다..."

# Python 버전 확인
python_version=$(python3 --version 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ Python 확인됨: $python_version"
else
    echo "❌ Python 3이 설치되어 있지 않습니다."
    echo "Python 3.8 이상을 설치해주세요."
    exit 1
fi

# 가상환경 생성
echo "📦 가상환경 생성 중..."
python3 -m venv ai_agent_env

# 가상환경 활성화
echo "🔧 가상환경 활성화 중..."
source ai_agent_env/bin/activate

# 의존성 설치
echo "📥 의존성 설치 중..."
pip install --upgrade pip
pip install -r requirements.txt

# 환경 변수 파일 생성
echo "⚙️ 환경 변수 파일 설정 중..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 .env 파일이 생성되었습니다."
    echo "⚠️  .env 파일을 편집하여 API 키를 설정해주세요:"
    echo "   - GEMINI_API_KEY: Google Gemini API 키"
    echo "   - TAVILY_API_KEY: Tavily 검색 API 키"
else
    echo "✅ .env 파일이 이미 존재합니다."
fi

# 설치 완료
echo ""
echo "🎉 AI Agent 설치가 완료되었습니다!"
echo ""
echo "다음 단계:"
echo "1. .env 파일을 편집하여 API 키 설정"
echo "2. 가상환경 활성화: source ai_agent_env/bin/activate"
echo "3. 서버 실행: python main.py"
echo "4. 테스트 실행: python test_agent.py"
echo ""
echo "API 문서: http://localhost:8000/docs"
echo "데모 쿼리: http://localhost:8000/demo"
echo ""
echo "문제가 있으면 README.md를 확인해주세요."
