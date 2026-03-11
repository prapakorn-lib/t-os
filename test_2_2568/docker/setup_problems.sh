#!/bin/bash
# setup_problems.sh
# รันโดยอัตโนมัติตอน container start เพื่อ inject ปัญหาที่ซ่อนไว้ (ข้อ 1.3)

echo "[setup] กำลังตั้งค่าปัญหาที่ซ่อนไว้สำหรับข้อ 1.3..."

# -------------------------------------------------------
# ปัญหาที่ 1: PostgreSQL data directory permission ผิด
# นักศึกษาต้องวินิจฉัยและแก้สิทธิ์ให้ถูกต้อง
# -------------------------------------------------------
if [ -d "/var/lib/postgresql" ]; then
    chmod 700 /var/lib/postgresql 2>/dev/null || true
    # ทำให้ subdir มี permission ผิดเพื่อให้ postgres ไม่ start
    find /var/lib/postgresql -maxdepth 2 -type d -exec chmod 777 {} \; 2>/dev/null || true
    echo "[setup] ✓ ตั้งค่า PostgreSQL permission ผิดเรียบร้อย"
fi

# -------------------------------------------------------
# ปัญหาที่ 2: รัน dummy process ที่ bind port 8000
# นักศึกษาต้องหา process และ kill ก่อน run uvicorn
# -------------------------------------------------------
# ใช้ Python สร้าง process ที่ listen port 8000 อยู่เบื้องหลัง
python3 -c "
import socket, time, os
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    s.bind(('0.0.0.0', 8000))
    s.listen(1)
    # เขียน pid ไว้ให้นักศึกษาเจอ
    with open('/tmp/blocker.pid', 'w') as f:
        f.write(str(os.getpid()))
    while True:
        time.sleep(60)
except:
    pass
" &

echo "[setup] ✓ Port 8000 ถูก bind โดย dummy process แล้ว"
echo "[setup] เสร็จสิ้น — ปัญหาทั้ง 2 จุดพร้อมแล้ว"
