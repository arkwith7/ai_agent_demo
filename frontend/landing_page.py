import streamlit as st
import base64
import os

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
    # 1) 이미지 로드
    base64_image = get_base64_of_bin_file("resources/images/imgg-gi3-25p6uljm.png")

    # 2) CSS 스타일
    st.markdown(f"""
    <style>
    /* 전체 페이지 리셋 */
    * {{
        margin: 0 !important;
        padding: 0 !important;
        box-sizing: border-box !important;
    }}
    
    html, body {{
        margin: 0 !important;
        padding: 0 !important;
        background: #e5e5e5 !important;
        font-family: Arial, sans-serif !important;
        overflow-x: hidden !important;
    }}

    /* Streamlit 컨테이너 리셋 + 배경색 통일 */
    .stApp,
    [data-testid="stAppViewContainer"],
    .main,
    .main .block-container {{
        margin: 0 !important;
        padding: 0 !important;
        padding-top: 0 !important;
        max-width: none !important;
        width: 100% !important;
        background: #e5e5e5 !important;
    }}
    
    /* 추가 Streamlit 컨테이너들도 배경색 통일 */
    section[data-testid="stSidebar"],
    .css-1d391kg,
    .css-18e3th9,
    .css-1y4p8pa,
    .reportview-container,
    .main .block-container > div,
    .element-container {{
        background: #e5e5e5 !important;
    }}

    /* 헤더 제거 */
    header[data-testid="stHeader"],
    .stDeployButton {{
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
    }}

    /* 첫 번째 요소 여백 제거 */
    .main > div:first-child,
    .element-container:first-child,
    .stMarkdown:first-child {{
        margin-top: 0 !important;
        padding-top: 0 !important;
    }}

    /* 네비게이션 래퍼 추가 */
    .navbar-wrapper {{
        display: flex;
        justify-content: center;
        padding: 0;
        margin: 0;
        background: #e5e5e5;
    }}

    /* 네비게이션 바 */
    .navbar {{
        width: 100%; 
        max-width: 1400px; 
        padding: 16px 24px; 
        display: flex; 
        justify-content: space-between; 
        align-items: center;
        background: #e5e5e5;
        margin-top: 0 !important;
        /* 정렬 보정 */
        box-sizing: border-box;
        position: relative;
    }}
    
    .navbar .logo {{
        flex: 0 0 auto;
        display: flex;
        align-items: center;
    }}
    
    .navbar .nav-links {{
        flex: 0 0 auto;
        display: flex;
        align-items: center;
        gap: 32px;
    }}
    
    .navbar .logo a {{
        font-family: Georgia, serif; 
        font-size: 1.8rem; 
        font-weight: 700;
        text-decoration: none; 
        color: #222;
    }}
    
    .navbar .logo a:hover {{ 
        color: #ff5a00; 
    }}
    
    .navbar .nav-links a {{
        font-family: Arial, sans-serif; 
        font-size: 1rem;
        text-decoration: none; 
        color: #222; 
        transition: color 0.3s;
        white-space: nowrap;
        cursor: pointer;
        /* margin-left 제거하고 gap으로 간격 조정 */
    }}
    
    .navbar .nav-links a:hover {{ 
        color: #ff5a00; 
    }}

    /* Hero 래퍼 */
    .hero-wrapper {{
        display: flex; 
        justify-content: center; 
        padding: 0; 
        margin: 0;
    }}
    
    /* Hero 영역 */
    .hero {{
        width: 100%; 
        max-width: 1400px; 
        height: 75vh; 
        min-height: 400px;
        margin: 0; 
        border-radius: 12px; 
        overflow: hidden;
        display: flex; 
        align-items: center; 
        justify-content: center;
        box-shadow: 0 4px 32px rgba(0,0,0,0.15);
        position: relative;
        
        background-image: 
            linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)),
            url("data:image/png;base64,{base64_image}");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
    }}
      
    .hero-content {{
        color: #fff; 
        text-align: center; 
        font-size: 2.8rem;
        font-weight: 500; 
        line-height: 1.3;
        z-index: 2;
    }}
    
    /* CTA 버튼 스타일 */
    .cta-button {{
        display: inline-block;
        margin-top: 32px;
        padding: 16px 32px;
        background: #ff5a00;
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-size: 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
        border: none;
    }}
    
    .cta-button:hover {{
        background: #e54a00;
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(255, 90, 0, 0.3);
    }}

    /* 반응형 디자인 */
    @media (max-width: 768px) {{
        .navbar-wrapper {{
            background: #e5e5e5;
        }}
        .navbar {{ 
            flex-direction: column; 
            align-items: stretch;
            padding: 12px 16px;
            text-align: center;
        }}
        .navbar .logo {{
            justify-content: center;
            margin-bottom: 12px;
        }}
        .navbar .nav-links {{ 
            justify-content: center;
            flex-wrap: wrap;
            gap: 16px;
        }}
        .navbar .nav-links a {{ 
            font-size: 0.9rem; 
        }}
        .hero {{ 
            height: 50vh; 
            min-height: 300px;
        }}
        .hero-content {{ 
            font-size: 1.5rem; 
        }}
        .cta-button {{
            font-size: 1rem;
            padding: 12px 24px;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

    # 3) 네비게이션 클릭 이벤트 처리를 위한 JavaScript
    st.markdown("""
    <script>
    function navigateToPage(pageName) {
        // Streamlit의 session state를 업데이트하고 페이지를 리로드
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            data: {page: pageName}
        }, '*');
    }
    </script>
    """, unsafe_allow_html=True)

    # 4) HTML 마크업
    st.markdown("""
    <div class="navbar-wrapper">
      <nav class="navbar">
        <div class="logo">
          <a href="#" onclick="navigateToPage('홈')">Agentic AI 체험</a>
        </div>
        <div class="nav-links">
          <a href="#" onclick="navigateToPage('투자 AI 체험')">AI 체험</a>
          <a href="#" onclick="navigateToPage('분석 결과 리포트')">분석 리포트</a>
          <a href="#" onclick="navigateToPage('모의 투자')">모의 투자</a>
        </div>
      </nav>
    </div>
    <div class="hero-wrapper">
      <div class="hero">
        <div class="hero-content">
          <p><span>AI Agent</span>가 실시간으로 정보를 수집,<br>분석, 판단해주는 능력을 체험한다.</p>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 5) Streamlit 버튼으로 페이지 전환 (JavaScript 대안)
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🤖 투자 AI 체험", key="nav_chat", use_container_width=True):
            st.session_state['page'] = '투자 AI 체험'
            st.rerun()
    
    with col2:
        if st.button("📊 분석 결과 리포트", key="nav_report", use_container_width=True):
            st.session_state['page'] = '분석 결과 리포트'
            st.rerun()
    
    with col3:
        if st.button("💰 모의 투자", key="nav_simulation", use_container_width=True):
            st.session_state['page'] = '모의 투자'
            st.rerun()
    
    with col4:
        if st.button("🏠 홈으로", key="nav_home", use_container_width=True):
            st.session_state['page'] = '홈'
            st.rerun()

# main.py에서 호출하므로 여기서는 직접 실행하지 않음