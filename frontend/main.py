import streamlit as st
from landing_page import landing_page
from chat_page import chat_page
from report_page import report_page
from simulation_page import simulation_page

# 페이지 설정 (맨 첫 줄에 위치)
st.set_page_config(
    layout="wide", 
    page_title="Agentic AI 체험",
    page_icon="🤖"
)

# Session State 초기화 (페이지 설정 직후)
if 'page' not in st.session_state:
    st.session_state['page'] = '홈'

# 페이지 내비게이션 처리
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