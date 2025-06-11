
import os
import shutil
from datetime import datetime

# ไฟล์ที่ต้องสำรอง
files_to_backup = ["users.json", "logs.json"]
backup_dir = "backups"

# สร้างโฟลเดอร์ backups ถ้ายังไม่มี
os.makedirs(backup_dir, exist_ok=True)

# วันที่สำหรับชื่อไฟล์
date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

for file in files_to_backup:
    if os.path.exists(file):
        backup_filename = f"{file.replace('.json','')}_{date_str}.json"
        shutil.copy(file, os.path.join(backup_dir, backup_filename))
        print(f"✅ สำรองไฟล์ {file} ไปยัง backups/{backup_filename}")
    else:
        print(f"⚠️ ไม่พบไฟล์ {file}, ข้ามการสำรองข้อมูล")
