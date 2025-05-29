import streamlit as st
import time
from datetime import datetime
import uuid
import html

# ============================================================================
# 페이지 설정 및 기본 스타일
# ============================================================================

def configure_page():
    """페이지 기본 설정"""
    st.set_page_config(
        page_title="AI Agent 주식 분석 데모",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

def apply_custom_css():
    """커스텀 CSS 적용 - 상단 네비게이션 완전 덮어버리기"""
    st.markdown("""
    <style>
        /* Streamlit 및 main.py 모든 상단 요소 강제 숨기기 */
        .stDeployButton {display: none !important;}
        #MainMenu {visibility: hidden !important;}
        .stHeader {display: none !important;}
        footer {visibility: hidden !important;}
        .viewerBadge_container__1QSob {display: none !important;}
        header[data-testid="stHeader"] {display: none !important;}
        
        /* main.py 네비게이션 모든 클래스 강제 숨기기 */
        .css-1d391kg, .css-18e3th9, .css-1lcbmhc, .css-1outpf7 {display: none !important;}
        .stTabs {display: none !important;}
        div[data-testid="stSidebar"] {display: none !important;}
        
        /* 상단 모든 컨테이너를 강제로 숨기고 덮어버리기 */
        .main > div:first-child {display: none !important;}
        .stApp > div:first-child {display: none !important;}
        .stApp > header {display: none !important;}
        
        /* 메인 앱의 네비게이션 헤더 완전 제거 */
        .static-header {display: none !important;}
        header.static-header {display: none !important;}
        .stElementContainer:has(.static-header) {display: none !important;}
        div[data-testid="stMarkdownContainer"]:has(.static-header) {display: none !important;}
        
        /* main-content가 포함된 빈 컨테이너 제거 */
        .stElementContainer:has(.main-content) {display: none !important;}
        div[data-testid="stMarkdownContainer"]:has(.main-content) {display: none !important;}
        
        /* hr 구분선 제거 */
        hr {display: none !important;}
        .stElementContainer:has(hr) {display: none !important;}
        div[data-testid="stMarkdownContainer"]:has(hr) {display: none !important;}
        
        /* 전체 앱을 최상단부터 시작 */
        .stApp {
            font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: #f8f9fa;
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        /* 메인 컨테이너를 최상단부터 시작 */
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: none !important;
            padding-top: 0 !important;
        }
        
        /* 고정 헤더로 모든 상단 요소 덮어버리기 */
        .fixed-header {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            z-index: 999999 !important;
            background: white !important;
            padding: 1rem 2rem !important;
            border-bottom: 1px solid #dee2e6 !important;
            display: flex !important;
            justify-content: space-between !important;
            align-items: center !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
            height: 60px !important;
            box-sizing: border-box !important;
        }
        
        .fixed-header h1 {
            color: #007bff !important;
            margin: 0 !important;
            font-size: 1.6em !important;
            font-weight: 600 !important;
        }
        
        .header-home-btn {
            color: #007bff !important;
            text-decoration: none !important;
            font-size: 0.95em !important;
            padding: 8px 16px !important;
            border: 1px solid #007bff !important;
            border-radius: 5px !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            background: white !important;
            display: inline-block !important;
        }
        
        .header-home-btn:hover {
            background-color: #007bff !important;
            color: white !important;
        }
        
        /* 헤더 높이만큼 여백 추가 */
        .main-content {
            margin-top: 60px !important;
            padding: 1rem !important;
            min-height: calc(100vh - 60px) !important;
        }
        
        /* Streamlit 컬럼에 직접 카드 스타일 적용 - 채팅 카드에 맞게 조정 */
        div[data-testid="column"]:first-child {
            background: white !important;
            border: 1px solid #dee2e6 !important;
            border-radius: 10px !important;
            padding: 20px !important;
            margin: 0 10px 0 0 !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
            height: calc(100vh - 120px) !important;
            overflow: hidden !important;
            display: flex !important;
            flex-direction: column !important;
            gap: 10px !important;
        }
        
        div[data-testid="column"]:last-child {
            background: white !important;
            border: 1px solid #dee2e6 !important;
            border-radius: 10px !important;
            padding: 25px !important;
            margin: 0 0 0 10px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
            height: calc(100vh - 120px) !important;
            overflow-y: auto !important;
        }
        
        /* 좌측 패널 스타일 제거 (이제 컬럼에 직접 적용) */
        .left-panel {
            display: none !important;
        }
        
        /* 우측 패널 스타일 제거 */
        .right-panel {
            display: none !important;
        }
        
        /* 좌측 컬럼의 자식 요소들 스타일링 - 단순화 */
        div[data-testid="column"]:first-child > div:nth-child(1) {
            flex-shrink: 0;
        }
        
        div[data-testid="column"]:first-child > div:nth-child(2) {
            flex: 1 !important;
            display: flex !important;
            flex-direction: column !important;
            min-height: 0 !important;
        }
        
        div[data-testid="column"]:first-child > div:nth-child(3),
        div[data-testid="column"]:first-child > div:nth-child(4),
        div[data-testid="column"]:first-child > div:nth-child(5),
        div[data-testid="column"]:first-child > div:nth-child(6) {
            flex-shrink: 0;
        }
        
        /* 채팅 컨테이너 래퍼 스타일 강화 */
        .chat-container-wrapper {
            background: #fafafa !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 8px !important;
            padding: 15px !important;
            flex: 1 !important;
            overflow-y: auto !important;
            margin-bottom: 15px !important;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.05) !important;
            min-height: 250px !important;
            max-height: calc(100vh - 500px) !important;
        }
        
        /* 좌측 패널 제목들 스타일 개선 - 채팅 카드에 맞게 조정 */
        div[data-testid="column"]:first-child h5 {
            font-size: 16px !important;
            margin: 0 0 8px 0 !important;
            color: #333 !important;
            font-weight: 600 !important;
        }
        
        /* 첫 번째 제목은 상단 마진 제거 */
        div[data-testid="column"]:first-child h5:first-of-type {
            margin-top: 0 !important;
        }
        
        /* 질문 입력 제목과 채팅 카드 사이 간격 조정 */
        div[data-testid="column"]:first-child h5:nth-of-type(2) {
            margin-top: 10px !important;
        }
        
        /* Streamlit 컴포넌트 조정 */
        div[data-testid="column"]:first-child .stTextArea textarea {
            border-radius: 8px !important;
            border: 1px solid #dee2e6 !important;
            min-height: 68px !important;
        }
        
        div[data-testid="column"]:first-child .stButton button {
            border-radius: 8px !important;
            border: none !important;
            background-color: #007bff !important;
            color: white !important;
            font-weight: 500 !important;
            width: 100% !important;
            margin: 2px 0 !important;
        }
        
        div[data-testid="column"]:first-child .stButton button:hover {
            background-color: #0056b3 !important;
        }
        
        /* 메시지 스타일 */
        .chat-message {
            margin-bottom: 12px;
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 85%;
            word-wrap: break-word;
        }
        
        /* 결과 카드 - 우측 컬럼에 맞게 조정 */
        .result-card {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        /* 환영 메시지 - 우측 컬럼에 맞게 조정 */
        .welcome-message {
            text-align: center;
            padding: 60px 30px;
            background: #f8f9fa;
            border-radius: 10px;
            border: 1px solid #e9ecef;
            margin: 0;
        }
        
        /* 채팅 컨테이너 개선 - flex 구조에 맞게 조정 */
        .chat-container {
            background: #fafafa;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            flex: 1;
            overflow-y: auto;
            margin-bottom: 15px;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
            scroll-behavior: smooth;
            min-height: 200px;
            max-height: calc(100vh - 500px);
        }
        
        /* 새로운 채팅 컨테이너 래퍼 스타일 */
        .chat-container-wrapper {
            background: #fafafa;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            flex: 1;
            overflow-y: auto;
            margin-bottom: 15px;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
            min-height: 200px;
            max-height: calc(100vh - 500px);
        }
        
        /* 메시지 스타일 */
        .chat-message {
            margin-bottom: 12px;
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 85%;
            word-wrap: break-word;
        }
        
        /* 결과 카드 - 우측 컬럼에 맞게 조정 */
        .result-card {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        /* 환영 메시지 - 우측 컬럼에 맞게 조정 */
        .welcome-message {
            text-align: center;
            padding: 60px 30px;
            background: #f8f9fa;
            border-radius: 10px;
            border: 1px solid #e9ecef;
            margin: 0;
        }
        
        /* Streamlit 컴포넌트 조정 */
        .stTextArea textarea {
            border-radius: 8px !important;
            border: 1px solid #dee2e6 !important;
            min-height: 68px !important;
        }
        
        .stButton button {
            border-radius: 8px !important;
            border: none !important;
            background-color: #007bff !important;
            color: white !important;
            font-weight: 500 !important;
            width: 100% !important;
            margin: 2px 0 !important;
        }
        
        .stButton button:hover {
            background-color: #0056b3 !important;
        }
        
        /* 컬럼 간격 조정 */
        .stColumn {
            padding: 0 5px !important;
        }
        
        /* 컬럼 간격 최소화 */
        div[data-testid="column"] {
            padding: 0 5px !important;
        }
    </style>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    """, unsafe_allow_html=True)

# ============================================================================
# 세션 상태 관리
# ============================================================================

def init_session_state():
    """세션 상태 초기화"""
    if 'demo_chat_history' not in st.session_state:
        st.session_state.demo_chat_history = [
            {
                "sender": "agent",
                "message": "안녕하세요! AI 주식 분석 비서입니다. 무엇을 도와드릴까요? 예를 들어 '워런 버핏 기준으로 회사 찾아줘' 와 같이 질문해보세요.",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
        ]
    
    if 'demo_results' not in st.session_state:
        st.session_state.demo_results = []
    
    if 'demo_current_view' not in st.session_state:
        st.session_state.demo_current_view = "welcome"

# ============================================================================
# 샘플 데이터
# ============================================================================

SAMPLE_COMPANIES = [
    {
        "name": "(주) 테크솔루션",
        "icon": "🏢",
        "sector": "소프트웨어",
        "roe": "18.5%",
        "pbr": "0.9",
        "market_cap": "8.2조원",
        "criteria_met": "6/6",
        "comment": "워런 버핏의 모든 기준을 충족하는 우수 기업입니다."
    },
    {
        "name": "(주) 그린에너지",
        "icon": "💻",
        "sector": "신재생에너지", 
        "roe": "16.2%",
        "pbr": "1.1",
        "market_cap": "5.8조원",
        "criteria_met": "5/6",
        "comment": "ESG 트렌드에 부합하는 미래 성장 동력을 보유한 기업입니다."
    },
    {
        "name": "(주) 바이오헬스",
        "icon": "🏭",
        "sector": "바이오/제약",
        "roe": "14.7%", 
        "pbr": "1.3",
        "market_cap": "4.1조원",
        "criteria_met": "4/6",
        "comment": "신약 파이프라인의 잠재력은 크지만 개발 리스크를 고려해야 합니다."
    }
]

# ============================================================================
# 핵심 기능 함수들
# ============================================================================

def add_chat_message(message: str, sender: str = "user"):
    """채팅 메시지 추가"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.demo_chat_history.append({
        "message": message,
        "sender": sender,
        "timestamp": timestamp
    })

def simulate_agent_response(user_query: str):
    """Agent 응답 시뮬레이션"""
    
    # 사용자 메시지 추가
    add_chat_message(user_query, "user")
    
    # Agent 응답 시작
    add_chat_message("요청을 접수했습니다. 분석을 시작하겠습니다.", "agent")
    
    if "워런 버핏" in user_query or "워런버핏" in user_query:
        add_chat_message("분석이 완료되었습니다! 워런 버핏 기준에 부합하는 추천 종목은 다음과 같습니다.", "agent")
        st.session_state.demo_results = SAMPLE_COMPANIES
        st.session_state.demo_current_view = "results"
        
    elif "성장주" in user_query:
        add_chat_message("성장주 분석이 완료되었습니다!", "agent")
        st.session_state.demo_results = SAMPLE_COMPANIES[:2]
        st.session_state.demo_current_view = "results"
    else:
        add_chat_message("더 구체적인 질문을 해주세요. 예: '워런 버핏 기준으로 회사 찾아줘'", "agent")

def navigate_to_home():
    """홈으로 이동"""
    # 데모 관련 세션 상태 초기화
    keys_to_remove = [key for key in st.session_state.keys() if key.startswith('demo_')]
    for key in keys_to_remove:
        del st.session_state[key]
    
    # 페이지 상태 변경 (main.py와 연동)
    if 'current_page' in st.session_state:
        st.session_state.current_page = "홈"
    elif 'page' in st.session_state:
        st.session_state.page = "홈"
    
    st.rerun()

# ============================================================================
# UI 렌더링 함수들
# ============================================================================

def render_fixed_header():
    """고정 헤더 렌더링 - 모든 상단 요소를 덮어버림"""
    st.markdown("""
    <div class="fixed-header">
        <h1><i class="fas fa-brain"></i> AI Agent 주식 분석</h1>
        <a class="header-home-btn" href="/?page=홈" target="_self">
            <i class="fas fa-home"></i> 소개 페이지로
        </a>
    </div>
    """, unsafe_allow_html=True)

def render_chat_history():
    """채팅 기록 렌더링 - 직접 HTML 채팅 컨테이너"""
    
    # 채팅 메시지들을 HTML로 구성
    chat_messages_html = ""
    
    for chat in st.session_state.demo_chat_history:
        if chat["sender"] == "user":
            # 사용자 메시지
            chat_messages_html += f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 8px;">
                <div style="background: #007bff; color: white; padding: 8px 12px; border-radius: 12px; border-bottom-right-radius: 4px; max-width: 80%; font-size: 0.9em; line-height: 1.4;">
                    <div style="font-size: 0.75em; opacity: 0.8; margin-bottom: 3px;">👤 사용자 • {chat["timestamp"]}</div>
                    <div>{html.escape(chat["message"])}</div>
                </div>
            </div>
            """
        else:
            # AI Agent 메시지
            chat_messages_html += f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 8px;">
                <div style="background: white; color: #212529; padding: 8px 12px; border-radius: 12px; border-bottom-left-radius: 4px; max-width: 80%; border: 1px solid #e0e0e0; font-size: 0.9em; line-height: 1.4;">
                    <div style="font-size: 0.75em; opacity: 0.8; margin-bottom: 3px;">🤖 AI Agent • {chat["timestamp"]}</div>
                    <div>{html.escape(chat["message"])}</div>
                </div>
            </div>
            """
    
    # 완전한 채팅 컨테이너 HTML
    chat_container_html = f"""
    <div style="
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        height: 320px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        display: flex;
        flex-direction: column;
        overflow: hidden;
    ">
        <div id="chatScrollContainer" style="
            background: #fafafa;
            margin: 10px;
            border-radius: 8px;
            padding: 15px;
            height: 280px;
            overflow-y: auto;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
        ">
            {chat_messages_html}
        </div>
    </div>
    
    <style>
        #chatScrollContainer::-webkit-scrollbar {{
            width: 6px;
        }}
        
        #chatScrollContainer::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 3px;
        }}
        
        #chatScrollContainer::-webkit-scrollbar-thumb {{
            background: #c1c1c1;
            border-radius: 3px;
        }}
        
        #chatScrollContainer::-webkit-scrollbar-thumb:hover {{
            background: #a8a8a8;
        }}
    </style>
    
    <script>
        function scrollToBottom() {{
            const container = document.getElementById('chatScrollContainer');
            if (container) {{
                container.scrollTop = container.scrollHeight;
            }}
        }}
        
        // 여러 번 시도해서 확실히 스크롤
        setTimeout(scrollToBottom, 100);
        setTimeout(scrollToBottom, 300);
        setTimeout(scrollToBottom, 500);
        setTimeout(scrollToBottom, 1000);
    </script>
    """
    
    # HTML 렌더링
    st.markdown(chat_container_html, unsafe_allow_html=True)

def render_welcome():
    """환영 메시지 렌더링"""
    st.markdown("""
    <div class="welcome-message">
        <div style="font-size: 3em; margin-bottom: 20px; color: #007bff;">💬</div>
        <h2>AI Agent와 대화를 시작하세요!</h2>
        <p>좌측 하단에 궁금한 점이나 분석하고 싶은 내용을 입력하시면,<br>
        AI Agent가 분석 결과를 이곳에 표시해 드립니다.</p>
        <p><strong>예시:</strong> "워런 버핏 기준으로 회사 찾아줘", "성장주 추천해줘"</p>
    </div>
    """, unsafe_allow_html=True)

def render_results():
    """분석 결과 렌더링"""
    
    for company in st.session_state.demo_results:
        status_color = "green" if "6/6" in company["criteria_met"] else "orange" if "5/6" in company["criteria_met"] else "gray"
        
        st.markdown(f'''
        <div class="result-card">
            <h3>{company["icon"]} {company["name"]}</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">
                <div><strong>업종:</strong> {company["sector"]}</div>
                <div><strong>시가총액:</strong> {company["market_cap"]}</div>
                <div><strong>ROE:</strong> {company["roe"]}</div>
                <div><strong>PBR:</strong> {company["pbr"]}</div>
            </div>
            <div style="background: #f0f8ff; padding: 1rem; border-radius: 8px; border-left: 4px solid {status_color};">
                <strong>워런 버핏 기준: {company["criteria_met"]} 충족</strong>
            </div>
            <div style="background: #f8f9fa; padding: 1rem; margin-top: 1rem; border-radius: 8px;">
                <strong>🤖 AI 분석:</strong><br>
                {company["comment"]}
            </div>
        </div>
        ''', unsafe_allow_html=True)

# ============================================================================
# 메인 함수
# ============================================================================

def start_demo_dynamic():
    """메인 데모 페이지"""
    
    # 페이지 설정 및 스타일 적용
    apply_custom_css()
    
    # 고정 헤더 렌더링 (모든 상단 요소를 덮어버림)
    render_fixed_header()
    
    # 세션 상태 초기화
    init_session_state()
    
    # 메인 컨텐츠 컨테이너 (헤더 아래 시작)
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # 3:7 비율로 좌우 컬럼 분할
    col_left, col_right = st.columns([3, 7], gap="large")
    
    # 좌측 패널 - 대화 인터페이스
    with col_left:
        # 대화창 영역
        st.markdown("##### 💬 대화창")
        render_chat_history()
        
        # 입력 영역
        st.markdown("##### ❓ 질문 입력")
        
        # 빠른 질문 버튼들
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💎 워런 버핏 기준", key="buffett_btn"):
                simulate_agent_response("워런 버핏 기준으로 회사 찾아줘")
                st.rerun()
        
        with col2:
            if st.button("📈 성장주 찾기", key="growth_btn"):
                simulate_agent_response("성장주 추천해줘")
                st.rerun()
        
        # 자유 입력
        user_input = st.text_area(
            "",
            placeholder="AI Agent에게 요청하세요...",
            height=68,
            key="user_input"
        )
        
        if st.button("🚀 분석 요청", type="primary", key="submit_btn"):
            if user_input.strip():
                simulate_agent_response(user_input)
                st.rerun()
    
    # 우측 패널 - 결과 표시
    with col_right:
        if st.session_state.demo_current_view == "results":
            render_results()
        else:
            render_welcome()
    
    st.markdown('</div>', unsafe_allow_html=True)  # main-content 닫기

# ============================================================================
# 실행부
# ============================================================================

if __name__ == "__main__":
    configure_page()
    start_demo_dynamic()