from typing import Type, Dict, Any, List
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import json
import random
from datetime import datetime, timedelta

class NewsToolInput(BaseModel):
    """Input for NewsTool"""
    stock_symbol: str = Field(description="Stock symbol or company name to search news for")
    days_back: int = Field(default=30, description="Number of days to look back for news (default: 30)")

class NewsTool(BaseTool):
    """
    종목 관련 뉴스 수집 및 감성 분석 도구
    """
    name: str = "news_sentiment_analyzer"
    description: str = """
    지정된 종목의 최근 뉴스를 수집하고 감성 분석을 수행합니다.
    뉴스의 긍정/부정/중립 감성을 분석하여 투자 심리를 파악합니다.
    
    입력: stock_symbol (종목코드 또는 회사명), days_back (조회 기간)
    출력: 뉴스 감성 점수와 주요 뉴스 요약
    """
    args_schema: Type[BaseModel] = NewsToolInput
    
    def _get_company_name(self, symbol: str) -> str:
        """종목코드에서 회사명 추출"""
        company_names = {
            "005930": "삼성전자",
            "000660": "SK하이닉스", 
            "035420": "NAVER",
            "005380": "현대차",
            "006400": "삼성SDI",
            "207940": "삼성바이오로직스",
            "068270": "셀트리온",
            "035720": "카카오",
            "051910": "LG화학",
            "012330": "현대모비스"
        }
        return company_names.get(symbol, f"기업_{symbol}")
    
    def _generate_mock_news(self, company_name: str, days_back: int) -> List[Dict[str, Any]]:
        """
        모의 뉴스 데이터 생성 (실제로는 네이버 뉴스, 한경닷컴 등의 API 사용)
        """
        # 회사별 고정 시드로 일관된 뉴스 생성
        random.seed(hash(company_name) % 1000)
        
        news_templates = {
            "positive": [
                f"{company_name}, 3분기 실적 시장 예상치 상회",
                f"{company_name}, 신제품 출시로 매출 급증 전망",
                f"{company_name}, 해외 시장 진출 확대로 성장 가속화",
                f"{company_name}, 기술 혁신으로 업계 선도",
                f"{company_name}, ESG 경영으로 지속가능성 강화"
            ],
            "negative": [
                f"{company_name}, 원자재 가격 상승으로 수익성 악화 우려",
                f"{company_name}, 경쟁 심화로 시장점유율 하락",
                f"{company_name}, 규제 강화로 사업 리스크 증가",
                f"{company_name}, 글로벌 경기둔화 영향으로 실적 부진",
                f"{company_name}, 공급망 차질로 생산 차질 발생"
            ],
            "neutral": [
                f"{company_name}, 정기 주주총회 개최 예정",
                f"{company_name}, 신규 임원진 선임 발표",
                f"{company_name}, 배당금 지급 일정 공지",
                f"{company_name}, 업계 동향 및 전망 발표",
                f"{company_name}, 사회공헌 활동 확대 계획"
            ]
        }
        
        news_list = []
        num_news = min(10, days_back // 3)  # 3일에 1개 정도의 뉴스
        
        for i in range(num_news):
            # 감성 분포: 긍정 40%, 중립 40%, 부정 20%
            sentiment_type = random.choices(
                ["positive", "neutral", "negative"], 
                weights=[0.4, 0.4, 0.2]
            )[0]
            
            title = random.choice(news_templates[sentiment_type])
            date = datetime.now() - timedelta(days=random.randint(1, days_back))
            
            # 감성 점수 (0-100, 50이 중립)
            if sentiment_type == "positive":
                sentiment_score = random.uniform(65, 90)
            elif sentiment_type == "negative":
                sentiment_score = random.uniform(10, 35)
            else:
                sentiment_score = random.uniform(45, 55)
            
            news_list.append({
                "title": title,
                "date": date.strftime("%Y-%m-%d"),
                "sentiment_type": sentiment_type,
                "sentiment_score": round(sentiment_score, 1),
                "source": random.choice(["한국경제", "매일경제", "이데일리", "연합뉴스", "뉴스1"])
            })
        
        return sorted(news_list, key=lambda x: x["date"], reverse=True)
    
    def _analyze_overall_sentiment(self, news_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """전체 뉴스의 종합 감성 분석"""
        if not news_list:
            return {
                "overall_score": 50.0,
                "sentiment": "중립",
                "confidence": 0.0
            }
        
        # 가중 평균 계산 (최근 뉴스일수록 높은 가중치)
        total_weighted_score = 0
        total_weight = 0
        
        for i, news in enumerate(news_list):
            weight = 1.0 / (i + 1)  # 최근 뉴스일수록 높은 가중치
            total_weighted_score += news["sentiment_score"] * weight
            total_weight += weight
        
        overall_score = total_weighted_score / total_weight
        
        # 감성 분류
        if overall_score >= 60:
            sentiment = "긍정적"
            emoji = "😊"
        elif overall_score <= 40:
            sentiment = "부정적"
            emoji = "😟"
        else:
            sentiment = "중립적"
            emoji = "😐"
        
        # 신뢰도 계산 (뉴스 수가 많을수록 높은 신뢰도)
        confidence = min(1.0, len(news_list) / 10)
        
        return {
            "overall_score": round(overall_score, 1),
            "sentiment": sentiment,
            "emoji": emoji,
            "confidence": round(confidence, 2)
        }
    
    def _get_investment_insight(self, sentiment_analysis: Dict[str, Any], company_name: str) -> str:
        """감성 분석 결과를 바탕으로 투자 인사이트 제공"""
        score = sentiment_analysis["overall_score"]
        sentiment = sentiment_analysis["sentiment"]
        confidence = sentiment_analysis["confidence"]
        
        if score >= 70 and confidence >= 0.7:
            return f"📈 {company_name}에 대한 뉴스 감성이 매우 긍정적입니다. 투자 심리 개선으로 주가 상승 모멘텀 기대"
        elif score >= 60:
            return f"📊 {company_name}에 대한 뉴스 감성이 긍정적입니다. 펀더멘털 개선 신호로 해석 가능"
        elif score <= 30 and confidence >= 0.7:
            return f"📉 {company_name}에 대한 뉴스 감성이 매우 부정적입니다. 단기 조정 압력 예상"
        elif score <= 40:
            return f"⚠️ {company_name}에 대한 뉴스 감성이 부정적입니다. 리스크 요인 주의 필요"
        else:
            return f"➡️ {company_name}에 대한 뉴스 감성이 중립적입니다. 재료 부족으로 횡보 전망"
    
    def _run(self, stock_symbol: str, days_back: int = 30) -> str:
        """도구 실행 메인 로직"""
        try:
            company_name = self._get_company_name(stock_symbol)
            
            # 뉴스 데이터 수집 (실제로는 뉴스 API 호출)
            news_list = self._generate_mock_news(company_name, days_back)
            
            # 감성 분석
            sentiment_analysis = self._analyze_overall_sentiment(news_list)
            
            # 투자 인사이트 생성
            investment_insight = self._get_investment_insight(sentiment_analysis, company_name)
            
            # 주요 뉴스 요약 (상위 3개)
            top_news = news_list[:3]
            
            result = {
                "company": company_name,
                "symbol": stock_symbol,
                "analysis_period": f"최근 {days_back}일",
                "sentiment_analysis": sentiment_analysis,
                "investment_insight": investment_insight,
                "news_count": len(news_list),
                "top_news": top_news,
                "summary": f"{company_name}의 최근 {days_back}일간 뉴스 감성 점수는 {sentiment_analysis['overall_score']}점({sentiment_analysis['sentiment']})입니다."
            }
            
            return json.dumps(result, ensure_ascii=False, indent=2)
            
        except Exception as e:
            return f"뉴스 분석 중 오류 발생: {str(e)}"
