import streamlit as st
from utils import get_recommendations
import os

def chat_page():
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

    /* 채팅 페이지 스타일 */
    .chat-container {{
        max-width: 800px;
        margin: 40px auto;
        padding: 20px;
        background: var(--card-bg);
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}

    .chat-title {{
        color: var(--primary-color);
        font-size: 2em;
        margin-bottom: 20px;
        text-align: center;
    }}

    .chat-description {{
        color: var(--secondary-color);
        text-align: center;
        margin-bottom: 30px;
    }}

    .chat-input-container {{
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }}

    .chat-input {{
        flex: 1;
        padding: 12px;
        border: 2px solid var(--border-color);
        border-radius: 8px;
        font-size: 1em;
    }}

    .chat-button {{
        background: var(--primary-color);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        cursor: pointer;
        font-weight: bold;
        transition: background-color 0.2s ease;
    }}

    .chat-button:hover {{
        background: var(--hover-darken-primary);
    }}

    .chat-info {{
        background: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
        color: #0d47a1;
    }}

    .chat-response {{
        background: #f5f5f5;
        padding: 20px;
        border-radius: 8px;
        margin-top: 20px;
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
                    <li><a href="#home">홈</a></li>
                    <li><a href="#ai-agent">AI Agent 소개</a></li>
                    <li><a href="#features">핵심 기능</a></li>
                    <li><a href="#principles">투자 원칙</a></li>
                    <li><a href="#demo" class="active">데모 체험</a></li>
                    <li><a href="#login">로그인</a></li>
                    <li><a href="#signup">회원가입</a></li>
                </ul>
            </nav>
        </div>
    </header>
    """, unsafe_allow_html=True)

    # 채팅 컨테이너
    st.markdown("""
    <div class="chat-container">
        <h1 class="chat-title">투자 AI 체험</h1>
        <p class="chat-description">실시간 대화 시연 - AI Agent가 질문을 수집, 분석하고 답변을 제공합니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # 채팅 입력
    col1, col2 = st.columns([4, 1])
    with col1:
        user_question = st.text_input("", placeholder="투자 관련 질문을 입력하세요", key="chat_input")
    with col2:
        if st.button("질문 보내기", key="send_button"):
            if user_question:
                with st.spinner("Agent가 질문을 처리 중입니다..."):
                    recommendations = get_recommendations(user_question)
                    st.session_state['chat_response'] = recommendations
            else:
                st.warning("질문을 입력해 주세요.")

    # 안내 메시지
    st.markdown("""
    <div class="chat-info">
        <i class="fas fa-info-circle"></i> 현재 종목 필터링 툴을 사용중입니다... (예: ROE 높은 기업 알려줘, 배당 많이 주는 기업?)
    </div>
    """, unsafe_allow_html=True)

    # 응답 표시
    if 'chat_response' in st.session_state:
        response = st.session_state['chat_response']
        if "error" in response:
            st.error(response["error"])
        else:
            st.markdown("""
            <div class="chat-response">
                <h3>Agent 응답</h3>
                <div class="response-content">
            """, unsafe_allow_html=True)
            st.write(response)
            st.markdown("</div></div>", unsafe_allow_html=True)

    # Font Awesome 추가
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    """, unsafe_allow_html=True)