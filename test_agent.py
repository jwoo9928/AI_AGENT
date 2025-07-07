"""
AI Agent 테스트 스크립트
"""
import asyncio
import json
from models import QueryRequest
from ai_agent import AIAgent


async def test_queries():
    """다양한 쿼리 테스트"""
    
    print("=== AI Agent 테스트 시작 ===\n")
    
    # AI Agent 초기화
    try:
        agent = AIAgent()
    except Exception as e:
        print(f"AI Agent 초기화 실패: {e}")
        print("API 키가 올바르게 설정되었는지 확인해주세요.")
        return
    
    # 테스트 쿼리들
    test_queries = [
        {
            "query": "현재 시간을 알려주세요",
            "expected_action": "realtime_api",
            "description": "실시간 시간 정보 조회"
        },
        {
            "query": "비트코인 가격이 궁금해요",
            "expected_action": "realtime_api",
            "description": "실시간 암호화폐 가격 조회"
        },
        {
            "query": "2024년 최신 AI 뉴스를 알려주세요",
            "expected_action": "web_search",
            "description": "웹에서 최신 뉴스 검색"
        },
        {
            "query": "Python FastAPI 사용법을 알려주세요",
            "expected_action": "web_search",
            "description": "웹에서 프로그래밍 정보 검색"
        },
        {
            "query": "오늘 날씨와 관련된 최신 뉴스를 알려주세요",
            "expected_action": "hybrid",
            "description": "실시간 정보 + 웹검색 결합"
        }
    ]
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"\n{'='*50}")
        print(f"테스트 {i}: {test_case['description']}")
        print(f"쿼리: {test_case['query']}")
        print(f"예상 액션: {test_case['expected_action']}")
        print(f"{'='*50}")
        
        try:
            request = QueryRequest(query=test_case['query'])
            response = agent.process_query(request)
            
            print(f"\n✅ 처리 완료!")
            print(f"📝 원본 쿼리: {response.query}")
            print(f"🔧 증강된 쿼리: {response.enhanced_query}")
            print(f"🎯 실행된 액션: {response.action_taken}")
            print(f"🔍 검색 결과 수: {len(response.results)}")
            print(f"⭐ 신뢰도: {response.confidence:.2f}")
            print(f"⏱️ 처리 시간: {response.processing_time:.2f}초")
            
            print(f"\n📋 검색 결과:")
            for j, result in enumerate(response.results[:2], 1):  # 상위 2개만 표시
                print(f"  {j}. [{result.source}] {result.content[:100]}...")
                if result.metadata:
                    print(f"     메타데이터: {json.dumps(result.metadata, ensure_ascii=False, indent=6)}")
            
            print(f"\n💬 최종 답변:")
            print(f"   {response.final_answer}")
            
            # 예상 액션과 실제 액션 비교
            if response.action_taken.value == test_case['expected_action']:
                print(f"\n✅ 액션 분류 정확!")
            else:
                print(f"\n⚠️ 액션 분류 차이: 예상 {test_case['expected_action']} vs 실제 {response.action_taken}")
                
        except Exception as e:
            print(f"\n❌ 테스트 실패: {e}")
        
        print(f"\n{'='*50}")
        input("다음 테스트를 계속하려면 Enter를 누르세요...")
    
    print(f"\n🎉 모든 테스트 완료!")


if __name__ == "__main__":
    print("AI Agent 테스트 스크립트")
    print("1. 쿼리 테스트")
    
    choice = input("\n선택하세요 (1): ").strip()
    
    if choice == "1":
        asyncio.run(test_queries())
    else:
        asyncio.run(test_queries())
