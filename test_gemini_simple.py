#!/usr/bin/env python3
"""
Gemini API 단순 테스트 스크립트
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gemini_client import GeminiClient

def test_gemini():
    """Gemini API 기본 테스트"""
    try:
        print("=" * 50)
        print("🧪 Gemini API 단순 테스트 시작")
        print("=" * 50)
        
        # 클라이언트 초기화
        client = GeminiClient()
        
        # 연결 테스트
        print("\n1️⃣ 연결 테스트:")
        success = client.test_connection()
        
        if not success:
            print("❌ 연결 테스트 실패 - 테스트 중단")
            return
        
        # 쿼리 증강 테스트
        print("\n2️⃣ 쿼리 증강 테스트:")
        test_query = "비트코인 가격이 궁금해요"
        enhanced_result = client.enhance_query(test_query)
        
        # 액션 분류 테스트
        print("\n3️⃣ 액션 분류 테스트:")
        action_result = client.classify_action(
            enhanced_result["enhanced_query"],
            enhanced_result["keywords"],
            enhanced_result["intent"]
        )
        
        print("\n" + "=" * 50)
        print("🎉 모든 테스트 완료!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ 테스트 중 오류 발생: {e}")
        import traceback
        print(f"❌ 상세 오류:\n{traceback.format_exc()}")

if __name__ == "__main__":
    test_gemini()
