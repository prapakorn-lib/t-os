#!/bin/bash
# entrypoint.sh — Container startup script

set -e

echo "============================================"
echo "  OS Lab Exam Environment"
echo "  Ubuntu 22.04 | Docker Container"
echo "============================================"

# --- 1. Start PostgreSQL service ---
echo "[init] Starting PostgreSQL..."
service postgresql start || true
sleep 2

# --- 2. Inject hidden problems for Q1.3 ---
echo "[init] Setting up exam problems..."
bash /exam/setup_problems.sh

# --- 3. Fix broken_script.py: ตั้ง path เป็น path ที่ไม่มีอยู่จริงก่อน ---
# (ไฟล์มี path /opt/myapp/reports ซึ่ง /opt/myapp ยังไม่มี → จะ error)
# ตั้งใจให้นักศึกษาสร้าง /opt/myapp เองในข้อ 1.1

echo "[init] Environment ready!"
echo ""
echo "  ไฟล์สำหรับการสอบอยู่ที่: /exam/"
echo "  ls /exam/ เพื่อดูรายการไฟล์"
echo ""

# --- Keep container running ---
exec "$@"
