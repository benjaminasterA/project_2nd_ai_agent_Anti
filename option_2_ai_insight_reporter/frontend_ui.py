# [2안] AI Insight Reporter Frontend
import streamlit as st
import requests, os, textwrap
import pandas as pd
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource
def load_global_fonts():
    fpath = "C:/Windows/Fonts/malgun.ttf" if os.name == 'nt' else "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    return fpath if os.path.exists(fpath) else None

font_path = load_global_fonts()

def create_report_image(text):
    img = Image.new('RGB', (800, 800), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(font_path, 16) if font_path else ImageFont.load_default()
        t_font = ImageFont.truetype(font_path, 24) if font_path else ImageFont.load_default()
    except:
        font = ImageFont.load_default(); t_font = font
    
    draw.rectangle([10, 10, 790, 790], outline=(50, 50, 50), width=2)
    draw.text((30, 30), "AI Insight Reporter: Final Report", font=t_font, fill=(200, 0, 0))
    
    y_pos = 90
    for line in textwrap.wrap(text, width=60):
        draw.text((30, y_pos), line, font=font, fill=(0, 0, 0))
        y_pos += 25
        if y_pos > 750: break
    
    buf = BytesIO(); img.save(buf, format="PNG"); buf.seek(0)
    return buf.getvalue()

st.set_page_config(page_title="AI Insight Reporter", layout="wide")

if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "last_ans" not in st.session_state: st.session_state.last_ans = None
if "stats_log" not in st.session_state: st.session_state.stats_log = []

st.sidebar.title("Reporter Menu")
menu = st.sidebar.radio("작업", ["뉴스 수집 및 분석", "통계 대시보드"])

if menu == "뉴스 수집 및 분석":
    st.title("🗞️ AI Insight Reporter")
    
    for role, content in st.session_state.chat_history:
        with st.chat_message(role): st.write(content)

    if prompt := st.chat_input("뉴스 주제를 입력하세요 (예: AI 반도체 트렌드)..."):
        st.session_state.chat_history.append(("user", prompt))
        with st.chat_message("user"): st.write(prompt)

        with st.spinner("최신 뉴스를 분석하고 보고서를 작성 중입니다..."):
            try:
                res = requests.post("http://127.0.0.1:8001/ask", params={"query": prompt})
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.last_ans = data["answer"]
                    st.session_state.chat_history.append(("assistant", data["answer"]))
                    st.session_state.stats_log.append(data["stats"])
                    st.rerun()
                else:
                    st.error(f"백엔드 오류 (Status: {res.status_code})")
            except requests.exceptions.RequestException as e:
                st.error(f"백엔드 연결 실패: {e}")
            except Exception as e:
                st.error(f"알 수 없는 오류 발생: {e}")

    if st.session_state.last_ans:
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            img_bytes = create_report_image(st.session_state.last_ans)
            st.image(img_bytes, caption="생성된 인사이트 보고서")
        with c2:
            st.info("뉴스 요약을 오디오로 감상하세요.")
            tts = gTTS(text=st.session_state.last_ans[:400], lang='ko')
            v_buf = BytesIO(); tts.write_to_fp(v_buf); v_buf.seek(0)
            st.audio(v_buf.getvalue())

elif menu == "통계 대시보드":
    st.title("📊 운영 통계")
    if st.session_state.stats_log:
        df = pd.DataFrame(st.session_state.stats_log)
        st.metric("평균 응답 속도", f"{df['latency'].mean():.2f}s")
        st.dataframe(df)
    else:
        st.info("데이터가 없습니다.")
