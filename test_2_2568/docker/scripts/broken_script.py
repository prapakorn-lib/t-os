"""
broken_script.py
----------------
โปรแกรมนี้มี bug อยู่ 1 จุด
นักศึกษา: รันโปรแกรม อ่าน error แล้วแก้ไขให้ถูกต้อง
"""

import os
import datetime

def write_system_info():
    # ------------------------------------------------
    # BUG: path นี้ไม่มีอยู่จริงใน container
    # นักศึกษาต้องแก้ให้เป็น path ที่ถูกต้อง
    # ------------------------------------------------
    output_dir = "/opt/myapp/reports"
    output_file = os.path.join(output_dir, "system_info.txt")

    # สร้าง directory ถ้ายังไม่มี
    os.makedirs(output_dir, exist_ok=True)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        f"=== System Info Report ===",
        f"Timestamp : {now}",
        f"Hostname  : {os.uname().nodename}",
        f"OS        : {os.uname().sysname} {os.uname().release}",
        f"User      : {os.environ.get('USER', 'unknown')}",
        f"Home Dir  : {os.path.expanduser('~')}",
        f"==========================",
    ]

    with open(output_file, "w") as f:
        for line in lines:
            f.write(line + "\n")

    print("✓ เขียนไฟล์สำเร็จ!")
    print(f"  ไฟล์อยู่ที่: {output_file}")
    print(f"\nเนื้อหาในไฟล์:")
    print("-" * 30)
    with open(output_file, "r") as f:
        print(f.read())


if __name__ == "__main__":
    write_system_info()
