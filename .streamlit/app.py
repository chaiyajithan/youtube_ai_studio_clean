import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import stripe
from pathlib import Path
import json
import os

# --- โหลด config
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# --- เรียกใช้งาน Authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- ตั้งค่า Stripe API Keys
STRIPE_SECRET_KEY = st.secrets.get("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = st.secrets.get("STRIPE_PUBLIC_KEY")
stripe.api_key = STRIPE_SECRET_KEY

# --- ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="YouTube AI Studio", layout="wide")

# --- แสดงกล่อง Login
name, auth_status, username = authenticator.login(
    form_name="เข้าสู่ระบบ",
    location="main"
)

if auth_status is False:
    st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
elif auth_status is None:
    st.warning("กรุณากรอกชื่อผู้ใช้และรหัสผ่าน")
elif auth_status:
    authenticator.logout("ออกจากระบบ", "sidebar")
    st.sidebar.write(f"ยินดีต้อนรับ {name}! ✨")

    st.title("📽️ YouTube AI Studio")
    st.markdown("สร้างคลิปวิดีโอจาก AI ในไม่กี่คลิก ✨")

    # --- ปุ่มอัปเกรดบัญชี ---
    if st.button("🚀 อัปเกรดเป็น Pro"):
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'thb',
                    'product_data': {
                        'name': 'YouTube AI Studio - Pro Plan',
                    },
                    'unit_amount': 29900,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8501?success=true',
            cancel_url='http://localhost:8501?canceled=true',
        )
        st.markdown(f"[คลิกเพื่อชำระเงิน]({session.url})", unsafe_allow_html=True)

    # --- ระบบเครดิต / อัปโหลด / AI Tools ... ต่อที่นี่ ---
    st.info("🔧 ฟีเจอร์อื่นๆ อยู่ระหว่างพัฒนา")

else:
    st.stop()
