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

### 기본 실행 순서

1. **환경 설정**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **환경 변수 설정**
   - 백엔드: `backend/.env` 파일 생성 (아래 "환경 변수 설정" 섹션 참조)
   - 프론트엔드: `frontend/vue-project/.env` 또는 `.env.local` 파일 생성

3. **백엔드 서버 실행**

   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **프론트엔드 실행**

   ```bash
   cd frontend/vue-project
   npm install
   npm run dev
   ```

5. **관리자 계정 생성** (선택사항)

   ```bash
   cd backend
   python create_admin.py
   ```

### 빠른 시작 (Quick Start)

개발환경에 따라 적절한 방법을 선택하세요:

- **로컬 개발**: 기본 설정으로 실행 → `http://localhost:5173`
- **Azure VM**: `.env.local` 파일 생성 후 실행 → `http://[VM-IP]:3000`

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

## 개발환경별 설정 가이드

### 로컬 개발 환경 (Windows/Mac/Linux)

로컬에서 개발하는 경우 기본 설정으로 실행 가능합니다.

**프론트엔드 실행:**
```bash
cd frontend/vue-project
npm install
npm run dev  # http://localhost:5173에서 실행
```

**백엔드 실행:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**브라우저 접속:** `http://localhost:5173`

---

### Azure VM 환경

Azure VM에서 개발하고 로컬 PC 브라우저로 접속하는 경우 네트워크 설정이 필요합니다.

#### 1. 환경변수 기반 Vite 설정

**기본 환경변수 파일 (`.env`)**: 로컬 개발 환경용 기본값
```env
# Vite 환경변수 설정 - 로컬 개발 환경용 기본값
VITE_API_TARGET=http://localhost:8000
VITE_DEV_PORT=5173
VITE_DEV_HOST=localhost
```

**Azure VM 환경변수 파일 (`.env.local`)**: VM 환경용 설정 (Git에서 제외됨)
```env
# Azure VM 환경용 설정
# 이 파일은 .gitignore에 추가되어 공개되지 않습니다
VITE_API_TARGET=http://localhost:8000  # VM 내부에서는 localhost 사용
VITE_DEV_PORT=3000
VITE_DEV_HOST=0.0.0.0
```

**Vite 설정 파일**: 환경변수를 자동으로 읽어서 적용
```javascript
// frontend/vue-project/vite.config.js
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ mode }) => {
  // 환경변수 로드
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [vue()],
    server: {
      port: parseInt(env.VITE_DEV_PORT) || 5173,
      host: env.VITE_DEV_HOST || 'localhost',
      open: env.VITE_DEV_HOST === '0.0.0.0' ? false : true, // 외부 호스트일 때는 브라우저 자동 열기 비활성화
      proxy: {
        '/api': {
          target: env.VITE_API_TARGET || 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        }
      }
    }
  }
})
```

#### 2. Azure 네트워크 보안 그룹 설정

Azure Portal에서 VM의 네트워크 보안 그룹에 다음 포트를 허용:
- **3000번 포트**: 프론트엔드 (Vue.js)
- **8000번 포트**: 백엔드 (FastAPI) - 선택사항

#### 3. 실행 순서

**백엔드 실행:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**프론트엔드 실행:**
```bash
cd frontend/vue-project
npm run dev  # 3000번 포트에서 실행
```

**브라우저 접속:** `http://[VM-PUBLIC-IP]:3000`

#### 4. 동작 원리

```
[로컬 PC 브라우저] → [Azure VM:3000 (Vue)] → [VM 내부 localhost:8000 (FastAPI)]
```

- 브라우저에서 Azure VM의 3000번 포트로 접속
- Vue 앱의 프록시가 API 요청을 같은 VM 내의 localhost:8000으로 전달
- 이렇게 하면 CORS 및 네트워크 문제를 해결할 수 있음

---

### 환경 변수 설정

개발 PC 변경 시 환경 변수 파일을 새로 생성해야 합니다.

#### 백엔드 환경 변수

`backend/.env` 파일 생성:

```env
# JWT 설정
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Azure OpenAI 설정
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_ENDPOINT=your-azure-openai-endpoint
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=your-deployment-name

# 데이터베이스 설정
DATABASE_URL=sqlite+aiosqlite:///./test.db

# 외부 API 설정 (선택사항)
OPEN_DART_API_KEY=your-opendart-api-key
KRX_API_KEY=your-krx-api-key
```

#### 프론트엔드 환경 변수

`frontend/vue-project/.env` 또는 `.env.local` 파일 생성:

```env
# Vite 환경 변수는 VITE_ 접두사 필요
VITE_API_URL=http://localhost:8000
```

---

### 트러블슈팅

#### 1. "ECONNREFUSED" 에러

**증상:** 프론트엔드에서 백엔드 API 호출 시 연결 거부 에러

**해결 방법:**
- 백엔드 서버가 정상 실행 중인지 확인
- 프록시 설정이 올바른지 확인
- Azure VM 환경에서는 위의 네트워크 설정 적용

#### 2. "Invalid HTTP request" 경고

**증상:** 백엔드 로그에 "Invalid HTTP request" 경고 메시지

**해결 방법:**
- 이는 정상적인 프록시 요청이므로 무시해도 됨
- 실제 API 요청이 정상 처리되는지 확인

#### 4. 로그인 기능 테스트 문제

**증상:** 로그인 시도 시 오류 발생

**해결 방법:**
- 백엔드 서버가 정상 실행 중인지 확인
- 관리자 계정이 생성되어 있는지 확인:
  ```bash
  cd backend
  python create_admin.py
  ```
- 브라우저 개발자 도구에서 네트워크 탭으로 API 요청 상태 확인

#### 5. 파일 권한 문제

**증상:** 환경 변수 파일 읽기 오류

**해결 방법:**
- 환경 변수 파일 권한 설정:
  ```bash
  chmod 600 .env
  chmod 600 .env.local
  ```

---

## 프로젝트 상태

**현재 구현 완료된 기능:**
- ✅ 백엔드 FastAPI 서버 (8000번 포트)
- ✅ 프론트엔드 Vue.js 앱 (환경별 포트 설정)
- ✅ JWT 기반 인증 시스템
- ✅ 환경변수 기반 설정 관리
- ✅ Azure VM 네트워크 호환성
- ✅ AI Agent 투자 분석 기능

**개발 환경 지원:**
- ✅ 로컬 개발 환경 (localhost:5173)
- ✅ Azure VM 환경 (VM-IP:3000)
- ✅ 환경변수 기반 자동 설정

**보안 설정:**
- ✅ 환경변수 파일 Git 제외 설정
- ✅ JWT 토큰 기반 인증
- ✅ CORS 정책 적용