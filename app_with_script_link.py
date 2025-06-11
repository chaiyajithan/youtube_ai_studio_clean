
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import stripe
import os
from dotenv import load_dotenv
from pathlib import Path
from credits import get_credit, add_credit, use_credit

# โหลด environment variables
load_dotenv()
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
stripe.api_key = STRIPE_SECRET_KEY

# โหลด config.yaml
with open("config.yaml", encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Authenticator object
authenticator = stauth.Authenticate(
    credentials=config["credentials"],
    cookie_name=config["cookie"]["name"],
    key=config["cookie"]["key"],
    expiry_days=config["cookie"]["expiry_days"]
)

# ฟอร์มล็อกอิน
login_result = authenticator.login(location="main")

# หาก login_result มีข้อมูล แสดงระบบ
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

        # logout
        authenticator.logout("Logout", location="sidebar")
        st.sidebar.success(f"👋 ยินดีต้อนรับ {name}!")
st.sidebar.page_link("generate_script.py", label="📝 สร้างสคริปต์ด้วย AI")
        st.sidebar.markdown(f"💳 เครดิตคงเหลือ: **{get_credit(username)}**")

        # ตั้งค่าหน้าเว็บ
        st.set_page_config(page_title="YouTube AI Studio", layout="wide")

        # โลโก้
        logo_path = Path("assets/logo_with_text_wide.jpg")
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)
        else:
            st.warning("⚠️ ไม่พบโลโก้ หรือไฟล์ภาพเสียหาย")

        # ส่วนหัวเรื่อง
        st.markdown("""
            <style>
            .main-title {
                font-size: 48px;
                color: #ff4b4b;
                font-weight: bold;
                margin-top: 0;
            }
            .subtitle {
                font-size: 24px;
                color: #444;
            }
            .feature-card {
                padding: 1.5rem;
                background-color: #f9f9f9;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                transition: all 0.3s ease-in-out;
            }
            .feature-card:hover {
                background-color: #ffeaea;
                transform: scale(1.02);
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("<h1 class='main-title'>🎥 YouTube AI Studio</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>สร้างคลิปวิดีโอจากไอเดียของคุณในไม่กี่คลิก 🚀</p>", unsafe_allow_html=True)

        # Navigation menu
        cols = st.columns(3)
        with cols[0]:
            st.markdown("""
            <div class='feature-card'>
                <h3>🎙️ แปลงข้อความเป็นเสียง</h3>
                <p>ใช้ AI สร้างเสียงพูดจากสคริปต์</p>
            </div>""", unsafe_allow_html=True)
        with cols[1]:
            st.markdown("""
            <div class='feature-card'>
                <h3>🖊️ สร้างสคริปต์ด้วย AI</h3>
                <p>เพียงพิมพ์หัวข้อ แล้วรับเนื้อหาอัตโนมัติ</p>
            </div>""", unsafe_allow_html=True)
        with cols[2]:
            st.markdown("""
            <div class='feature-card'>
                <h3>🎬 สร้างวิดีโอ + คำบรรยาย</h3>
                <p>นำเสียง ภาพ วิดีโอ มารวมอัตโนมัติ</p>
            </div>""", unsafe_allow_html=True)

        # ทดลองหักเครดิตเมื่อใช้งานฟีเจอร์
        st.subheader("⚙️ ทดลองใช้งานฟีเจอร์ (ใช้เครดิต 1)")
        if st.button("▶️ สร้างวิดีโอด้วย AI"):
            if use_credit(username, 1):
                st.success("✅ เริ่มสร้างวิดีโอ (หักเครดิต 1 หน่วย)")
            else:
                st.error("❌ เครดิตของคุณไม่เพียงพอ กรุณาเติมเงินก่อนใช้งาน")

        # ปุ่มอัปเกรดเป็น Pro
        st.subheader("🚀 อัปเกรดบัญชีเป็น Pro")
        if st.button("คลิกเพื่อชำระเงิน"):
            try:
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
                    success_url='http://localhost:8501/?session=success',
                    cancel_url='http://localhost:8501/?session=cancel',
                )
                st.markdown(f"[👉 ไปยังหน้าชำระเงิน]({session.url})")
            except Exception as e:
                st.error(f"❌ เกิดข้อผิดพลาด: {str(e)}")

        # ตรวจสอบสถานะการชำระเงิน
        params = st.experimental_get_query_params()
        if "session" in params:
            if params["session"][0] == "success":
                add_credit(username, 10)
                st.success("✅ การชำระเงินสำเร็จ! คุณได้รับ 10 เครดิต")
            elif params["session"][0] == "cancel":
                st.warning("❌ การชำระเงินถูกยกเลิก กรุณาลองใหม่อีกครั้ง")

        # ส่วนท้าย
        st.markdown("""
        ---
        <p style='text-align: center; color: #888;'>
        © 2025 YouTube AI Studio — Powered by Streamlit + Stripe
        </p>
        """, unsafe_allow_html=True)

# ✅ ระบบสมัครสมาชิก
with st.expander("📨 ลงทะเบียนผู้ใช้ใหม่"):
    try:
        if authenticator.register_user(pre_authorized=config['preauthorized']['emails']):
            st.success("ลงทะเบียนสำเร็จ! กรุณาเข้าสู่ระบบ")
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดขณะลงทะเบียน: {e}")
