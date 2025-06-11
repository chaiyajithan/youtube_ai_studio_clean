
import streamlit as st
import json
from credits import get_credit, add_credit
from logger import load_logs

st.set_page_config(page_title="🛠️ Admin Dashboard", layout="wide")
st.title("🛠️ แผงควบคุมผู้ดูแลระบบ")

# ตรวจสอบรหัสผ่านแอดมิน (แบบง่าย)
admin_pass = st.text_input("🔐 รหัสผ่านแอดมิน", type="password")
if admin_pass != "admin123":
    st.warning("กรุณาใส่รหัสผ่านแอดมินเพื่อดูข้อมูล")
    st.stop()

# โหลดผู้ใช้จาก users.json
try:
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)
except FileNotFoundError:
    users = {}

# ตารางผู้ใช้และเครดิต
st.subheader("👥 รายชื่อผู้ใช้และเครดิต")

cols = st.columns([3, 1, 2])
cols[0].write("**ชื่อผู้ใช้**")
cols[1].write("**เครดิต**")
cols[2].write("**เพิ่มเครดิต**")

for user in users.keys():
    cols[0].write(user)
    cols[1].write(get_credit(user))
    credit_input = cols[2].number_input(f"add_{user}", min_value=0, step=1, label_visibility="collapsed", key=f"{user}_input")
    if cols[2].button("เพิ่ม", key=f"{user}_btn"):
        add_credit(user, credit_input)
        st.success(f"เพิ่มเครดิตให้ {user} แล้ว +{credit_input}")

# แสดง log การใช้งานทั้งหมด
st.subheader("📜 ประวัติการใช้งานทั้งหมด")
logs = load_logs()
if logs:
    st.dataframe(logs[::-1])
else:
    st.info("ยังไม่มี log การใช้งาน")
