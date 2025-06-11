
import streamlit as st
from credits import get_credit
from logger import load_logs

st.set_page_config(page_title="📊 Dashboard", layout="centered")

# ตรวจสอบการล็อกอิน
if "username" not in st.session_state:
    st.error("กรุณาเข้าสู่ระบบก่อนใช้งานหน้านี้")
    st.stop()

username = st.session_state["username"]

st.title("📊 ข้อมูลบัญชีผู้ใช้")

# แสดงเครดิตปัจจุบัน
st.metric(label="💳 เครดิตคงเหลือ", value=get_credit(username))

# โหลดประวัติทั้งหมดแล้วกรองตามผู้ใช้
logs = load_logs()
user_logs = [log for log in logs if log["username"] == username]

# แสดงจำนวนครั้งที่ใช้แต่ละฟีเจอร์
st.subheader("📈 การใช้งานฟีเจอร์")
from collections import Counter
features = [log["feature"] for log in user_logs]
counts = Counter(features)
for feature, count in counts.items():
    st.write(f"• {feature} : {count} ครั้ง")

# แสดงประวัติล่าสุดแบบตาราง
st.subheader("📜 ประวัติการใช้งาน")
if user_logs:
    st.table(user_logs[::-1])  # เรียงล่าสุดก่อน
else:
    st.info("ยังไม่มีประวัติการใช้งาน")
