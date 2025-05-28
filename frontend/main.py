import streamlit as st
from ai_agent_introduction import ai_agent_introduction
from key_features_experience import key_features_experience
from warren_buffett_principles import warren_buffett_principles
from login import login
from signup import signup
from utils import get_recommendations, apply_page_styles
import os
from datetime import datetime
import pytz
from start_demo_dynamic import start_demo_dynamic

def main():
    # 페이지 설정
    st.set_page_config(
        page_title="AI Agent Stock Analysis",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # CSS 스타일 로드
    with open(os.path.join(os.path.dirname(__file__), 'resources/css/styles.css'), 'r') as f:
        css_content = f.read()
    
    # apply_page_styles()

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

    /* 메인 페이지 스타일 */
    .hero-section {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80');
        background-size: cover;
        background-position: center;
        color: white;
        text-align: center;
        padding: 100px 20px;
    }}

    .hero-title {{
        font-size: 3em;
        margin-bottom: 20px;
    }}

    .hero-description {{
        font-size: 1.2em;
        margin-bottom: 40px;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        text-align: center;
    }}

    .cta-button {{
        display: inline-block;
        background: var(--primary-color);
        color: white;
        padding: 15px 30px;
        border-radius: 5px;
        text-decoration: none;
        font-size: 1.2em;
        transition: background-color 0.3s ease;
    }}

    .cta-button:hover {{
        background: var(--primary-hover);
    }}

    .features-section {{
        padding: 80px 20px;
        background: var(--bg-light);
    }}

    .section-title {{
        text-align: center;
        color: var(--primary-color);
        font-size: 2.5em;
        margin-bottom: 50px;
    }}

    .features-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 30px;
        max-width: 1200px;
        margin: 0 auto;
    }}

    .feature-box {{
        background: var(--card-bg);
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}

    .feature-icon {{
        font-size: 2.5em;
        color: var(--primary-color);
        margin-bottom: 20px;
    }}

    .feature-title {{
        color: var(--primary-color);
        font-size: 1.5em;
        margin-bottom: 15px;
    }}

    .feature-description {{
        color: var(--text-color);
        line-height: 1.6;
    }}

    /* 네비게이션 링크 스타일 */
    nav {{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 18px;
        margin-top: 20px;
    }}
    .nav-link {{
        cursor: pointer;
        text-decoration: none;
        color: var(--text-color);
        transition: color 0.3s ease;
        margin: 0 10px;
        font-size: 1.1em;
    }}
    .nav-link:hover {{
        color: var(--primary-color);
    }}
    .nav-link.active {{
        color: var(--primary-color);
        font-weight: bold;
        border-bottom: 2px solid var(--primary-color);
    }}
    /* 상단 여백 제거 */
    .stApp {{ padding-top: 0 !important; }}
    .block-container {{ padding-top: 0rem !important; margin-top: 0rem !important; }}
    </style>
    """, unsafe_allow_html=True)

    # 쿼리 파라미터로 현재 페이지 결정
    query_params = st.query_params
    page = query_params.get("page", ["홈"])
    if isinstance(page, list):
        page = page[0]

    # st.write(f"현재 page 값: '{page}'")

    # 네비게이션 메뉴 (HTML <a> 링크)
    nav_html = f'''
    <header class="static-header">
        <div class="container" style="text-align:center;">
            <a class="nav-link{{' active' if page=='홈' else ''}}" href="/?page=홈" style="font-weight:bold;"><i class="fas fa-brain"></i> AI Stocks</a>
            <nav style="margin-top:20px;">
                <a class="nav-link{{' active' if page=='AI Agent 소개' else ''}}" href="/?page=AI%20Agent%20소개" target="_self">AI Agent 소개</a>
                <a class="nav-link{{' active' if page=='핵심 기능' else ''}}" href="/?page=핵심%20기능" target="_self">핵심 기능</a>
                <a class="nav-link{{' active' if page=='투자 원칙' else ''}}" href="/?page=투자%20원칙" target="_self">투자 원칙</a>
                <a class="nav-link{{' active' if page=='데모 체험' else ''}}" href="/?page=데모%20체험" target="_self">데모 체험</a>
                <a class="nav-link{{' active' if page=='로그인' else ''}}" href="/?page=로그인" target="_self">로그인</a>
                <a class="nav-link{{' active' if page=='회원가입' else ''}}" href="/?page=회원가입" target="_self">회원가입</a>
            </nav>
        </div>
    </header>
    '''
    st.markdown(nav_html, unsafe_allow_html=True)
    st.markdown("---")

    # 페이지 라우팅
    if page == "홈":
        st.markdown("""
        <div class="hero-section">
            <h1 class="hero-title">AI Agent로 시작하는 스마트 투자</h1>
            <div class="hero-description">
                인공지능 기반의 투자 분석 시스템으로 더 나은 투자 결정을 내리세요.<br>
                실시간 시장 분석, 맞춤형 포트폴리오 추천, 전문가 수준의 투자 조언을 제공합니다.
            </div>
            <a class="cta-button" href="/?page=데모%20체험" style="margin-top:30px;display:inline-block;" target="_self">지금 시작하기</a>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="features-section">
            <h2 class="section-title">주요 기능</h2>
            <div class="features-grid">
                <div class="feature-box">
                    <div class="feature-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <h3 class="feature-title">실시간 시장 분석</h3>
                    <p class="feature-description">
                        AI Agent가 실시간으로 주식 시장을 분석하고 투자 기회를 찾아냅니다.
                    </p>
                </div>
                <div class="feature-box">
                    <div class="feature-icon">
                        <i class="fas fa-robot"></i>
                    </div>
                    <h3 class="feature-title">AI 기반 투자 추천</h3>
                    <p class="feature-description">
                        머신러닝 알고리즘을 활용한 맞춤형 투자 추천을 제공합니다.
                    </p>
                </div>
                <div class="feature-box">
                    <div class="feature-icon">
                        <i class="fas fa-comments"></i>
                    </div>
                    <h3 class="feature-title">자연어 상담</h3>
                    <p class="feature-description">
                        일상적인 대화처럼 투자 관련 질문에 답변합니다.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        kst = datetime.now(pytz.timezone('Asia/Seoul'))
        formatted_time = kst.strftime('%Y-%m-%d %H:%M:%S')
        st.markdown(f"""
        <footer class="static-footer">
            <p>&copy; 2025 AI Agent Stock Analysis Demo. All Rights Reserved. (KST: {formatted_time})</p>
        </footer>
        """, unsafe_allow_html=True)
    elif page == "AI Agent 소개":
        ai_agent_introduction()
    elif page == "핵심 기능":
        key_features_experience()
    elif page == "투자 원칙":
        warren_buffett_principles()
    elif page == "데모 체험":
        start_demo_dynamic()
    elif page == "로그인":
        login()
    elif page == "회원가입":
        signup()

    # Font Awesome 추가
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    """, unsafe_allow_html=True)

    # JavaScript 추가
    st.markdown("""
    <script>
    window.streamlit = {
        setComponentValue: function(value) {
            window.parent.postMessage({
                type: "streamlit:setComponentValue",
                value: value
            }, "*");
        }
    };
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()