import streamlit as st
import os
from datetime import datetime
import pytz

def signup():
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

    /* 회원가입 페이지 스타일 */
    .signup-container {{
        max-width: 500px;
        margin: 60px auto;
        padding: 30px;
        background: var(--card-bg);
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}

    .signup-title {{
        color: var(--primary-color);
        font-size: 2em;
        margin-bottom: 30px;
        text-align: center;
    }}

    .signup-form {{
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

    .signup-button {{
        background: var(--primary-color);
        color: white;
        padding: 12px;
        border: none;
        border-radius: 5px;
        font-size: 1.1em;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }}

    .signup-button:hover {{
        background: var(--primary-hover);
    }}

    .signup-links {{
        margin-top: 20px;
        text-align: center;
    }}

    .signup-links a {{
        color: var(--primary-color);
        text-decoration: none;
    }}

    .signup-links a:hover {{
        text-decoration: underline;
    }}

    .terms {{
        margin-top: 20px;
        font-size: 0.9em;
        color: var(--text-light);
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)

    # 회원가입 폼
    st.markdown("""
    <div class="signup-container">
        <h1 class="signup-title">회원가입</h1>
        <form class="signup-form">
            <div class="form-group">
                <label for="name">이름</label>
                <input type="text" id="name" name="name" required>
            </div>
            <div class="form-group">
                <label for="email">이메일</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="password">비밀번호</label>
                <input type="password" id="password" name="password" required>
            </div>
            <div class="form-group">
                <label for="confirm-password">비밀번호 확인</label>
                <input type="password" id="confirm-password" name="confirm-password" required>
            </div>
            <button type="submit" class="signup-button">회원가입</button>
            <div class="signup-links">
                <p>이미 계정이 있으신가요? <a href="#login">로그인</a></p>
            </div>
            <div class="terms">
                <p>회원가입 시 <a href="#terms">이용약관</a>과 <a href="#privacy">개인정보처리방침</a>에 동의하게 됩니다.</p>
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