
import streamlit as st
from credits import get_credit, use_credit
import openai
import os
from dotenv import load_dotenv

# โหลด API key สำหรับ OpenAI
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

st.set_page_config(page_title="📝 สร้างสคริปต์ด้วย AI", layout="centered")

# ตรวจสอบว่าผู้ใช้ล็อกอินหรือยัง
if "username" not in st.session_state:
    st.error("กรุณาเข้าสู่ระบบก่อนใช้งานหน้านี้")
    st.stop()

username = st.session_state["username"]

st.title("📝 สร้างสคริปต์วิดีโอด้วย AI")

topic = st.text_input("📌 ใส่หัวข้อหรือไอเดียวิดีโอของคุณ")

if st.button("✨ สร้างสคริปต์"):
    if not topic:
        st.warning("กรุณาใส่หัวข้อก่อน")
        st.stop()

    if not use_credit(username, 1):
        st.error("❌ เครดิตของคุณไม่เพียงพอ กรุณาเติมเงิน")
        st.stop()

    with st.spinner("กำลังสร้างสคริปต์..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "คุณคือนักเขียนสคริปต์วิดีโอ YouTube มืออาชีพ"},
                    {"role": "user", "content": f"ช่วยเขียนสคริปต์วิดีโอสำหรับหัวข้อ: {topic} ความยาวประมาณ 300 คำ"}
                ],
                temperature=0.7
            )
            script_text = response["choices"][0]["message"]["content"]
            st.success("✅ สร้างสคริปต์สำเร็จ")
            st.text_area("🧾 สคริปต์ที่สร้าง:", value=script_text, height=300)
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
