import streamlit as st
import requests

def landing_page():
    st.markdown(
        """
        <style>
        /* 기본 스타일 리셋 및 폰트 설정 */
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            overflow-x: hidden;
        }
        /* 네비게이션 바 */
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            padding: 20px 50px;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 1000;
        }
        .navbar .logo {
            font-size: 28px;
            color: #ffffff;
            font-weight: bold;
            text-decoration: none;
        }
        .navbar .nav-links a {
            color: #ffffff;
            margin-left: 30px;
            font-size: 18px;
            text-decoration: none;
            transition: color 0.3s;
        }
        .navbar .nav-links a:hover {
            color: #1f77b4;
        }
        /* Hero 섹션 */
        .hero {
            height: 100vh;
            background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url('https://via.placeholder.com/1500x800') no-repeat center center/cover;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            text-align: center;
            padding: 0 20px;
        }
        .hero h1 {
            font-size: 56px;
            margin-bottom: 20px;
        }
        .hero p {
            font-size: 24px;
            margin-bottom: 40px;
        }
        .hero .cta-btn {
            background-color: #1f77b4;
            color: #ffffff;
            padding: 15px 40px;
            font-size: 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
            text-decoration: none;
        }
        .hero .cta-btn:hover {
            background-color: #145a86;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    
    # 상단 네비게이션 바 렌더링 (사이드바는 제외)
    st.markdown(
        """
        <div class="navbar">
            <a href="#" class="logo">Agentic AI 체험</a>
            <div class="nav-links">
                <a href="#">Service</a>
                <a href="#">About</a>
                <a href="#">로그인</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Hero 섹션 렌더링
    st.markdown(
        """
        <div class="hero">
            <div>
                <h1>AI Agent, 나만의 주식분석 비서</h1>
                <p>대화만으로 주식 분석을 경험해보세요. 종목 추천은 물론 데이터 분석까지!</p>
                <a href="#" class="cta-btn" onclick="window.parent.postMessage({target:'streamlit', type:'NAVIGATE', page:'투자 AI 체험'}, '*');">Agent 체험하기</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # JS 이벤트가 동작하지 않을 경우를 위한 추가 버튼
    if st.button("Agent 체험하기", key="landing_btn"):
        st.session_state['page'] = '투자 AI 체험'

def chat_page():
    st.title("투자 AI 체험")
    st.write("실시간 대화 시연 - AI Agent가 질문을 수집, 분석하고 답변을 제공합니다.")
    user_question = st.text_input("투자 관련 질문을 입력하세요:")
    if st.button("질문 보내기"):
        if user_question:
            with st.spinner("Agent가 질문을 처리 중입니다..."):
                recommendations = get_recommendations(user_question)
                st.session_state['chat_response'] = recommendations
        else:
            st.warning("질문을 입력해 주세요.")
    st.info("현재 종목 필터링 툴을 사용중입니다... (예: ROE 높은 기업 알려줘, 배당 많이 주는 기업?)")
    if 'chat_response' in st.session_state:
        response = st.session_state['chat_response']
        if "error" in response:
            st.error(response["error"])
        else:
            st.markdown("### Agent 응답")
            st.write(response)
            
def report_page():
    st.title("분석 결과 리포트")
    st.write("Agent가 수행한 작업 및 분석 결과를 시각화합니다.")
    if 'chat_response' in st.session_state:
        recommendations = st.session_state['chat_response']
        if recommendations and "stocks" in recommendations:
            for stock in recommendations["stocks"]:
                st.markdown(f"**{stock['name']}**")
                st.write(f"ROE: {stock['roe']}, FCF: {stock['fcf']}")
                st.write("분석 근거: 데이터 호출, 조건 필터링, 분석 해석 등")
        else:
            st.info("아직 분석 결과가 도출되지 않았습니다.")
    else:
        st.info("Agent와 대화를 진행 후 분석 리포트를 확인하세요.")
        
def simulation_page():
    st.title("모의 투자")
    st.write("내 포트폴리오 구성 및 투자 시뮬레이션 기능은 추후 구현될 예정입니다.")
    st.info("포트폴리오 추가, 투자 금액 입력, 시뮬레이션 결과 확인 기능이 포함될 예정입니다.")
    
def get_recommendations(question):
    response = requests.post("http://localhost:8000/chat", json={"question": question})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "추천을 가져오는 데 실패했습니다."}

# 페이지 내비게이션 처리
if 'page' not in st.session_state:
    st.session_state['page'] = '홈'

if st.session_state['page'] == "홈":
    # 랜딩 페이지에서는 사이드바 메뉴 없이 상단 메뉴만 표시
    landing_page()
else:
    # 홈페이지가 아닐 경우에만 사이드바 메뉴 표시
    st.sidebar.title("메뉴")
    page = st.sidebar.radio(
        "페이지 선택", 
        options=["홈", "투자 AI 체험", "분석 결과 리포트", "모의 투자"], 
        index=["홈", "투자 AI 체험", "분석 결과 리포트", "모의 투자"].index(st.session_state['page'])
    )
    st.session_state['page'] = page

    if page == "홈":
        landing_page()
    elif page == "투자 AI 체험":
        chat_page()
    elif page == "분석 결과 리포트":
        report_page()
    elif page == "모의 투자":
        simulation_page()