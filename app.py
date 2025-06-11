
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import stripe
import os
from dotenv import load_dotenv
from pathlib import Path
from credits import get_credit, add_credit
from logger import log_usage

# โหลด environment variables
load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# โหลด config.yaml
with open("config.yaml", encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Authenticator
authenticator = stauth.Authenticate(
    credentials=config["credentials"],
    cookie_name=config["cookie"]["name"],
    key=config["cookie"]["key"],
    expiry_days=config["cookie"]["expiry_days"]
)

# Login
login_result = authenticator.login(location="main")
if login_result is not None:
    name, auth_status, username = login_result

    if auth_status is False:
        st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    elif auth_status is None:
        st.warning("กรุณากรอกชื่อผู้ใช้และรหัสผ่าน")
    elif auth_status:
        # ✅ เริ่มระบบเครดิต (ใช้ฟรี 3 ครั้งครั้งแรก)
        if get_credit(username) == 0:
            add_credit(username, 3)

        # UI หลัก
        st.set_page_config(page_title="YouTube AI Studio", layout="wide")
        authenticator.logout("Logout", location="sidebar")
        st.sidebar.success(f"👋 ยินดีต้อนรับ {name}!")
        st.sidebar.markdown(f"💳 เครดิตคงเหลือ: **{get_credit(username)}**")
        st.sidebar.page_link("generate_script.py", label="📝 สร้างสคริปต์ด้วย AI")
        st.sidebar.page_link("generate_voice.py", label="🔊 แปลงข้อความเป็นเสียง")
        st.sidebar.page_link("generate_video.py", label="🎬 สร้างวิดีโอด้วย AI")
        st.sidebar.page_link("dashboard.py", label="📊 ข้อมูลบัญชี / ประวัติการใช้งาน")

        # ส่วนหัว
        logo_path = Path("assets/logo_with_text_wide.jpg")
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)
        st.title("🎥 YouTube AI Studio")
        st.markdown("สร้างวิดีโอจากข้อความด้วย AI 🔥 อย่างง่ายดาย")

        # ฟีเจอร์แนะนำ (demo UI)
        st.markdown("### 🔧 ฟีเจอร์เด่น")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("📝 เขียนสคริปต์อัตโนมัติด้วย AI")
        with col2:
            st.info("🎤 แปลงสคริปต์เป็นเสียงพูด")
        with col3:
            st.info("🎬 สร้างวิดีโอจากเสียงและภาพ")

        # ปุ่ม Stripe Checkout
        st.subheader("🚀 อัปเกรดบัญชี (เพิ่มเครดิต)")
        if st.button("💳 คลิกเพื่อชำระเงิน"):
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'thb',
                        'product_data': {'name': 'YouTube AI Studio - Pro Credit'},
                        'unit_amount': 29900,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:8501/?session=success',
                cancel_url='http://localhost:8501/?session=cancel',
            )
            st.markdown(f"[👉 ไปยังหน้าชำระเงิน]({session.url})")

        # ตรวจสอบสถานะการชำระเงิน
        params = st.experimental_get_query_params()
        if "session" in params:
            if params["session"][0] == "success":
                add_credit(username, 10)
                st.success("✅ ชำระเงินสำเร็จ! ได้รับ 10 เครดิต")
                log_usage(username, "stripe_payment")
            elif params["session"][0] == "cancel":
                st.warning("❌ ยกเลิกการชำระเงิน")

# ระบบสมัครสมาชิก
with st.expander("📨 ลงทะเบียนผู้ใช้ใหม่"):
    try:
        if authenticator.register_user(pre_authorized=config['preauthorized']['emails']):
            st.success("ลงทะเบียนสำเร็จ! กรุณาเข้าสู่ระบบ")
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดขณะลงทะเบียน: {e}")
