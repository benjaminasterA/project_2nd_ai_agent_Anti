# [1안] Smart Media Archive Frontend
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

def create_archive_card(text):
    img = Image.new('RGB', (800, 600), color=(240, 248, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(font_path, 18) if font_path else ImageFont.load_default()
        t_font = ImageFont.truetype(font_path, 28) if font_path else ImageFont.load_default()
    except:
        font = ImageFont.load_default(); t_font = font
    
    draw.rectangle([20, 20, 780, 580], outline=(0, 102, 204), width=5)
    draw.text((40, 40), "Media Archive Analysis", font=t_font, fill=(0, 51, 153))
    
    y_pos = 110
    for line in textwrap.wrap(text, width=50):
        draw.text((40, y_pos), line, font=font, fill=(50, 50, 50))
        y_pos += 35
    
    buf = BytesIO(); img.save(buf, format="PNG"); buf.seek(0)
    return buf.getvalue()

st.set_page_config(page_title="Smart Media Archive", layout="wide")

if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "last_ans" not in st.session_state: st.session_state.last_ans = None
if "stats_log" not in st.session_state: st.session_state.stats_log = []

menu = st.sidebar.radio("아카이브 관리", ["미디어 분석 및 검색", "아카이브 통계"])

if menu == "미디어 분석 및 검색":
    st.title("📸 Smart Media Archive Agent")
    
    for role, content in st.session_state.chat_history:
        with st.chat_message(role): st.write(content)

    if prompt := st.chat_input("미디어 묘사 또는 검색어를 입력하세요..."):
        st.session_state.chat_history.append(("user", prompt))
        with st.chat_message("user"): st.write(prompt)

        with st.spinner("AI가 미디어를 분석 중입니다..."):
            try:
                res = requests.post("http://127.0.0.1:8003/ask", params={"query": prompt})
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
            img_bytes = create_archive_card(st.session_state.last_ans)
            st.image(img_bytes, caption="자동 생성된 아카이브 카드")
        with c2:
            tts = gTTS(text=st.session_state.last_ans[:250], lang='ko')
            v_buf = BytesIO(); tts.write_to_fp(v_buf); v_buf.seek(0)
            st.audio(v_buf.getvalue())

elif menu == "아카이브 통계":
    st.title("📊 Archive Operation Stats")
    if st.session_state.stats_log:
        df = pd.DataFrame(st.session_state.stats_log)
        st.metric("평균 분석 시간", f"{df['latency'].mean():.2f}s")
        st.line_chart(df.set_index("timestamp")["latency"])
        st.dataframe(df)
    else:
        st.info("아직 분석 내역이 없습니다.")
