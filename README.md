# AI Agent Demo

## 프로젝트 개요

이 프로젝트는 LLM 기반 AI Agent 기술 체험을 위한 웹 애플리케이션 데모입니다.  
사용자는 자연어로 투자 관련 질문을 입력하고, AI Agent가 다양한 툴(예: BuffettFilterTool, NewsTool, ValuationTool)을 호출하여 데이터를 수집, 가공, 해석한 후 종목 추천 결과를 반환합니다.

## 프로젝트 구조

```
/ai_agent_demo
├── frontend/
│   ├── main.py                # 전체 앱 진입점 (랜딩 페이지 및 내비게이션 처리)
│   ├── landing_page.py        # 메인(랜딩) 페이지 관련 코드
│   ├── chat_page.py           # 투자 AI 체험(채팅) 페이지 관련 코드
│   ├── report_page.py         # 분석 결과 리포트 페이지 관련 코드
│   ├── simulation_page.py     # 모의 투자 페이지 관련 코드
│   ├── utils.py               # get_recommendations 등 공통 유틸리티 함수
│   └── resources/  
│       ├── css/               # CSS 파일 관리 (필요한 경우)
│       └── images/            # 이미지 파일 관리 (예: hero 배경 이미지)
│           └── hero_background.jpg  # hero 섹션에 사용할 이미지
├── backend/
│ ├── main.py # FastAPI 실행 진입점
│ ├── api/
│ │ ├── auth.py # 로그인/회원가입/JWT
│ │ ├── user.py # 사용자 설정/조건 저장
│ │ └── chat.py # Agent 질의응답 API
│ ├── core/
│ │ ├── agent.py # LangChain Agent 설정
│ │ └── tools/ # BuffettFilterTool 등 커스텀 툴
│ ├── models/
│ │ └── models.py # SQLAlchemy ORM 정의
│ ├── db.py # SQLite 연동
│ └── security.py # JWT 헬퍼
├── .env
├── .env.example # 환경변수 예제 파일
├── .gitignore # Git 무시 파일
├── Dockerfile  
├── requirements.txt
└── README.md # 프로젝트 개요 및 실행 방법 안내

.
├── frontend
│   ├── chat_page.py
│   ├── landing_page.py
│   ├── main.py
│   ├── report_page.py
│   ├── resources
│   │   ├── css
│   │   └── images
│   ├── simulation_page.py
│   ├── streamlit_app.py
│   └── utils.py
├── backend
│   ├── api
│   │   ├── auth.py
│   │   ├── chat.py
│   │   └── user.py
│   ├── core
│   │   ├── agent.py
│   │   └── tools
│   │       └── buffett_filter_tool.py
│   ├── db.py
│   ├── main.py
│   ├── models
│   │   └── models.py
│   └── security.py
├── Dockerfile
├── README.md
└── requirements.txt

```

## 기술 환경

- **프로그램 언어:** Python 3.10+
- **백엔드:** FastAPI, Uvicorn
- **프론트엔드:** Streamlit (추후 React 등으로 교체 가능)
- **AI Agent:** LangChain, OpenAI GPT (또는 Azure OpenAI)
- **인증:** JWT 기반 사용자 인증 및 세션 관리
- **DB:** SQLite, SQLAlchemy
- **개발 환경:** VS Code, GitHub Copilot, Docker (선택)

## 실행 방법

1. **환경 설정**  
   - 프로젝트 루트 디렉토리에 `.env.example` 파일을 참고하여 `.env` 파일을 생성하고 필요한 환경 변수를 설정합니다.

   ```bash
   cp .env.example .env
   ```
2. **의존성 설치**
   - Python 가상환경을 생성한 후, requirements.txt 파일을 이용해 필요한 패키지를 설치합니다.

   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **백엔드 서버 실행**
   - backend 디렉토리에서 FastAPI 애플리케이션을 실행합니다.

   ```
   uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```
4. **프론트엔드 실행**
   - 별도의 터미널에서 frontend 디렉토리 내의 streamlit_app.py를 실행합니다.

   ```
   streamlit run frontend/streamlit_app.py
   ```
5. **기능 체험**
   - 브라우저에서 백엔드 API 또는 프론트엔드(기본 제공하는 Streamlit UI)를 통해 AI Agent 데모를 체험합니다.