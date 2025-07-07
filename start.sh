#!/bin/bash

# AI Agent 실행 스크립트

echo "🚀 AI Agent 시작 중..."

# .env 파일 확인
if [ ! -f .env ]; then
    echo "❌ .env 파일이 없습니다."
    echo "📝 .env.example을 복사하여 .env 파일을 만들고 API 키를 설정해주세요:"
    echo "   cp .env.example .env"
    echo "   vim .env  # 또는 다른 편집기로 편집"
    exit 1
fi

# 가상환경 확인 및 활성화
if [ ! -d ".venv" ]; then
    echo "📦 가상환경이 없습니다. 먼저 ./install.sh를 실행해주세요."
    exit 1
fi

echo "🔧 가상환경 활성화 중..."
source .venv/bin/activate

echo "🌟 AI Agent API 서버 시작!"
echo "📚 API 문서: http://localhost:8000/docs"
echo "🔍 데모 쿼리: http://localhost:8000/demo"
echo ""
echo "종료하려면 Ctrl+C를 누르세요."
echo ""

python main.py
