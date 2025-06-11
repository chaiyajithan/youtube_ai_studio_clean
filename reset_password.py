
import streamlit as st
import yaml
import bcrypt
from yaml.loader import SafeLoader

st.set_page_config(page_title="🔐 รีเซ็ตรหัสผ่าน", layout="centered")
st.title("🔐 รีเซ็ตรหัสผ่านผู้ใช้")

# โหลด config.yaml
with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.load(file, Loader=SafeLoader)

# ฟอร์มรีเซ็ตรหัสผ่าน
st.write("กรุณากรอกชื่อผู้ใช้และรหัสผ่านใหม่ของคุณ")

username = st.text_input("👤 ชื่อผู้ใช้")
email = st.text_input("📧 อีเมลที่ลงทะเบียนไว้")
new_password = st.text_input("🔑 รหัสผ่านใหม่", type="password")
confirm_password = st.text_input("🔁 ยืนยันรหัสผ่านใหม่", type="password")

if st.button("✅ รีเซ็ตรหัสผ่าน"):
    if not username or not email or not new_password or not confirm_password:
        st.warning("กรุณากรอกข้อมูลให้ครบทุกช่อง")
        st.stop()
    
    if new_password != confirm_password:
        st.error("❌ รหัสผ่านทั้งสองช่องไม่ตรงกัน")
        st.stop()

    # ตรวจสอบ username และ email
    user_data = config["credentials"]["usernames"].get(username)
    if not user_data or user_data["email"].lower() != email.lower():
        st.error("❌ ไม่พบข้อมูลผู้ใช้หรืออีเมลไม่ตรงกัน")
        st.stop()

    # แฮชรหัสผ่านใหม่และบันทึก
    hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    config["credentials"]["usernames"][username]["password"] = hashed_pw

    with open("config.yaml", "w", encoding="utf-8") as file:
        yaml.dump(config, file, allow_unicode=True)
    
    st.success("✅ รีเซ็ตรหัสผ่านเรียบร้อยแล้ว กรุณาเข้าสู่ระบบใหม่")
