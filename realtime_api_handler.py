"""
Realtime API Handler - 실시간 API 데이터 처리
"""
import requests
import time
from typing import List, Dict, Any
from models import SearchResult


class RealtimeAPIHandler:
    """실시간 API 핸들러"""
    
    def __init__(self):
        pass
    
    def get_current_time(self) -> List[SearchResult]:
        """현재 시간 정보 반환"""
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        result = SearchResult(
            source="realtime_api",
            content=f"현재 시간: {current_time}",
            relevance_score=1.0,
            metadata={
                "type": "current_time",
                "timestamp": current_time
            }
        )
        
        return [result]
    
    def get_weather_info(self, location: str = "Seoul") -> List[SearchResult]:
        """
        날씨 정보 조회 (OpenWeatherMap API 예시)
        실제 구현 시 API 키 필요
        """
        # 이는 예시 구현입니다. 실제로는 OpenWeatherMap API 등을 사용해야 합니다.
        mock_weather = {
            "Seoul": {"temp": "15°C", "condition": "맑음", "humidity": "60%"},
            "Busan": {"temp": "18°C", "condition": "흐림", "humidity": "70%"},
            "Incheon": {"temp": "14°C", "condition": "비", "humidity": "85%"}
        }
        
        weather_data = mock_weather.get(location, mock_weather["Seoul"])
        
        content = f"{location}의 현재 날씨: 온도 {weather_data['temp']}, 날씨 {weather_data['condition']}, 습도 {weather_data['humidity']}"
        
        result = SearchResult(
            source="realtime_api",
            content=content,
            relevance_score=0.9,
            metadata={
                "type": "weather",
                "location": location,
                "temperature": weather_data["temp"],
                "condition": weather_data["condition"],
                "humidity": weather_data["humidity"]
            }
        )
        
        return [result]
    
    def get_stock_price(self, symbol: str) -> List[SearchResult]:
        """
        주식 가격 정보 조회 (Alpha Vantage API 예시)
        실제 구현 시 API 키 필요
        """
        # 이는 예시 구현입니다. 실제로는 Alpha Vantage API 등을 사용해야 합니다.
        mock_stocks = {
            "AAPL": {"price": "$150.25", "change": "+1.25%"},
            "GOOGL": {"price": "$2,450.30", "change": "-0.85%"},
            "TSLA": {"price": "$850.40", "change": "+2.15%"},
            "MSFT": {"price": "$305.60", "change": "+0.95%"}
        }
        
        stock_data = mock_stocks.get(symbol.upper(), {"price": "N/A", "change": "N/A"})
        
        content = f"{symbol.upper()} 주식 가격: {stock_data['price']}, 변동률: {stock_data['change']}"
        
        result = SearchResult(
            source="realtime_api",
            content=content,
            relevance_score=0.9,
            metadata={
                "type": "stock_price",
                "symbol": symbol.upper(),
                "price": stock_data["price"],
                "change": stock_data["change"]
            }
        )
        
        return [result]
    
    def get_crypto_price(self, symbol: str) -> List[SearchResult]:
        """
        암호화폐 가격 정보 조회
        CoinGecko API를 사용한 실제 구현 예시
        """
        try:
            # CoinGecko API는 무료로 사용 가능
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": symbol.lower(),
                "vs_currencies": "usd,krw",
                "include_24hr_change": "true"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if symbol.lower() in data:
                crypto_data = data[symbol.lower()]
                usd_price = crypto_data.get("usd", 0)
                krw_price = crypto_data.get("krw", 0)
                change_24h = crypto_data.get("usd_24h_change", 0)
                
                content = f"{symbol.upper()} 가격: ${usd_price:,.2f} (₩{krw_price:,.0f}), 24시간 변동률: {change_24h:.2f}%"
                
                result = SearchResult(
                    source="realtime_api",
                    content=content,
                    relevance_score=0.95,
                    metadata={
                        "type": "crypto_price",
                        "symbol": symbol.upper(),
                        "usd_price": usd_price,
                        "krw_price": krw_price,
                        "change_24h": change_24h
                    }
                )
                
                return [result]
            else:
                return self._get_crypto_not_found(symbol)
                
        except Exception as e:
            print(f"❌ 암호화폐 가격 조회 중 오류: {e}")
            # 에러 시에도 유용한 정보 제공
            error_result = SearchResult(
                source="realtime_api",
                content=f"{symbol.upper()} 암호화폐 가격 조회에 실패했습니다. 네트워크 연결을 확인해주세요.",
                relevance_score=0.2,
                metadata={
                    "type": "crypto_price",
                    "symbol": symbol.upper(),
                    "error": str(e),
                    "suggestion": "나중에 다시 시도해보세요"
                }
            )
            return [error_result]
    
    def _get_crypto_not_found(self, symbol: str) -> List[SearchResult]:
        """암호화폐를 찾을 수 없을 때 반환하는 결과"""
        result = SearchResult(
            source="realtime_api",
            content=f"{symbol.upper()} 암호화폐 정보를 찾을 수 없습니다.",
            relevance_score=0.3,
            metadata={
                "type": "crypto_price",
                "symbol": symbol.upper(),
                "error": "not_found"
            }
        )
        return [result]
    
    def search(self, query: str, parameters: Dict[str, Any] = None) -> List[SearchResult]:
        """
        실시간 API 검색 메인 함수 (에러 방어적)
        
        Args:
            query: 검색 쿼리
            parameters: 추가 매개변수
            
        Returns:
            검색 결과 리스트
        """
        if parameters is None:
            parameters = {}
        
        query_lower = query.lower()
        
        try:
            # 쿼리 분석하여 적절한 API 호출
            if "시간" in query_lower or "time" in query_lower:
                return self.get_current_time()
            elif "날씨" in query_lower or "weather" in query_lower:
                location = parameters.get("location", "Seoul")
                return self.get_weather_info(location)
            elif "주식" in query_lower or "stock" in query_lower:
                symbol = parameters.get("symbol", "AAPL")
                return self.get_stock_price(symbol)
            elif "암호화폐" in query_lower or "crypto" in query_lower or "bitcoin" in query_lower:
                symbol = parameters.get("symbol", "bitcoin")
                return self.get_crypto_price(symbol)
            else:
                # 기본적으로 현재 시간 반환
                return self.get_current_time()
        except Exception as e:
            print(f"❌ 실시간 API 내부 오류: {e}")
            # 에러 발생 시 기본 시간 정보라도 반환 시도
            try:
                return self.get_current_time()
            except Exception as e2:
                print(f"❌ 기본 시간 정보도 실패: {e2}")
                # 완전 실패 시 예외 발생 (상위에서 처리)
                raise Exception(f"실시간 API 완전 실패: {e}")
