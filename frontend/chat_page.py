import streamlit as st
from utils import get_recommendations, apply_page_styles

def chat_page():
    # 헤더 제거 및 상단 여백 최소화 CSS (랜딩페이지와 동일)
    apply_page_styles()
    
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