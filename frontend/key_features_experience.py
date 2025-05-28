import streamlit as st
import os
from datetime import datetime
import pytz

def key_features_experience():
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

    /* 기능 체험 페이지 스타일 */
    .features-container {{
        max-width: 1200px;
        margin: 40px auto;
        padding: 20px;
    }}

    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 30px;
        margin-top: 40px;
    }}

    .feature-card {{
        background: var(--card-bg);
        border-radius: 10px;
        padding: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: transform 0.3s ease;
    }}

    .feature-card:hover {{
        transform: translateY(-5px);
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

    .feature-list {{
        list-style: none;
        padding: 0;
        margin-top: 15px;
    }}

    .feature-list li {{
        margin-bottom: 10px;
        padding-left: 25px;
        position: relative;
    }}

    .feature-list li:before {{
        content: "✓";
        color: var(--primary-color);
        position: absolute;
        left: 0;
    }}
    </style>
    """, unsafe_allow_html=True)

    # 기능 체험 컨텐츠
    st.markdown("""
    <div class="features-container">
        <h1 class="intro-title">핵심 기능 체험</h1>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-chart-line"></i>
                </div>
                <h2 class="feature-title">실시간 시장 분석</h2>
                <p class="feature-description">AI Agent가 실시간으로 주식 시장을 분석하고 투자 기회를 찾아냅니다.</p>
                <ul class="feature-list">
                    <li>실시간 가격 모니터링</li>
                    <li>시장 동향 분석</li>
                    <li>투자 기회 탐색</li>
                </ul>
            </div>
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-robot"></i>
                </div>
                <h2 class="feature-title">AI 기반 투자 추천</h2>
                <p class="feature-description">머신러닝 알고리즘을 활용한 맞춤형 투자 추천을 제공합니다.</p>
                <ul class="feature-list">
                    <li>개인화된 포트폴리오</li>
                    <li>리스크 분석</li>
                    <li>수익률 예측</li>
                </ul>
            </div>
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-comments"></i>
                </div>
                <h2 class="feature-title">자연어 상담</h2>
                <p class="feature-description">일상적인 대화처럼 투자 관련 질문에 답변합니다.</p>
                <ul class="feature-list">
                    <li>24/7 상담 가능</li>
                    <li>맞춤형 투자 조언</li>
                    <li>투자 용어 설명</li>
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