import streamlit as st
from datetime import datetime
import pytz
import os

def start_demo_dynamic():
    # 스타일 적용
    with open(os.path.join(os.path.dirname(__file__), 'resources/css/styles.css'), 'r') as f:
        css_content = f.read()

    st.markdown(f"""
    <style>
    {css_content}
    .demo-main-container {{ display: flex; gap: 0; min-height: 600px; }}
    .left-panel {{ width: 400px; background: #fff; border-right: 1px solid #dee2e6; padding: 20px; box-sizing: border-box; }}
    .right-panel {{ flex: 1; background: #f8f9fa; padding: 25px; min-height: 600px; }}
    .panel-title {{ font-weight: 600; margin-bottom: 12px; }}
    .chat-history-pane, .agent-action-log-pane {{ border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; background: #fff; margin-bottom: 20px; min-height: 120px; max-height: 220px; overflow-y: auto; }}
    .agent-action-log-pane {{ font-size: 0.92em; background: #f9f9f9; }}
    .suggested-prompt-button {{ background: #e9ecef; color: #212529; font-size: 0.95em; padding: 8px 12px; border: none; border-radius: 6px; margin-right: 8px; margin-bottom: 6px; cursor: pointer; }}
    .suggested-prompt-button:hover {{ background: #d3d9df; }}
    .send-button {{ background: #007bff; color: #fff; border: none; border-radius: 6px; padding: 10px 18px; font-weight: 500; cursor: pointer; }}
    .send-button:hover {{ background: #0056b3; }}
    .results-container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
    .company-card {{ background: #fff; border: 1px solid #dee2e6; border-radius: 10px; padding: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.08); }}
    .company-card h3 {{ margin-top: 0; color: #007bff; }}
    .details-button, .back-to-results-button {{ background: #28a745; color: #fff; border: none; border-radius: 6px; padding: 10px 15px; cursor: pointer; margin-top: 10px; }}
    .details-button:hover, .back-to-results-button:hover {{ background: #1e7e34; }}
    </style>
    """, unsafe_allow_html=True)

    # 상태 초기화
    if 'demo_chat' not in st.session_state:
        st.session_state.demo_chat = [
            {'sender': 'agent', 'text': "안녕하세요! AI 주식 분석 비서입니다. 무엇을 도와드릴까요? 예를 들어 '워런 버핏 기준으로 회사 찾아줘' 와 같이 질문해보세요."}
        ]
    if 'demo_log' not in st.session_state:
        st.session_state.demo_log = ["AI Agent 준비 완료."]
    if 'demo_result' not in st.session_state:
        st.session_state.demo_result = None
    if 'demo_detail' not in st.session_state:
        st.session_state.demo_detail = None

    # 좌측 패널
    with st.container():
        st.markdown('<div class="demo-main-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([400, 9999], gap="small")
        with col1:
            st.markdown('<div class="left-panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-title"><i class="fas fa-comments"></i> 대화창</div>', unsafe_allow_html=True)
            # 채팅 히스토리
            chat_box = ""
            for msg in st.session_state.demo_chat:
                if msg['sender'] == 'user':
                    chat_box += f'<div style="text-align:right;"><span style="background:#007bff;color:#fff;padding:7px 13px;border-radius:16px;display:inline-block;margin-bottom:4px;">{msg["text"]}</span></div>'
                else:
                    chat_box += f'<div style="text-align:left;"><span style="background:#e9ecef;color:#212529;padding:7px 13px;border-radius:16px;display:inline-block;margin-bottom:4px;">{msg["text"]}</span></div>'
            st.markdown(f'<div class="chat-history-pane">{chat_box}</div>', unsafe_allow_html=True)
            # Agent 로그
            st.markdown('<div class="panel-title"><i class="fas fa-cogs"></i> Agent 활동 로그</div>', unsafe_allow_html=True)
            log_box = "".join([f'<div style="margin-bottom:4px;">{log}</div>' for log in st.session_state.demo_log])
            st.markdown(f'<div class="agent-action-log-pane">{log_box}</div>', unsafe_allow_html=True)
            # 입력창
            st.markdown('<div class="panel-title"><i class="fas fa-keyboard"></i> 질문 입력</div>', unsafe_allow_html=True)
            with st.form("demo_chat_form", clear_on_submit=True):
                user_input = st.text_area("", placeholder="AI Agent에게 요청하세요...", key="demo_input", height=70, label_visibility="collapsed")
                col_btn1, col_btn2, col_btn3 = st.columns([1,1,1])
                prompt1 = col_btn1.form_submit_button("워런 버핏 기준", use_container_width=True)
                prompt2 = col_btn2.form_submit_button("성장주 찾기", use_container_width=True)
                send = col_btn3.form_submit_button("전송", use_container_width=True)
            # 프롬프트 버튼 처리
            if prompt1:
                user_input = "워런 버핏 기준으로 회사 찾아줘"
                send = True
            if prompt2:
                user_input = "성장주 찾아줘"
                send = True
            # 전송 처리
            if send and user_input.strip():
                st.session_state.demo_chat.append({'sender': 'user', 'text': user_input.strip()})
                # 시뮬레이션 응답
                if "워런 버핏" in user_input:
                    st.session_state.demo_log.append("워런 버핏 6단계 필터링 진행...")
                    st.session_state.demo_result = "buffett"
                    st.session_state.demo_detail = None
                    st.session_state.demo_chat.append({'sender': 'agent', 'text': "분석이 완료되었습니다. 워런 버핏 기준에 부합하는 추천 종목은 다음과 같습니다. 우측 화면에서 확인해주세요."})
                elif "성장주" in user_input:
                    st.session_state.demo_log.append("성장주 필터링 진행...")
                    st.session_state.demo_result = "growth"
                    st.session_state.demo_detail = None
                    st.session_state.demo_chat.append({'sender': 'agent', 'text': "성장 가능성이 높은 기업들을 분석했습니다. 우측 화면에서 추천 종목을 확인하세요."})
                else:
                    st.session_state.demo_log.append(f"지원하지 않는 쿼리: {user_input}")
                    st.session_state.demo_result = None
                    st.session_state.demo_detail = None
                    st.session_state.demo_chat.append({'sender': 'agent', 'text': f'"{user_input}"에 대한 분석은 현재 데모에서 지원하지 않거나, 좀 더 구체적인 질문이 필요합니다. "워런 버핏" 또는 "성장주"를 포함하여 질문해보세요.'})
        # 우측 패널
        with col2:
            st.markdown('<div class="right-panel">', unsafe_allow_html=True)
            # 상세 뷰
            if st.session_state.demo_detail:
                detail = st.session_state.demo_detail
                st.markdown(f"""
                <button onclick="window.location.reload()" class="back-to-results-button" style="margin-bottom:20px;">← 결과 목록으로</button>
                <div class="company-card">
                    <h2>{detail['name']} 상세 분석</h2>
                    <p><b>ROE:</b> {detail['roe']} / <b>PBR:</b> {detail['pbr']} / <b>시가총액:</b> {detail['market_cap']}</p>
                    <div style="margin:15px 0;">{detail['fcf']}</div>
                    <div style="background:#e7f3fe;border-left:5px solid #007bff;padding:15px;">{detail['comment']}</div>
                </div>
                """, unsafe_allow_html=True)
            # 결과 카드
            elif st.session_state.demo_result == "buffett":
                st.markdown("<h2>분석 결과: 워런 버핏 기준 추천 종목</h2>", unsafe_allow_html=True)
                col_b1, col_b2, col_b3 = st.columns(3)
                with col_b1:
                    if st.button("(주) 가나다전자 상세", key="buffett_a"):
                        st.session_state.demo_detail = {
                            'name': '(주) 가나다전자', 'roe': '22%', 'pbr': '1.2', 'market_cap': '5조',
                            'fcf': 'FCF 데이터 준비 중입니다.',
                            'comment': '(주) 가나다전자는 높은 ROE와 시장 신뢰도를 바탕으로 워런 버핏 기준 5가지를 충족합니다. 다만, 잉여현금흐름의 변동성이 다소 있어 장기적 안정성은 추가 검토가 필요합니다.'
                        }
                with col_b2:
                    if st.button("(주) 마이크로솔루션 상세", key="buffett_b"):
                        st.session_state.demo_detail = {
                            'name': '(주) 마이크로솔루션', 'roe': '18%', 'pbr': '0.9', 'market_cap': '8조',
                            'fcf': '<table><thead><tr><th>연도</th><th>예상 FCF (억원)</th></tr></thead><tbody><tr><td>2025</td><td>800</td></tr><tr><td>2026</td><td>850</td></tr><tr><td>2027</td><td>920</td></tr><tr><td>2028</td><td>1000</td></tr><tr><td>2029</td><td>1100</td></tr><tr><td><strong>합계</strong></td><td><strong>4670</strong></td></tr></tbody></table>',
                            'comment': '(주) 마이크로솔루션의 향후 5년 예상 FCF 총합은 4,670억원으로 현재 시가총액(8조원) 대비 양호한 수준입니다. 워런 버핏의 모든 기준을 충족하며, 특히 지속적인 ROE 성장과 안정적인 현금 흐름이 긍정적입니다.'
                        }
                with col_b3:
                    if st.button("(주) 대한민국철강 상세", key="buffett_c"):
                        st.session_state.demo_detail = {
                            'name': '(주) 대한민국철강', 'roe': '16%', 'pbr': '1.0', 'market_cap': '3조',
                            'fcf': 'FCF 데이터 준비 중입니다.',
                            'comment': '(주) 대한민국철강은 ROE, PBR 등 주요 지표에서 양호한 성과를 보이고 있으나, 워런 버핏 기준 4가지만 충족합니다. 추가적인 성장성 검토가 필요합니다.'
                        }
            elif st.session_state.demo_result == "growth":
                st.markdown("<h2>분석 결과: 추천 성장주</h2>", unsafe_allow_html=True)
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    if st.button("(주) 넥스트테크 상세", key="growth_x"):
                        st.session_state.demo_detail = {
                            'name': '(주) 넥스트테크', 'roe': 'N/A (성장 초기)', 'pbr': 'N/A', 'market_cap': '1.5조',
                            'fcf': '성장 초기 기업 FCF 예측 모델 적용 예정',
                            'comment': '(주) 넥스트테크는 최근 3년간 연평균 매출 성장률 35%를 기록하며 빠르게 성장하고 있는 기술 기업입니다. 현재 수익성보다는 시장 점유율 확대에 집중하고 있으며, 향후 2-3년 내 흑자 전환이 기대됩니다.'
                        }
                with col_g2:
                    if st.button("(주) 바이오퓨처 상세", key="growth_y"):
                        st.session_state.demo_detail = {
                            'name': '(주) 바이오퓨처', 'roe': 'N/A', 'pbr': 'N/A', 'market_cap': 'N/A',
                            'fcf': '신약 파이프라인 다수, 기술수출 기대',
                            'comment': '(주) 바이오퓨처는 혁신적인 신약 파이프라인을 보유하고 있으며, 기술수출을 통한 성장 기대감이 높습니다.'
                        }
            else:
                st.markdown("""
                <div class="results-placeholder">
                    <i class="fas fa-comments"></i>
                    <h2>AI Agent와 대화를 시작하세요!</h2>
                    <p>좌측 하단에 궁금한 점이나 분석하고 싶은 내용을 입력하시면, AI Agent가 분석 결과를 이곳에 표시해 드립니다.</p>
                    <p>예시: "워런 버핏 기준으로 회사 찾아줘", "A 기업 재무상태 알려줘"</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 푸터
    kst = datetime.now(pytz.timezone('Asia/Seoul'))
    formatted_time = kst.strftime('%Y-%m-%d %H:%M:%S')
    st.markdown(f"""
    <footer class="static-footer">
        <p>&copy; 2025 AI Agent Stock Analysis Demo. All Rights Reserved. (KST: {formatted_time})</p>
    </footer>
    """, unsafe_allow_html=True)

    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    """, unsafe_allow_html=True) 