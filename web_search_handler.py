"""
Web Search Handler using Tavily API
"""
import requests
from typing import List, Dict, Any
from config import Config
from models import SearchResult


class WebSearchHandler:
    """웹 검색 핸들러 - Tavily API 사용"""
    
    def __init__(self):
        self.api_key = Config.TAVILY_API_KEY
        self.api_url = "https://api.tavily.com/search"
        
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY가 설정되지 않았습니다.")
    
    def search(self, query: str, max_results: int = 5) -> List[SearchResult]:
        """
        웹 검색 수행
        
        Args:
            query: 검색 쿼리
            max_results: 최대 결과 수
            
        Returns:
            검색 결과 리스트
        """
        try:
            headers = {
                "Content-Type": "application/json"
            }
            
            payload = {
                "api_key": self.api_key,
                "query": query,
                "search_depth": "basic",
                "include_answer": True,
                "include_images": False,
                "include_raw_content": True,
                "max_results": max_results
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            try:
                data = response.json()
            except Exception as e:
                print(f"❌ JSON 파싱 실패: {e}")
                print(f"❌ 응답 내용: {response.text[:500]}")
                raise Exception(f"API 응답 JSON 파싱 실패: {e}")
            
            # 응답 데이터 검증
            if not data:
                print("❌ 빈 응답 데이터")
                raise Exception("빈 응답 데이터")
            
            if not isinstance(data, dict):
                print(f"❌ 예상과 다른 응답 타입: {type(data)}")
                raise Exception(f"예상과 다른 응답 타입: {type(data)}")
            
            print(f"📊 Tavily API 응답 구조: {list(data.keys())}")
            
            results = []
            
            # Tavily 검색 결과 파싱
            if "results" in data and data["results"]:
                print(f"📝 검색 결과 {len(data['results'])}개 발견")
                for idx, result in enumerate(data["results"]):
                    if not isinstance(result, dict):
                        print(f"⚠️ 결과 {idx}가 dict가 아님: {type(result)}")
                        continue
                        
                    # raw_content 안전 처리
                    raw_content = result.get("raw_content", "")
                    if raw_content and len(raw_content) > 1000:
                        raw_content = raw_content[:1000]
                    
                    search_result = SearchResult(
                        source="web_search",
                        content=result.get("content", ""),
                        relevance_score=float(result.get("score", 0.5)),
                        metadata={
                            "title": result.get("title", ""),
                            "url": result.get("url", ""),
                            "published_date": result.get("published_date", ""),
                            "raw_content": raw_content
                        }
                    )
                    results.append(search_result)
            else:
                print("⚠️ 'results' 키가 없거나 비어있음")
            
            # Tavily 답변이 있는 경우 추가
            if "answer" in data and data["answer"]:
                print(f"📋 Tavily 답변 발견: {data['answer'][:100]}...")
                answer_result = SearchResult(
                    source="web_search_summary",
                    content=str(data["answer"]),
                    relevance_score=0.9,
                    metadata={
                        "type": "tavily_answer",
                        "query": query
                    }
                )
                results.insert(0, answer_result)  # 답변을 맨 앞에 추가
            
            print(f"✅ 총 {len(results)}개 검색 결과 반환")
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 웹 검색 API 요청 실패: {e}")
            # 네트워크 에러 시 빈 리스트 반환 (상위에서 처리)
            raise Exception(f"웹 검색 API 연결 실패: {e}")
        except Exception as e:
            print(f"❌ 웹 검색 중 오류 발생: {e}")
            # 기타 에러 시 예외 발생 (상위에서 처리)
            raise Exception(f"웹 검색 처리 실패: {e}")
    
    def search_news(self, query: str, max_results: int = 3) -> List[SearchResult]:
        """
        뉴스 검색 수행
        
        Args:
            query: 검색 쿼리
            max_results: 최대 결과 수
            
        Returns:
            뉴스 검색 결과 리스트
        """
        try:
            headers = {
                "Content-Type": "application/json"
            }
            
            payload = {
                "api_key": self.api_key,
                "query": f"{query} news",
                "search_depth": "basic",
                "include_answer": False,
                "include_images": False,
                "include_raw_content": True,
                "max_results": max_results,
                "include_domains": ["news.google.com", "reuters.com", "bbc.com", "cnn.com"]
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            try:
                data = response.json()
            except Exception as e:
                print(f"❌ 뉴스 검색 JSON 파싱 실패: {e}")
                return []
            
            # 응답 데이터 검증
            if not data or not isinstance(data, dict):
                print("❌ 뉴스 검색 - 빈 응답 또는 잘못된 타입")
                return []
            
            results = []
            
            if "results" in data and data["results"]:
                for result in data["results"]:
                    if not isinstance(result, dict):
                        continue
                        
                    search_result = SearchResult(
                        source="news_search",
                        content=result.get("content", ""),
                        relevance_score=float(result.get("score", 0.5)),
                        metadata={
                            "title": result.get("title", ""),
                            "url": result.get("url", ""),
                            "published_date": result.get("published_date", ""),
                            "type": "news"
                        }
                    )
                    results.append(search_result)
            
            return results
            
        except Exception as e:
            print(f"뉴스 검색 중 오류 발생: {e}")
            return []
