# AI Agent - Smart Query Processing System

## 프로젝트 개요
사용자 질의를 받아 Gemini가 쿼리를 증강하고, 필요한 액션(Realtime API, Web Search)을 자동으로 판단하여 실행하는 지능형 시스템입니다.

## 아키텍처
```
사용자 쿼리 → Gemini 쿼리 증강 → 액션 분류기 → [Realtime API | Web Search] → 응답 생성
```

## 주요 기능
- **쿼리 증강**: Gemini API를 통한 사용자 질의 고도화
- **자동 액션 분류**: 증강된 쿼리 분석으로 적절한 데이터 소스 선택
- **다중 데이터 소스**: Realtime API, Web Search 지원
- **통합 응답**: 여러 소스의 정보를 종합한 최종 응답 생성

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 편집하여 API 키 설정
```

### 3. 실행
```bash
python main.py
```

## API 엔드포인트
- `POST /query`: 사용자 질의 처리
- `GET /health`: 헬스 체크
- `GET /demo`: 데모 쿼리 예시

## 기술 스택
- **Python**: 메인 개발 언어
- **Gemini 2.0 Flash**: 쿼리 증강 및 액션 분류 (HTTP 요청)
- **Tavily API**: 웹 검색
- **FastAPI**: REST API 서버

## 주요 업데이트
- Gemini 2.0 Flash 모델 사용
- 개선된 JSON 파싱 (```json 래핑 처리)
- 더 견고한 에러 처리
- 연결 테스트 기능 추가
- 벡터 DB 제거로 시스템 단순화
