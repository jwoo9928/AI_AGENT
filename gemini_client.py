"""
Gemini API Client - HTTP 요청으로 Gemini API 호출
"""
import json
import requests
from typing import Dict, Any
from config import Config


class GeminiClient:
    """Gemini API 클라이언트 (HTTP 요청 기반)"""
    
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.model = Config.GEMINI_MODEL
        self.api_url = Config.GEMINI_API_URL.format(model=self.model)
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")
    
    def generate_content(self, prompt: str) -> str:
        """
        Gemini API로 콘텐츠 생성 (단순화된 버전)
        
        Args:
            prompt: 입력 프롬프트
            
        Returns:
            생성된 텍스트
        """
        headers = {
            "Content-Type": "application/json",
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 9000,
                "responseMimeType": "text/plain"
            }
        }
        
        # API 키를 URL 파라미터로 추가
        url = f"{self.api_url}?key={self.api_key}"
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            
            data = response.json()
            print(f"📨 Gemini API 원본 응답: {data}")
            
            # 안전한 응답 파싱
            try:
                # 기본 구조 확인
                if 'candidates' not in data or not data['candidates']:
                    raise Exception("응답에 candidates가 없습니다")
                
                candidate = data['candidates'][0]
                
                # content 구조 확인 및 파싱
                if 'content' in candidate:
                    content = candidate['content']
                    if 'parts' in content and content['parts']:
                        text = content['parts'][0].get('text', '')
                        if text:
                            return text.strip()
                
                # finishReason이 'SAFETY' 등인 경우 처리
                if 'finishReason' in candidate:
                    finish_reason = candidate['finishReason']
                    if finish_reason == 'SAFETY':
                        raise Exception("안전 필터로 인해 응답이 차단되었습니다")
                    elif finish_reason == 'MAX_TOKENS':
                        raise Exception("최대 토큰 수 초과로 응답이 잘렸습니다")
                
                # 모든 파싱 시도 실패
                raise Exception(f"예상과 다른 응답 구조: {data}")
                
            except Exception as parse_error:
                print(f"❌ 응답 파싱 중 세부 오류: {parse_error}")
                raise Exception(f"Gemini API 응답 파싱 실패: {parse_error}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Gemini API 요청 실패: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Gemini API 응답 JSON 파싱 실패: {e}")
    
    def enhance_query(self, original_query: str) -> Dict[str, Any]:
        """
        사용자 쿼리를 증강
        
        Args:
            original_query: 원본 쿼리
            
        Returns:
            증강된 쿼리 정보
        """
        print(f"🔧 쿼리 증강 시작: '{original_query}'")
        
        prompt = Config.QUERY_ENHANCEMENT_PROMPT.format(
            original_query=original_query
        )
        
        response = self.generate_content(prompt)
        print(f"📝 Gemini 증강 원본 응답:\n{response}")
        
        try:
            # JSON 응답을 파싱
            # Gemini가 ```json으로 래핑할 수 있으므로 정리
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            enhanced_data = json.loads(cleaned_response)
            enhanced_data["original_query"] = original_query
            
            print("✅ 쿼리 증강 완료:")
            print(f"   📈 증강된 쿼리: '{enhanced_data.get('enhanced_query', 'N/A')}'")
            print(f"   🔑 키워드: {enhanced_data.get('keywords', [])}")
            print(f"   🎯 의도: {enhanced_data.get('intent', 'N/A')}")
            print(f"   📊 복잡도: {enhanced_data.get('complexity_score', 'N/A')}/10")
            
            return enhanced_data
        except json.JSONDecodeError as e:
            print(f"❌ JSON 파싱 실패: {e}")
            print(f"❌ 응답 내용: {response}")
            # JSON 파싱 실패 시 기본값 반환
            fallback_data = {
                "original_query": original_query,
                "enhanced_query": original_query,
                "keywords": [original_query],
                "intent": "정보 검색",
                "complexity_score": 5.0
            }
            print(f"🔄 기본값으로 대체: {fallback_data}")
            return fallback_data
    
    def classify_action(self, enhanced_query: str, keywords: list, intent: str) -> Dict[str, Any]:
        """
        액션 분류
        
        Args:
            enhanced_query: 증강된 쿼리
            keywords: 키워드 리스트
            intent: 의도
            
        Returns:
            액션 분류 결과
        """
        print(f"🎯 액션 분류 시작:")
        print(f"   📝 증강된 쿼리: '{enhanced_query}'")
        print(f"   🔑 키워드: {keywords}")
        print(f"   💭 의도: '{intent}'")
        
        prompt = Config.ACTION_CLASSIFICATION_PROMPT.format(
            enhanced_query=enhanced_query,
            keywords=", ".join(keywords),
            intent=intent
        )
        
        response = self.generate_content(prompt)
        print(f"📝 Gemini 분류 원본 응답:\n{response}")
        
        try:
            # JSON 응답을 파싱
            # Gemini가 ```json으로 래핑할 수 있으므로 정리
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            action_data = json.loads(cleaned_response)
            
            print("✅ 액션 분류 완료:")
            print(f"   🚀 선택된 액션: {action_data.get('action_type', 'N/A')}")
            print(f"   📊 신뢰도: {action_data.get('confidence', 'N/A')}")
            print(f"   💡 선택 이유: {action_data.get('reasoning', 'N/A')}")
            print(f"   ⚙️ 매개변수: {action_data.get('parameters', {})}")
            
            return action_data
        except json.JSONDecodeError as e:
            print(f"❌ JSON 파싱 실패: {e}")
            print(f"❌ 응답 내용: {response}")
            # JSON 파싱 실패 시 기본값 반환
            fallback_data = {
                "action_type": "web_search",
                "confidence": 0.5,
                "reasoning": "기본 웹 검색으로 설정 (파싱 실패)",
                "parameters": {}
            }
            print(f"🔄 기본값으로 대체: {fallback_data}")
            return fallback_data

