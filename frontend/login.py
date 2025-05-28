import streamlit as st
import os
from datetime import datetime
import pytz

def login():
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

    /* 로그인 페이지 스타일 */
    .login-container {{
        max-width: 400px;
        margin: 60px auto;
        padding: 30px;
        background: var(--card-bg);
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}

    .login-title {{
        color: var(--primary-color);
        font-size: 2em;
        margin-bottom: 30px;
        text-align: center;
    }}

    .login-form {{
        display: flex;
        flex-direction: column;
        gap: 20px;
    }}

    .form-group {{
        display: flex;
        flex-direction: column;
        gap: 8px;
    }}

    .form-group label {{
        color: var(--text-color);
        font-weight: 500;
    }}

    .form-group input {{
        padding: 12px;
        border: 1px solid var(--border-color);
        border-radius: 5px;
        font-size: 1em;
        background: var(--input-bg);
        color: var(--text-color);
    }}

    .form-group input:focus {{
        outline: none;
        border-color: var(--primary-color);
    }}

    .login-button {{
        background: var(--primary-color);
        color: white;
        padding: 12px;
        border: none;
        border-radius: 5px;
        font-size: 1.1em;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }}

    .login-button:hover {{
        background: var(--primary-hover);
    }}

    .login-links {{
        margin-top: 20px;
        text-align: center;
    }}

    .login-links a {{
        color: var(--primary-color);
        text-decoration: none;
        margin: 0 10px;
    }}

    .login-links a:hover {{
        text-decoration: underline;
    }}
    </style>
    """, unsafe_allow_html=True)

    # 로그인 폼
    st.markdown("""
    <div class="login-container">
        <h1 class="login-title">로그인</h1>
        <form class="login-form">
            <div class="form-group">
                <label for="email">이메일</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="password">비밀번호</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="login-button">로그인</button>
            <div class="login-links">
                <a href="#forgot-password">비밀번호 찾기</a>
                <a href="#signup">회원가입</a>
            </div>
        </form>
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