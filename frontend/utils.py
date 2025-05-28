import streamlit as st
import requests

def get_recommendations(question):
    response = requests.post("http://localhost:8000/chat", json={"question": question})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "추천을 가져오는 데 실패했습니다."}
    
def apply_page_styles():
    # 헤더 제거 및 상단 여백 최소화 CSS (랜딩페이지와 동일)
    st.markdown("""
    <style>
    /* 전체 페이지 리셋 */
    * {
        margin: 0 !important;
        padding: 0 !important;
        box-sizing: border-box !important;
    }
    
    html, body {
        margin: 0 !important;
        padding: 0 !important;
        background: #e5e5e5 !important;
        font-family: Arial, sans-serif !important;
        overflow-x: hidden !important;
    }

    /* Streamlit 컨테이너 리셋 + 배경색 통일 */
    .stApp,
    [data-testid="stAppViewContainer"],
    .main,
    .main .block-container {
        margin: 0 !important;
        padding: 0 !important;
        padding-top: 0 !important;
        max-width: none !important;
        width: 100% !important;
        background: #e5e5e5 !important;
    }
    
    /* 추가 Streamlit 컨테이너들도 배경색 통일 */
    section[data-testid="stSidebar"],
    .css-1d391kg,
    .css-18e3th9,
    .css-1y4p8pa,
    .reportview-container,
    .main .block-container > div,
    .element-container {
        background: #e5e5e5 !important;
    }

    /* 헤더 제거 */
    header[data-testid="stHeader"],
    .stDeployButton {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
    }

    /* 첫 번째 요소 여백 제거 */
    .main > div:first-child,
    .element-container:first-child,
    .stMarkdown:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* 컨텐츠 여백 조정 */
    .main .block-container {
        padding: 1rem 1rem 0 1rem !important;
    }
    
    /* 타이틀 상단 여백 제거 */
    h1 {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)