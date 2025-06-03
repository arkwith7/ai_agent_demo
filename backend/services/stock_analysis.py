from typing import List, Dict, Any, TYPE_CHECKING, Optional
from datetime import datetime
if TYPE_CHECKING:
    from core.agent import StockAnalysisAgent
from schemas.analysis import StockRecommendation, StockAnalysis
from services.data_providers.opendart_api import OpenDARTProvider, opendart_provider
from services.data_providers.financial_services_stock import FinancialServicesStockProvider, fss_provider
from services.logger import LoggerService
import pandas as pd
import os
import logging

# 로그 디렉토리 생성
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log')
os.makedirs(log_dir, exist_ok=True)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(log_dir, 'stock_analysis.log'))
    ]
)

logger = logging.getLogger(__name__)
logger.info(f"로그 디렉토리 생성/확인: {log_dir}")

class StockAnalysisService:
    _instance = None
    
    def __new__(cls, agent=None):
        if cls._instance is None:
            cls._instance = super(StockAnalysisService, cls).__new__(cls)
            cls._instance.agent = agent
            cls._instance.opendart = opendart_provider
            cls._instance.fss = fss_provider
            cls._instance.logger = LoggerService()
            cls._instance.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'market_data')
            os.makedirs(cls._instance.data_dir, exist_ok=True)
            logger.info(f"데이터 디렉토리 생성/확인: {cls._instance.data_dir}")
        return cls._instance

    def __init__(self, agent=None):
        if not hasattr(self, 'initialized'):
            self.agent = agent
            self.opendart = opendart_provider
            self.fss = fss_provider
            self.logger = LoggerService()
            self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'market_data')
            os.makedirs(self.data_dir, exist_ok=True)
            logger.info(f"StockAnalysisService 초기화 완료")
            self.initialized = True

    async def collect_financial_data(self, stock_code: str) -> Dict[str, Any]:
        """
        OpenDART API를 통해 재무 데이터를 수집합니다.
        """
        try:
            self.logger.info(f"Collecting financial data for stock: {stock_code}")
            financial_statements = await self.opendart.get_financial_statements(stock_code, 3)  # 최근 3년 데이터
            company_info = await self.opendart.get_company_info(stock_code)
            
            return {
                "company_info": company_info,
                "financial_statements": financial_statements,
                "dividend_info": await self.opendart.get_major_shareholders(stock_code)
            }
        except Exception as e:
            self.logger.error(f"Error collecting financial data for {stock_code}: {str(e)}")
            raise

    def _generate_recommendation_reason(self, criteria_scores: Dict[str, float], total_score: float) -> str:
        """추천 이유를 생성합니다."""
        reasons = []
        
        # 버핏 기준 기반 추천 이유
        if criteria_scores:
            top_criteria = sorted(criteria_scores.items(), key=lambda x: x[1], reverse=True)[:2]
            for criterion, score in top_criteria:
                if score >= 80:
                    reasons.append(f"{criterion} 점수가 매우 높습니다 ({score}점)")
        
        # 기본 추천 이유
        if not reasons:
            if total_score >= 80:
                reasons.append("종합 평가가 매우 우수합니다")
            elif total_score >= 70:
                reasons.append("종합 평가가 우수합니다")
            else:
                reasons.append("안정적인 투자 대상입니다")
        
        return " | ".join(reasons)

    async def get_recommendations(self, query: str = "", max_results: int = 5) -> List[StockRecommendation]:
        """
        주식 추천 목록을 반환합니다.
        """
        try:
            self.logger.info("시장 데이터 수집 시작")
            # 1. 시장 데이터 수집
            market_data = await self.agent.collect_market_data("")
            
            self.logger.info(f"수집된 시장 데이터: {len(market_data)}개 종목")
            
            # 2. 기본 점수 계산 (재무 데이터 없이)
            initial_scores = []
            for stock_data in market_data:
                try:
                    # 기본 점수 계산 (시장 데이터만으로)
                    basic_score = self._calculate_basic_score(stock_data)
                    initial_scores.append({
                        'stock_data': stock_data,
                        'basic_score': basic_score
                    })
                except Exception as e:
                    self.logger.error(f"기본 점수 계산 중 오류 발생 (종목 {stock_data['srtnCd']}): {str(e)}")
                    continue
            
            # 3. 기본 점수로 상위 20개 종목 선별
            initial_scores.sort(key=lambda x: x['basic_score'], reverse=True)
            top_20_stocks = initial_scores[:20]
            
            # 4. 선별된 종목에 대해서만 재무 데이터 조회 및 상세 분석
            recommendations = []
            for stock in top_20_stocks:
                try:
                    stock_data = stock['stock_data']
                    self.logger.info(f"종목 {stock_data['srtnCd']} 상세 분석 시작")
                    
                    # 재무 데이터 조회
                    financial_data = await self.collect_financial_data(stock_data['srtnCd'])
                    
                    # 버핏 기준 평가
                    criteria_scores = self.evaluate_buffett_criteria({
                        "market_data": stock_data,
                        "financial_data": financial_data
                    })
                    
                    # 종합 점수 계산
                    total_score = sum(criteria_scores.values()) / len(criteria_scores)
                    
                    # 추천 이유 생성
                    reason = self._generate_recommendation_reason(criteria_scores, total_score)
                    
                    recommendations.append(StockRecommendation(
                        name=stock_data['itmsNm'],
                        market=stock_data.get('mrktCtg', 'KOSPI'),
                        currentPrice=float(stock_data['clpr']),
                        changeRate=float(stock_data.get('fltRt', 0)),
                        volume=float(stock_data.get('trqu', 0)),
                        marketCap=float(stock_data['mrktTotAmt']),
                        reason=reason,
                        criteria_scores=criteria_scores,
                        total_score=total_score
                    ))
                    self.logger.info(f"종목 {stock_data['srtnCd']} 분석 완료")
                except Exception as e:
                    self.logger.error(f"종목 {stock_data['srtnCd']} 분석 중 오류 발생: {str(e)}")
                    continue
            
            # 5. 최종 점수로 정렬하고 상위 5개만 반환
            recommendations.sort(key=lambda x: x.total_score, reverse=True)
            final_recommendations = recommendations[:5]
            self.logger.info(f"추천 종목 {len(final_recommendations)}개 생성 완료")
            
            return final_recommendations
        except Exception as e:
            self.logger.error(f"주식 추천 목록 생성 중 오류 발생: {str(e)}")
            raise

    def _calculate_basic_score(self, stock_data: Dict[str, Any]) -> float:
        """기본 점수를 계산합니다 (재무 데이터 없이)."""
        try:
            score = 0.0
            
            # 1. 가격 점수 (1,000원 ~ 1,000,000원 범위 내)
            price = float(stock_data.get('현재가', 0))
            if 1000 <= price <= 1000000:
                price_score = 100 - (abs(price - 50000) / 50000 * 100)  # 5만원에 가까울수록 높은 점수
                score += price_score * 0.3
                logger.debug(f"가격 점수: {price_score:.2f}")
            
            # 2. 등락률 점수 (-5% ~ +15% 범위 내)
            change_rate = float(stock_data.get('등락률', 0))
            if -5 <= change_rate <= 15:
                change_score = 100 - (abs(change_rate - 5) / 20 * 100)  # +5%에 가까울수록 높은 점수
                score += change_score * 0.3
                logger.debug(f"등락률 점수: {change_score:.2f}")
            
            # 3. 거래량 점수
            volume = float(stock_data.get('거래량', 0))
            if volume > 0:
                volume_score = min(100, volume / 1000000 * 100)  # 100만주 기준
                score += volume_score * 0.4
                logger.debug(f"거래량 점수: {volume_score:.2f}")
            
            logger.debug(f"종목 {stock_data.get('종목명', 'Unknown')} 최종 점수: {score:.2f}")
            return score
            
        except Exception as e:
            logger.error(f"기본 점수 계산 중 오류 발생: {str(e)}")
            return 0.0

    async def get_detailed_analysis(self, stock_code: str) -> StockAnalysis:
        """
        특정 종목에 대한 상세 분석을 반환합니다.
        """
        try:
            self.logger.info(f"종목 {stock_code} 상세 분석 시작")
            if self.agent is None:
                raise Exception("종목 분석 기능이 준비되지 않았습니다. 관리자에게 문의하세요.")
            # 1. 재무 데이터 조회
            financial_data = await self.agent.collect_financial_data(stock_code)
            
            # 2. 시장 데이터 조회
            market_data = await self.agent.collect_market_data(stock_code)
            
            # 3. 버핏 기준 평가
            criteria_scores = self.evaluate_buffett_criteria({
                "market_data": market_data[0] if market_data else {},
                "financial_data": financial_data
            })
            
            # 4. 종합 분석 결과 생성
            analysis = StockAnalysis(
                stock_code=stock_code,
                stock_name=financial_data['company_info']['corp_name'],
                current_price=float(market_data[0]['clpr']) if market_data else 0.0,
                market_cap=float(market_data[0]['mrktTotAmt']) if market_data else 0.0,
                criteria_scores=criteria_scores,
                total_score=sum(criteria_scores.values()) / len(criteria_scores),
                financial_data=financial_data,
                market_data=market_data
            )
            self.logger.info(f"종목 {stock_code} 상세 분석 완료")
            return analysis
        except Exception as e:
            self.logger.error(f"종목 상세 분석 중 오류 발생: {str(e)}")
            raise

    def evaluate_buffett_criteria(self, data: Dict[str, Any]) -> Dict[str, float]:
        """
        워렌 버핏의 투자 기준에 따라 종목을 평가합니다.
        """
        try:
            market_data = data.get("market_data", {})
            financial_data = data.get("financial_data", {})
            
            # 1. 시가총액 평가 (100점 만점)
            market_cap_score = self._evaluate_market_cap(float(market_data.get("mrktTotAmt", 0)))
            
            # 2. ROE 평가 (100점 만점)
            roe_score = self._evaluate_roe(financial_data.get("financial_statements", []))
            
            # 3. 이익률 평가 (100점 만점)
            profit_margin_score = self._evaluate_profit_margin(financial_data.get("financial_statements", []))
            
            # 4. 부채비율 평가 (100점 만점)
            debt_ratio_score = self._evaluate_debt_ratio(financial_data.get("financial_statements", []))
            
            # 5. 배당금 평가 (100점 만점)
            dividend_score = self._evaluate_dividend(financial_data.get("dividend_info", {}))
            
            # 6. 경영진 평가 (100점 만점)
            management_score = self._evaluate_management(financial_data.get("company_info", {}))
            
            return {
                "market_cap": market_cap_score,
                "roe": roe_score,
                "profit_margin": profit_margin_score,
                "debt_ratio": debt_ratio_score,
                "dividend": dividend_score,
                "management": management_score
            }
        except Exception as e:
            self.logger.error(f"버핏 기준 평가 중 오류 발생: {str(e)}")
            raise

    def _evaluate_market_cap(self, market_cap: float) -> float:
        """시가총액 평가"""
        # TODO: 실제 평가 로직 구현
        return 80.0

    def _evaluate_roe(self, financial_statements: List[Dict[str, Any]]) -> float:
        """ROE 평가"""
        # TODO: 실제 평가 로직 구현
        return 75.0

    def _evaluate_profit_margin(self, financial_statements: List[Dict[str, Any]]) -> float:
        """이익률 평가"""
        # TODO: 실제 평가 로직 구현
        return 70.0

    def _evaluate_debt_ratio(self, financial_statements: List[Dict[str, Any]]) -> float:
        """부채비율 평가"""
        # TODO: 실제 평가 로직 구현
        return 85.0

    def _evaluate_dividend(self, dividend_info: Dict[str, Any]) -> float:
        """배당금 평가"""
        # TODO: 실제 평가 로직 구현
        return 65.0

    def _evaluate_management(self, company_info: Dict[str, Any]) -> float:
        """경영진 평가"""
        # TODO: 실제 평가 로직 구현
        return 90.0

    async def collect_market_data(self) -> Dict[str, Any]:
        """시장 데이터를 수집하고 저장합니다."""
        try:
            logger.info("=== 시장 데이터 수집 시작 ===")
            
            # 시장 데이터 수집
            logger.info("금융위원회 API를 통해 시장 데이터 수집 중...")
            market_data = await self.fss.get_market_data()
            
            if market_data is None or market_data.empty:
                logger.error("시장 데이터를 가져오는데 실패했습니다.")
                raise Exception("시장 데이터를 가져오는데 실패했습니다.")
            
            logger.info(f"수집된 데이터: {len(market_data)}개 종목")
            
            # 데이터 저장
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"market_data_{timestamp}.csv"
            filepath = os.path.join(self.data_dir, filename)
            
            logger.info(f"데이터 저장 시작: {filepath}")
            market_data.to_csv(filepath, index=False, encoding='utf-8-sig')
            logger.info("데이터 저장 완료")
            
            # 데이터 샘플 로깅
            logger.info("\n=== 수집된 데이터 샘플 ===")
            sample_data = market_data.head(3)
            for _, row in sample_data.iterrows():
                logger.info(f"종목: {row['종목명']} ({row['종목코드']})")
                logger.info(f"현재가: {row['현재가']}원")
                logger.info(f"등락률: {row['등락률']}%")
                logger.info(f"거래량: {row['거래량']}주")
                logger.info("---")
            
            return {
                "success": True,
                "message": "시장 데이터 수집 완료",
                "filename": filename,
                "data_count": len(market_data)
            }
            
        except Exception as e:
            logger.error(f"데이터 수집 중 오류 발생: {str(e)}")
            raise Exception(f"데이터 수집 중 오류 발생: {str(e)}")

    async def get_recommendations_from_latest(self, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """최신 데이터를 기반으로 주식 추천을 생성합니다."""
        try:
            logger.info("=== 주식 추천 생성 시작 ===")
            
            # 최신 데이터 읽기
            logger.info("최신 시장 데이터 읽기 시작")
            market_data = await self.get_latest_market_data()
            
            if market_data is None or market_data.empty:
                logger.error("수집된 시장 데이터가 없습니다.")
                raise Exception("수집된 시장 데이터가 없습니다.")
            
            logger.info(f"읽어온 데이터: {len(market_data)}개 종목")
            
            # 기본 파라미터 설정
            if params is None:
                params = {}
            
            market_segment = params.get("market_segment", "KOSPI")
            min_score = params.get("min_score", 60)
            max_results = params.get("max_results", 5)
            
            logger.info(f"분석 파라미터: 시장={market_segment}, 최소점수={min_score}, 최대결과={max_results}")
            
            # 시장 구분 필터링
            if market_segment:
                market_data = market_data[market_data['시장구분'] == market_segment]
                logger.info(f"시장 필터링 후: {len(market_data)}개 종목")
            
            if market_data.empty:
                logger.error(f"{market_segment} 시장 데이터가 없습니다.")
                raise Exception(f"{market_segment} 시장 데이터가 없습니다.")
            
            # 점수 계산
            logger.info("종목별 점수 계산 시작")
            market_data['score'] = market_data.apply(self._calculate_basic_score, axis=1)
            
            # 점수 기준 필터링 및 정렬
            recommendations = market_data[market_data['score'] >= min_score].sort_values('score', ascending=False)
            logger.info(f"점수 {min_score} 이상 종목: {len(recommendations)}개")
            
            # 결과 제한
            recommendations = recommendations.head(max_results)
            
            # 결과 포맷팅 (추천 이유 포함)
            result = []
            for _, row in recommendations.iterrows():
                # 간단한 추천 이유 생성
                score = float(row['score'])
                if score >= 80:
                    reason = "종합 평가가 매우 우수합니다."
                elif score >= 70:
                    reason = "종합 평가가 우수합니다."
                else:
                    reason = "안정적인 투자 대상입니다."
                stock_info = {
                    "종목코드": row['종목코드'],
                    "종목명": row['종목명'],
                    "현재가": float(row['현재가']),
                    "등락률": float(row['등락률']),
                    "거래량": float(row['거래량']),
                    "시가총액": float(row['시가총액']),
                    "점수": score,
                    "reason": reason
                }
                result.append(stock_info)
                logger.info(f"추천 종목: {stock_info['종목명']} (점수: {stock_info['점수']:.2f}, 이유: {reason})")
            
            logger.info("=== 주식 추천 생성 완료 ===")
            return result
            
        except Exception as e:
            logger.error(f"추천 생성 중 오류 발생: {str(e)}")
            raise Exception(f"추천 생성 중 오류 발생: {str(e)}")

    async def get_latest_market_data(self) -> Optional[pd.DataFrame]:
        """가장 최근의 시장 데이터를 읽습니다."""
        try:
            logger.info("=== 최신 시장 데이터 읽기 시작 ===")
            
            # 데이터 디렉토리의 모든 CSV 파일 목록
            csv_files = [f for f in os.listdir(self.data_dir) if f.endswith('.csv')]
            logger.info(f"발견된 CSV 파일 수: {len(csv_files)}")
            
            if not csv_files:
                logger.error("수집된 시장 데이터가 없습니다.")
                raise Exception("수집된 시장 데이터가 없습니다.")
            
            # 파일명으로 정렬하여 가장 최근 파일 선택
            latest_file = sorted(csv_files)[-1]
            filepath = os.path.join(self.data_dir, latest_file)
            logger.info(f"최신 데이터 파일: {latest_file}")
            
            # CSV 파일 읽기
            logger.info("CSV 파일 읽기 시작")
            df = pd.read_csv(filepath, encoding='utf-8-sig')
            
            if df.empty:
                logger.error("데이터 파일이 비어있습니다.")
                raise Exception("데이터 파일이 비어있습니다.")
            
            logger.info(f"데이터 읽기 완료: {len(df)}개 종목")
            logger.info("=== 최신 시장 데이터 읽기 완료 ===")
            
            return df
            
        except Exception as e:
            logger.error(f"데이터 읽기 중 오류 발생: {str(e)}")
            raise Exception(f"데이터 읽기 중 오류 발생: {str(e)}")

# 싱글톤 인스턴스 생성
stock_analysis = StockAnalysisService(None)  # agent는 나중에 설정 