# ============================================================
#  Dockerfile — OS Lab Practical Exam
#  Base: Ubuntu 22.04
#  วิชา: Operating Systems
# ============================================================

FROM ubuntu:22.04

# ---- ป้องกัน interactive prompts ----
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Bangkok

# ---- ติดตั้ง packages พื้นฐาน ----
# (Development tools ยังไม่ติดตั้ง — นักศึกษาต้องทำเองในข้อ 1.2)
RUN apt-get update && apt-get install -y \
    # system utilities
    sudo \
    nano \
    vim \
    curl \
    wget \
    net-tools \
    lsof \
    procps \
    iproute2 \
    # PostgreSQL
    postgresql \
    postgresql-contrib \
    # Python (minimal — นักศึกษาต้องติดตั้ง pip, build-essential เอง)
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ---- สร้าง student user ----
RUN useradd -m -s /bin/bash student \
    && echo "student:student123" | chpasswd \
    && echo "student ALL=(ALL) NOPASSWD: /usr/bin/apt, /usr/bin/apt-get" >> /etc/sudoers

# ---- สร้าง /exam directory ----
RUN mkdir -p /exam

# ---- คัดลอก exam scripts ----
COPY scripts/threading_demo.py    /exam/threading_demo.py
COPY scripts/broken_script.py     /exam/broken_script.py
COPY scripts/main.py              /exam/main.py
COPY scripts/buggy_api.py         /exam/buggy_api.py
COPY scripts/setup_problems.sh    /exam/setup_problems.sh
COPY scripts/entrypoint.sh        /entrypoint.sh

# ---- สิทธิ์ไฟล์ ----
RUN chmod +x /entrypoint.sh \
    && chmod +x /exam/setup_problems.sh \
    && chmod 644 /exam/*.py \
    && chown -R root:root /exam

# ---- Pre-install FastAPI packages (ประหยัดเวลาระหว่างสอบ) ----
RUN pip3 install \
    fastapi \
    "uvicorn[standard]" \
    psycopg2-binary \
    pydantic

# ---- ตั้งค่า PostgreSQL ให้ยอมรับ password authentication ----
RUN service postgresql start && sleep 3 \
    && su postgres -c "psql -c \"ALTER USER postgres PASSWORD 'postgres123';\"" \
    && service postgresql stop

# ---- Working directory ----
WORKDIR /home/student

# ---- Expose port ----
EXPOSE 8000 8001

# ---- Entrypoint ----
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
