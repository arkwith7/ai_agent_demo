# AI Agent Demo

## 프로젝트 개요

이 프로젝트는 LLM 기반 AI Agent 기술 체험을 위한 웹 애플리케이션 데모입니다.  
사용자는 자연어로 투자 관련 질문을 입력하고, AI Agent가 다양한 툴(예: BuffettFilterTool, NewsTool, ValuationTool)을 호출하여 데이터를 수집, 가공, 해석한 후 종목 추천 결과를 반환합니다.

## 프로젝트 구조

```
/ai_agent_demo
├── frontend/
│   ├── vue-project/          # Vue.js 기반 프론트엔드
│   └── resources/            # 정적 리소스 파일
├── backend/
│   ├── main.py              # FastAPI 실행 진입점
│   ├── api/                 # API 엔드포인트
│   ├── core/               # 핵심 비즈니스 로직
│   ├── db/                 # 데이터베이스 관련
│   ├── schemas/            # Pydantic 스키마
│   ├── services/           # 비즈니스 서비스
│   ├── test_*.py           # 테스트 파일들
│   └── create_admin.py     # 관리자 계정 생성 스크립트
├── venv/                   # Python 가상환경
├── .gitignore             # Git 무시 파일
├── Dockerfile             # Docker 설정
├── requirements.txt       # Python 의존성
└── README.md             # 프로젝트 문서
```

## 기술 환경

- **프로그램 언어:** Python 3.10+
- **백엔드:** FastAPI, Uvicorn
- **프론트엔드:** Vue.js
- **AI Agent:** LangChain, OpenAI GPT
- **인증:** JWT 기반 사용자 인증
- **DB:** SQLite, SQLAlchemy
- **테스트:** pytest
- **개발 환경:** VS Code, Docker

## 주요 기능

1. **AI Agent 기반 투자 분석**
   - 자연어 기반 투자 질의응답
   - 버핏 필터 기반 종목 분석
   - 뉴스 및 시장 데이터 분석

2. **사용자 관리**
   - JWT 기반 인증
   - 사용자 설정 저장
   - 관리자 기능

3. **테스트**
   - 버핏 필터 테스트
   - OpenDart API 테스트
   - 향상된 버핏 필터 테스트

## 실행 방법

1. **환경 설정**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **백엔드 서버 실행**
   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **프론트엔드 실행**
   ```bash
   cd frontend/vue-project
   npm install
   npm run serve
   ```

4. **관리자 계정 생성**
   ```bash
   cd backend
   python create_admin.py
   ```

## 테스트 실행

```bash
cd backend
pytest test_*.py
```

## Docker 실행

```bash
docker build -t ai-agent-demo .
docker run -p 8000:8000 ai-agent-demo
```