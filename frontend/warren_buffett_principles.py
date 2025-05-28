import streamlit as st
import os
from datetime import datetime
import pytz

def warren_buffett_principles():
    # CSS 스타일 로드
    with open(os.path.join(os.path.dirname(__file__), 'resources/css/styles.css'), 'r') as f:
        css_content = f.read()
    
    st.markdown(f"""
    <style>
    {css_content}
    
    /* Streamlit 컨테이너 리셋 */
    .stApp,
    [data-testid="stAppViewContainer"],
    .main,
    .main .block-container {{
        margin: 0 !important;
        padding: 0 !important;
        padding-top: 0 !important;
        max-width: none !important;
        width: 100% !important;
    }}
    
    /* 헤더 제거 */
    header[data-testid="stHeader"],
    .stDeployButton {{
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
    }}

    /* 투자 원칙 페이지 스타일 */
    .principles-container {{
        max-width: 1000px;
        margin: 40px auto;
        padding: 20px;
    }}

    .principle-card {{
        background: var(--card-bg);
        border-radius: 10px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}

    .principle-title {{
        color: var(--primary-color);
        font-size: 1.8em;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 15px;
    }}

    .principle-icon {{
        font-size: 1.5em;
        color: var(--primary-color);
    }}

    .principle-content {{
        color: var(--text-color);
        line-height: 1.8;
    }}

    .principle-quote {{
        font-style: italic;
        color: var(--primary-color);
        border-left: 4px solid var(--primary-color);
        padding-left: 20px;
        margin: 20px 0;
    }}

    .principle-list {{
        list-style: none;
        padding: 0;
        margin-top: 20px;
    }}

    .principle-list li {{
        margin-bottom: 15px;
        padding-left: 30px;
        position: relative;
    }}

    .principle-list li:before {{
        content: "•";
        color: var(--primary-color);
        position: absolute;
        left: 10px;
        font-size: 1.5em;
    }}
    </style>
    """, unsafe_allow_html=True)

    # 투자 원칙 컨텐츠
    st.markdown("""
    <div class="principles-container">
        <h1 class="intro-title">워렌 버핏의 투자 원칙</h1>
        <div class="principle-card">
            <h2 class="principle-title">
                <i class="fas fa-book principle-icon"></i>
                가치 투자
            </h2>
            <div class="principle-content">
                <p>워렌 버핏의 가장 핵심적인 투자 원칙은 가치 투자입니다. 기업의 내재가치를 분석하고, 시장가격이 내재가치보다 낮을 때 투자하는 전략입니다.</p>
                <div class="principle-quote">
                    "가격은 당신이 지불하는 것이고, 가치는 당신이 얻는 것이다."
                </div>
                <ul class="principle-list">
                    <li>기업의 재무제표 분석</li>
                    <li>경제적 해자(Moat) 평가</li>
                    <li>안전마진 확보</li>
                </ul>
            </div>
        </div>
        <div class="principle-card">
            <h2 class="principle-title">
                <i class="fas fa-chart-pie principle-icon"></i>
                장기 투자
            </h2>
            <div class="principle-content">
                <p>단기적인 시장 변동에 흔들리지 않고, 우수한 기업에 장기적으로 투자하는 것을 강조합니다.</p>
                <div class="principle-quote">
                    "우리의 선호하는 보유 기간은 영원이다."
                </div>
                <ul class="principle-list">
                    <li>복리 효과 활용</li>
                    <li>거래 비용 최소화</li>
                    <li>세금 효율성 확보</li>
                </ul>
            </div>
        </div>
        <div class="principle-card">
            <h2 class="principle-title">
                <i class="fas fa-shield-alt principle-icon"></i>
                리스크 관리
            </h2>
            <div class="principle-content">
                <p>투자에서 가장 중요한 것은 원금을 지키는 것입니다. 리스크를 철저히 관리하고 분산 투자를 통해 안정적인 수익을 추구합니다.</p>
                <div class="principle-quote">
                    "규칙 1: 절대 돈을 잃지 마라. 규칙 2: 규칙 1을 절대 잊지 마라."
                </div>
                <ul class="principle-list">
                    <li>포트폴리오 분산</li>
                    <li>리스크 한도 설정</li>
                    <li>투자 기회 선별</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 푸터
    kst = datetime.now(pytz.timezone('Asia/Seoul'))
    formatted_time = kst.strftime('%Y-%m-%d %H:%M:%S')
    
    st.markdown(f"""
    <footer class="static-footer">
        <p>&copy; 2025 AI Agent Stock Analysis Demo. All Rights Reserved. (KST: {formatted_time})</p>
    </footer>
    """, unsafe_allow_html=True)

    # Font Awesome 추가
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    """, unsafe_allow_html=True) 