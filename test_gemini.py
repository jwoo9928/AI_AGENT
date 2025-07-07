#!/usr/bin/env python3
"""
Gemini API 테스트 스크립트
"""
import sys
import os

# 현재 디렉토리를 Python 패스에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gemini_client import GeminiClient
from config import Config

def test_gemini_api():
    """Gemini API 기본 테스트"""
    print("=" * 60)
    print("🧪 Gemini 2.5 Pro API 테스트")
    print("=" * 60)
    
    # API 키 확인
    if not Config.GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY가 설정되지 않았습니다.")
        print("💡 .env 파일에 GEMINI_API_KEY를 설정해주세요.")
        return False
    
    try:
        # Gemini 클라이언트 초기화
        print("🚀 Gemini 클라이언트 초기화 중...")
        client = GeminiClient()
        
        # 모델 정보 출력
        model_info = client.get_model_info()
        print(f"📋 모델 정보:")
        for key, value in model_info.items():
            print(f"   {key}: {value}")
        
        # 연결 테스트
        print("\n🔗 연결 테스트 실행 중...")
        if client.test_connection():
            print("✅ 연결 테스트 성공!")
        else:
            print("❌ 연결 테스트 실패!")
            return False
        
        # 기본 텍스트 생성 테스트
        print("\n📝 기본 텍스트 생성 테스트...")
        test_prompt = "한국의 수도는 어디인가요? 간단히 답변해주세요."
        response = client.generate_content(test_prompt)
        print(f"✅ 응답: {response}")
        
        # JSON 응답 테스트
        print("\n🔧 JSON 응답 테스트...")
        json_prompt = """
        다음 정보를 JSON 형태로 응답해주세요:
        {
            "country": "대한민국",
            "capital": "서울",
            "population": "약 5천만명"
        }
        """
        json_response = client.generate_content(json_prompt)
        print(f"✅ JSON 응답: {json_response}")
        
        # 쿼리 증강 테스트
        print("\n🔍 쿼리 증강 테스트...")
        enhanced = client.enhance_query("AI가 뭐야?")
        print(f"✅ 증강된 쿼리: {enhanced}")
        
        # 액션 분류 테스트
        print("\n🎯 액션 분류 테스트...")
        action = client.classify_action(
            enhanced_query="인공지능의 정의와 활용 분야",
            keywords=["AI", "인공지능", "정의"],
            intent="정보 검색"
        )
        print(f"✅ 액션 분류: {action}")
        
        print("\n🎉 모든 테스트 완료!")
        return True
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    success = test_gemini_api()
    if success:
        print("\n✅ Gemini 2.5 Pro API가 정상적으로 작동합니다!")
    else:
        print("\n❌ Gemini API 설정을 확인해주세요.")
        print("💡 .env 파일에 올바른 GEMINI_API_KEY를 설정했는지 확인하세요.")
    
    sys.exit(0 if success else 1)
