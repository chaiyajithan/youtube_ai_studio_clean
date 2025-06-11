
import streamlit as st
from credits import get_credit, use_credit
import moviepy.editor as mp
import os
import tempfile

st.set_page_config(page_title="🎬 สร้างวิดีโอ AI", layout="centered")

# ตรวจสอบการล็อกอิน
if "username" not in st.session_state:
    st.error("กรุณาเข้าสู่ระบบก่อนใช้งานหน้านี้")
    st.stop()

username = st.session_state["username"]

st.title("🎬 สร้างวิดีโอจากเสียง + ข้อความ")

st.write("อัปโหลดไฟล์เสียง (.mp3) และภาพ (.jpg, .png) เพื่อสร้างวิดีโอ")

audio_file = st.file_uploader("🔊 เลือกไฟล์เสียง", type=["mp3"])
image_file = st.file_uploader("🖼️ เลือกภาพพื้นหลัง", type=["jpg", "jpeg", "png"])

if st.button("🎞️ สร้างวิดีโอ"):
    if not audio_file or not image_file:
        st.warning("กรุณาอัปโหลดไฟล์เสียงและภาพให้ครบ")
        st.stop()

    if not use_credit(username, 1):
        st.error("❌ เครดิตของคุณไม่เพียงพอ กรุณาเติมเงิน")
        st.stop()

    try:
        with st.spinner("📽️ กำลังประมวลผลวิดีโอ..."):
            # บันทึกไฟล์ชั่วคราว
            audio_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            audio_temp.write(audio_file.read())
            audio_temp.close()

            image_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            image_temp.write(image_file.read())
            image_temp.close()

            # โหลดไฟล์
            audio_clip = mp.AudioFileClip(audio_temp.name)
            image_clip = mp.ImageClip(image_temp.name).set_duration(audio_clip.duration).set_audio(audio_clip).resize(height=720)

            video_path = os.path.join(tempfile.gettempdir(), "output_video.mp4")
            image_clip.write_videofile(video_path, fps=24, codec="libx264", audio_codec="aac")

            with open(video_path, "rb") as video_file:
                st.video(video_file.read())

            st.success("✅ สร้างวิดีโอเสร็จสิ้นแล้ว")

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการสร้างวิดีโอ: {e}")
