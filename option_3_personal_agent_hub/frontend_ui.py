# [3안] Personal Agent Hub Frontend
import streamlit as st
import requests, os, time
import pandas as pd
from io import BytesIO
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Personal AI Agent", layout="wide")

if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "stats_log" not in st.session_state: st.session_state.stats_log = []

st.title("🤖 Personal Agent Hub")
st.markdown("---")

# 채팅창 구현
chat_container = st.container(height=500)
with chat_container:
    for role, content in st.session_state.chat_history:
        with st.chat_message(role): st.write(content)

if prompt := st.chat_input("에이전트에게 무엇이든 물어보세요..."):
    st.session_state.chat_history.append(("user", prompt))
    with chat_container:
        with st.chat_message("user"): st.write(prompt)

    with st.spinner("에이전트가 생각 중입니다..."):
        try:
            res = requests.post("http://127.0.0.1:8004/ask", params={"query": prompt})
            if res.status_code == 200:
                data = res.json()
                st.session_state.chat_history.append(("assistant", data["answer"]))
                st.session_state.stats_log.append(data["stats"])
                st.rerun()
            else:
                st.error(f"백엔드 오류 (Status: {res.status_code})")
        except requests.exceptions.RequestException as e:
            st.error(f"백엔드 연결 실패: {e}")
        except Exception as e:
            st.error(f"알 수 없는 오류 발생: {e}")

# 사이드바: 에이전트 상태 및 음성 안내
st.sidebar.title("Agent Status")
if st.session_state.chat_history and st.session_state.chat_history[-1][0] == "assistant":
    last_msg = st.session_state.chat_history[-1][1]
    st.sidebar.success("응답 완료")
    if st.sidebar.button("🔊 음성으로 듣기"):
        tts = gTTS(text=last_msg[:300], lang='ko')
        v_buf = BytesIO(); tts.write_to_fp(v_buf); v_buf.seek(0)
        st.sidebar.audio(v_buf.getvalue())

st.sidebar.divider()
if st.session_state.stats_log:
    st.sidebar.metric("마지막 지연시간", f"{st.session_state.stats_log[-1]['latency']}s")
    st.sidebar.metric("총 토큰", f"{st.session_state.stats_log[-1]['total_tokens']}")
