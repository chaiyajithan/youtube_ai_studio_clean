
import streamlit as st
from credits import get_credit, use_credit
from gtts import gTTS
import tempfile
import os

st.set_page_config(page_title="🔊 แปลงข้อความเป็นเสียง", layout="centered")

# ตรวจสอบการล็อกอิน
if "username" not in st.session_state:
    st.error("กรุณาเข้าสู่ระบบก่อนใช้งานหน้านี้")
    st.stop()

username = st.session_state["username"]

st.title("🔊 แปลงข้อความเป็นเสียงด้วย AI")

text_input = st.text_area("📝 วางข้อความที่ต้องการให้ AI อ่านออกเสียง", height=200)

if st.button("🎤 สร้างเสียงพูดจากข้อความ"):
    if not text_input.strip():
        st.warning("กรุณากรอกข้อความก่อน")
        st.stop()

    if not use_credit(username, 1):
        st.error("❌ เครดิตของคุณไม่เพียงพอ กรุณาเติมเงิน")
        st.stop()

    try:
        with st.spinner("🎧 กำลังสร้างเสียง..."):
            tts = gTTS(text_input, lang='th')
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_file.name)
            audio_file = open(temp_file.name, "rb")
            st.audio(audio_file.read(), format="audio/mp3")
            st.success("✅ แปลงข้อความเป็นเสียงสำเร็จ")
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการแปลงเสียง: {e}")
