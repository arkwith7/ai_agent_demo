import streamlit as st
import os
from datetime import datetime
import pytz

def ai_agent_introduction():
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

    /* 소개 페이지 스타일 */
    .intro-container {{
        max-width: 800px;
        margin: 40px auto;
        padding: 20px;
        background: var(--card-bg);
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}

    .intro-title {{
        color: var(--primary-color);
        font-size: 2em;
        margin-bottom: 20px;
        text-align: center;
    }}

    .intro-content {{
        color: var(--text-color);
        line-height: 1.8;
        margin-bottom: 30px;
    }}

    .intro-section {{
        margin-bottom: 40px;
    }}

    .intro-section h2 {{
        color: var(--primary-color);
        margin-bottom: 20px;
    }}

    .intro-section p {{
        margin-bottom: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

    # 소개 컨텐츠
    st.markdown("""
    <div class="intro-container">
        <h1 class="intro-title">AI Agent 소개</h1>
        <div class="intro-section">
            <h2>AI Agent란?</h2>
            <p>AI Agent는 인공지능 기반의 자율적인 문제 해결 시스템입니다. 주어진 목표를 달성하기 위해 스스로 판단하고 행동하며, 사용자와의 상호작용을 통해 지속적으로 학습하고 발전합니다.</p>
        </div>
        <div class="intro-section">
            <h2>주식 분석 AI Agent의 특징</h2>
            <p>1. <strong>자연어 이해</strong>: 일반적인 대화처럼 투자 관련 질문을 이해하고 처리합니다.</p>
            <p>2. <strong>데이터 분석</strong>: 실시간으로 주식 시장 데이터를 수집하고 분석합니다.</p>
            <p>3. <strong>투명한 의사결정</strong>: 분석 과정과 판단 근거를 명확하게 제시합니다.</p>
            <p>4. <strong>지속적 학습</strong>: 새로운 정보와 패턴을 학습하여 분석 능력을 향상시킵니다.</p>
        </div>
        <div class="intro-section">
            <h2>AI Agent의 장점</h2>
            <p>• <strong>효율성</strong>: 복잡한 데이터 분석을 빠르게 수행합니다.</p>
            <p>• <strong>객관성</strong>: 감정에 휘둘리지 않는 객관적인 분석을 제공합니다.</p>
            <p>• <strong>접근성</strong>: 전문적인 투자 지식이 없어도 쉽게 활용할 수 있습니다.</p>
            <p>• <strong>맞춤형 분석</strong>: 사용자의 투자 성향과 목표에 맞는 분석을 제공합니다.</p>
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