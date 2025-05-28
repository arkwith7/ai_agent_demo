import streamlit as st
import base64
import os
from datetime import datetime
import pytz

def get_base64_of_bin_file(bin_file_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(base_dir, bin_file_path)
    try:
        with open(abs_file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        st.error(f"Error: Image not found at {abs_file_path}")
        return ""

def landing_page():
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
    </style>
    """, unsafe_allow_html=True)

    # 헤더 섹션
    st.markdown("""
    <header class="static-header">
        <div class="container">
            <a href="#" class="logo"><i class="fas fa-brain"></i> AI Stocks</a>
            <nav>
                <ul>
                    <li><a href="#" class="active">홈</a></li>
                    <li><a href="#ai-agent">AI Agent 소개</a></li>
                    <li><a href="#features">핵심 기능</a></li>
                    <li><a href="#principles">투자 원칙</a></li>
                    <li><a href="#demo">데모 체험</a></li>
                    <li><a href="#login">로그인</a></li>
                    <li><a href="#signup">회원가입</a></li>
                </ul>
            </nav>
        </div>
    </header>
    """, unsafe_allow_html=True)

    # Hero 섹션
    st.markdown("""
    <section class="hero">
        <div class="hero-content">
            <h1>AI Agent, <br>나만의 주식 분석 비서를 경험하세요.</h1>
            <p>복잡한 설정과 버튼 클릭은 이제 그만! <br> AI Agent와 대화하며 원하는 종목을 찾고, 분석 과정을 직접 확인해보세요.</p>
            <a href="#demo" class="cta-button">AI Agent 데모 체험하기 <i class="fas fa-arrow-right"></i></a>
        </div>
    </section>
    """, unsafe_allow_html=True)

    # 메인 컨텐츠
    st.markdown("""
    <main class="content-container">
        <section class="section">
            <h2>AI Agent 주식 분석, 무엇이 다른가요?</h2>
            <p>본 데모 서비스는 단순한 종목 추천을 넘어, AI Agent가 사용자의 요청을 어떻게 이해하고, 어떤 과정을 통해 정보를 분석하여 결과를 도출하는지 그 '경험'에 초점을 맞추고 있습니다. AI Agent의 능동적인 문제 해결 과정을 직접 체험하며 미래의 투자 방식을 엿볼 수 있습니다.</p>
            <a href="#ai-agent" class="learn-more-link">AI Agent 더 알아보기 &raquo;</a>
        </section>

        <section class="section">
            <h2>주요 체험 포인트</h2>
            <div class="features-grid">
                <div class="feature-box">
                    <div class="feature-icon"><i class="fas fa-comments"></i></div>
                    <h3>자연어 기반 요청</h3>
                    <p>"현금흐름 좋고 ROE 높은 IT 기업 찾아줘" 와 같이, 사람에게 말하듯 AI Agent에게 요청하고 결과를 받아보세요.</p>
                </div>
                <div class="feature-box">
                    <div class="feature-icon"><i class="fas fa-microscope"></i></div>
                    <h3>투명한 분석 과정</h3>
                    <p>AI Agent가 어떤 데이터를 조회하고, 어떤 기준으로 종목을 필터링하는지 실시간으로 그 과정을 확인할 수 있습니다.</p>
                </div>
                <div class="feature-box">
                    <div class="feature-icon"><i class="fas fa-chart-line"></i></div>
                    <h3>대화형 인사이트</h3>
                    <p>분석 결과에 대해 궁금한 점을 추가로 질문하고, AI Agent와 대화하며 더 깊이 있는 인사이트를 얻을 수 있습니다.</p>
                </div>
            </div>
            <a href="#features" class="learn-more-link">핵심 기능 자세히 보기 &raquo;</a>
        </section>
    </main>
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

    # JavaScript for KST time update
    st.markdown("""
    <script>
    function updateTimeKST() {
        const now = new Date();
        const kstOffset = 9 * 60; // KST is UTC+9
        const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
        const kstNow = new Date(utc + (kstOffset * 60000));
        
        const year = kstNow.getFullYear();
        const month = String(kstNow.getMonth() + 1).padStart(2, '0');
        const day = String(kstNow.getDate()).padStart(2, '0');
        const hours = String(kstNow.getHours()).padStart(2, '0');
        const minutes = String(kstNow.getMinutes()).padStart(2, '0');
        const seconds = String(kstNow.getSeconds()).padStart(2, '0');
        
        document.querySelector('.static-footer p').innerHTML = 
            `&copy; 2025 AI Agent Stock Analysis Demo. All Rights Reserved. (KST: ${year}-${month}-${day} ${hours}:${minutes}:${seconds})`;
    }
    setInterval(updateTimeKST, 1000);
    </script>
    """, unsafe_allow_html=True)

# main.py에서 호출하므로 여기서는 직접 실행하지 않음