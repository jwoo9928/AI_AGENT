"""
Main AI Agent - 모든 컴포넌트를 통합하는 핵심 에이전트
"""
import time
from typing import List, Dict, Any
from models import (
    QueryRequest, EnhancedQuery, ActionDecision, 
    AgentResponse, SearchResult, ActionType
)
from gemini_client import GeminiClient
from web_search_handler import WebSearchHandler
from realtime_api_handler import RealtimeAPIHandler


class AIAgent:
    """AI 에이전트 메인 클래스"""
    
    def __init__(self):
        """에이전트 초기화"""
        print("AI Agent 초기화 중...")
        
        # 각 핸들러 초기화
        self.gemini_client = GeminiClient()
        self.web_search_handler = WebSearchHandler()
        self.realtime_api_handler = RealtimeAPIHandler()
        
        print("AI Agent 초기화 완료!")
    
    def process_query(self, request: QueryRequest) -> AgentResponse:
        """
        사용자 쿼리 처리
        
        Args:
            request: 사용자 쿼리 요청
            
        Returns:
            처리된 응답
        """
        start_time = time.time()
        
        try:
            # 1. Gemini로 쿼리 증강
            print(f"1. 쿼리 증강 중: {request.query}")
            enhanced_data = self.gemini_client.enhance_query(request.query)
            enhanced_query = EnhancedQuery(**enhanced_data)
            
            # 2. 액션 분류
            print(f"2. 액션 분류 중...")
            action_data = self.gemini_client.classify_action(
                enhanced_query.enhanced_query,
                enhanced_query.keywords,
                enhanced_query.intent
            )
            action_decision = ActionDecision(**action_data)
            
            # 3. 선택된 액션 실행
            print(f"3. 액션 실행 중: {action_decision.action_type}")
            search_results = self._execute_action(
                action_decision, 
                enhanced_query
            )
            
            # 4. 최종 응답 생성
            print(f"4. 최종 응답 생성 중...")
            final_answer = self._generate_final_answer(
                enhanced_query, 
                search_results
            )
            
            processing_time = time.time() - start_time
            
            response = AgentResponse(
                query=request.query,
                enhanced_query=enhanced_query.enhanced_query,
                action_taken=ActionType(action_decision.action_type),
                results=search_results,
                final_answer=final_answer,
                confidence=action_decision.confidence,
                processing_time=processing_time
            )
            
            print(f"처리 완료! (소요 시간: {processing_time:.2f}초)")
            return response
            
        except Exception as e:
            print(f"쿼리 처리 중 오류 발생: {e}")
            
            # 오류 발생 시 기본 응답
            processing_time = time.time() - start_time
            return AgentResponse(
                query=request.query,
                enhanced_query=request.query,
                action_taken=ActionType.WEB_SEARCH,
                results=[],
                final_answer=f"죄송합니다. 쿼리 처리 중 오류가 발생했습니다: {str(e)}",
                confidence=0.0,
                processing_time=processing_time
            )
    
    def _execute_action(self, action_decision: ActionDecision, enhanced_query: EnhancedQuery) -> List[SearchResult]:
        """
        액션 실행
        
        Args:
            action_decision: 액션 결정 정보
            enhanced_query: 증강된 쿼리
            
        Returns:
            검색 결과 리스트
        """
        action_type = ActionType(action_decision.action_type)
        query = enhanced_query.enhanced_query
        
        if action_type == ActionType.REALTIME_API:
            try:
                return self.realtime_api_handler.search(
                    query, 
                    action_decision.parameters
                )
            except Exception as e:
                print(f"❌ 실시간 API 검색 실패: {e}")
                # 실패 시 빈 결과 대신 에러 정보를 포함한 결과 반환
                from models import SearchResult
                error_result = SearchResult(
                    source="realtime_api_error",
                    content=f"실시간 API 검색 중 오류가 발생했습니다: {str(e)}",
                    relevance_score=0.1,
                    metadata={"error": str(e), "query": query}
                )
                return [error_result]
        
        elif action_type == ActionType.WEB_SEARCH:
            try:
                return self.web_search_handler.search(query)
            except Exception as e:
                print(f"❌ 웹 검색 실패: {e}")
                # 실패 시 빈 결과 대신 에러 정보를 포함한 결과 반환
                from models import SearchResult
                error_result = SearchResult(
                    source="web_search_error",
                    content=f"웹 검색 중 오류가 발생했습니다: {str(e)}",
                    relevance_score=0.1,
                    metadata={"error": str(e), "query": query}
                )
                return [error_result]
        
        elif action_type == ActionType.HYBRID:
            # 하이브리드: 웹 검색 + 실시간 API (에러 방어적 처리)
            results = []
            errors = []
            
            # 웹 검색 (에러 방어적)
            try:
                print("🌐 웹 검색 시도 중...")
                web_results = self.web_search_handler.search(query, max_results=3)
                if web_results:
                    results.extend(web_results)
                    print(f"✅ 웹 검색 성공: {len(web_results)}개 결과")
                else:
                    print("⚠️ 웹 검색 결과 없음")
            except Exception as e:
                error_msg = f"웹 검색 실패: {str(e)}"
                print(f"❌ {error_msg}")
                errors.append(error_msg)
            
            # 실시간 API (에러 방어적)
            if self._is_realtime_relevant(query):
                try:
                    print("⏰ 실시간 API 시도 중...")
                    realtime_results = self.realtime_api_handler.search(
                        query, 
                        action_decision.parameters
                    )
                    if realtime_results:
                        results.extend(realtime_results)
                        print(f"✅ 실시간 API 성공: {len(realtime_results)}개 결과")
                    else:
                        print("⚠️ 실시간 API 결과 없음")
                except Exception as e:
                    error_msg = f"실시간 API 실패: {str(e)}"
                    print(f"❌ {error_msg}")
                    errors.append(error_msg)
            else:
                print("ℹ️ 실시간 API 관련성 없음 - 건너뜀")
            
            # 결과 처리
            if results:
                # 관련성 점수로 정렬
                results.sort(key=lambda x: x.relevance_score, reverse=True)
                
                # 에러가 있었다면 메타데이터에 추가
                if errors:
                    for result in results:
                        if "hybrid_errors" not in result.metadata:
                            result.metadata["hybrid_errors"] = errors
                
                print(f"🎯 하이브리드 검색 완료: {len(results)}개 결과 (에러 {len(errors)}개)")
                return results[:5]  # 상위 5개만 반환
            else:
                # 모든 검색이 실패한 경우 에러 정보를 포함한 기본 결과 반환
                print("❌ 모든 하이브리드 검색 실패")
                from models import SearchResult
                error_result = SearchResult(
                    source="hybrid_error",
                    content=f"하이브리드 검색 중 오류가 발생했습니다: {'; '.join(errors)}",
                    relevance_score=0.1,
                    metadata={
                        "errors": errors,
                        "query": query,
                        "action_type": "hybrid_failed"
                    }
                )
                return [error_result]
            return results[:5]  # 상위 5개만 반환
        
        else:
            # 기본값: 웹 검색
            return self.web_search_handler.search(query)
    
    def _is_realtime_relevant(self, query: str) -> bool:
        """실시간 API가 관련성이 있는지 확인"""
        realtime_keywords = [
            "시간", "날씨", "주식", "암호화폐", "bitcoin", "실시간", 
            "현재", "지금", "today", "current", "live", "price"
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in realtime_keywords)
    
    def _generate_final_answer(self, enhanced_query: EnhancedQuery, search_results: List[SearchResult]) -> str:
        """
        최종 응답 생성 (에러 방어적)
        
        Args:
            enhanced_query: 증강된 쿼리
            search_results: 검색 결과들
            
        Returns:
            최종 답변
        """
        if not search_results:
            return "죄송합니다. 관련된 정보를 찾을 수 없습니다."
        
        # 에러 결과가 있는지 확인
        error_results = [r for r in search_results if "error" in r.source]
        valid_results = [r for r in search_results if "error" not in r.source]
        
        # 유효한 결과가 있으면 그것을 우선 사용
        results_to_use = valid_results if valid_results else search_results
        
        # 검색 결과를 종합하여 답변 생성
        context_parts = []
        
        for i, result in enumerate(results_to_use[:3]):  # 상위 3개 결과만 사용
            # 에러 결과인 경우 특별 처리
            if "error" in result.source:
                context_parts.append(f"⚠️ {result.source}: {result.content}")
            else:
                context_parts.append(f"출처 {i+1} ({result.source}): {result.content}")
        
        context = "\n\n".join(context_parts)
        
        # 에러가 있었던 경우 프롬프트에 명시
        error_note = ""
        if error_results:
            error_note = f"\n\n참고: 일부 검색에서 오류가 발생했지만, 가능한 정보로 답변을 제공합니다."
        
        # Gemini로 최종 답변 생성
        final_prompt = f"""
        사용자의 질문: {enhanced_query.enhanced_query}
        
        검색된 정보:
        {context}{error_note}
        
        위의 정보를 바탕으로 사용자의 질문에 대해 정확하고 유용한 답변을 제공해주세요.
        답변은 한국어로 작성하고, 가능한 한 구체적이고 도움이 되도록 해주세요.
        만약 정보가 불완전하거나 오류가 있었다면, 그 점도 언급해주세요.
        """
        
        try:
            final_answer = self.gemini_client.generate_content(final_prompt)
            return final_answer
        except Exception as e:
            print(f"❌ 최종 답변 생성 중 오류: {e}")
            # Gemini 실패 시 기본적인 정보 요약 제공
            if valid_results:
                summary = f"검색 결과를 요약하면:\n\n{context}"
            else:
                summary = f"검색 중 일부 오류가 발생했습니다:\n\n{context}"
            
            return summary + f"\n\n(참고: AI 응답 생성 중 오류가 발생하여 원본 검색 결과를 제공합니다.)"
    
    def health_check(self) -> Dict[str, Any]:
        """시스템 상태 확인"""
        return {
            "status": "healthy",
            "components": {
                "gemini_client": "connected",
                "web_search": "connected",
                "realtime_api": "connected"
            },
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
