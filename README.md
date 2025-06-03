# Stock Analysis API

주식 분석을 위한 REST API 서비스입니다.

## 기능

- 주식 시장 데이터 수집 및 분석
- 재무제표 분석
- 투자 추천
- ESG 분석
- 리스크 분석

## 설치

1. 저장소 클론
```bash
git clone https://github.com/yourusername/stock-analysis-api.git
cd stock-analysis-api
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
.\venv\Scripts\activate  # Windows
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
`.env` 파일을 생성하고 다음 변수들을 설정합니다:
```
DATABASE_URL=sqlite:///./stock_analysis.db
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key-here
FSS_API_KEY=your-fss-api-key-here
DART_API_KEY=your-dart-api-key-here
```

## 실행

```bash
uvicorn backend.main:app --reload
```

## API 문서

서버가 실행되면 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 라이선스

MIT