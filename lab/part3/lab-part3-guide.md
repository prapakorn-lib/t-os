# คู่มือการทำ LAB ส่วนที่ 3: การพัฒนา Web API Service
## Operating Systems Course

---

**ชื่อนักศึกษา:** ________________________________  
**รหัสนักศึกษา:** ________________________________  
**กลุ่มเรียน:** ____________ **วันที่ทำ LAB:** ____________

---

## 📋 ภาพรวมของ Lab

### วัตถุประสงค์
- เรียนรู้การพัฒนา Web API Service บนระบบปฏิบัติการ Linux
- ฝึกการติดตั้งและตั้งค่า Database (PostgreSQL)
- พัฒนา REST API ด้วย FastAPI Framework
- เรียนรู้การตั้งค่าความปลอดภัยและการ Deploy

### เวลาที่ใช้โดยประมาณ
- 2-3 ชั่วโมง (ขึ้นอยู่กับความชำนาญ)

### Scenario
บริษัทต้องการให้คุณพัฒนา Web API Service สำหรับจัดการข้อมูลสินค้า โดยต้องมีการเชื่อมต่อกับ Database และมีระบบ Authentication

---

## 🎯 ข้อกำหนดของระบบ

### ทรัพยากรที่ต้องการ
- Ubuntu 20.04 LTS หรือใหม่กว่า
- RAM อย่างน้อย 2 GB
- Storage อย่างน้อย 10 GB
- Python 3.8 หรือใหม่กว่า

### Software Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **Web Server:** Uvicorn
- **Language:** Python 3.8+

---

# 📝 ขั้นตอนการทำ Lab

## 3.1 การวางแผนระบบ (Planning Phase)

### 3.1.1 การวิเคราะห์ความต้องการทรัพยากร

#### วัตถุประสงค์
- เข้าใจความต้องการของระบบ
- วางแผนการจัดสรรทรัพยากร

#### ขั้นตอน

**1. ประเมินความต้องการ**

```
จำนวน concurrent users: 10-20 users
Requests per second: 5-10 requests/sec
Database size: 500 MB - 1 GB
```

**2. วางแผนทรัพยากร**

| ทรัพยากร | ค่าแนะนำ | เหตุผล |
|---|---|---|
| CPU | 2 cores | รองรับ concurrent requests |
| RAM | 2-4 GB | เพียงพอสำหรับ Python + PostgreSQL |
| Storage | 10-20 GB | สำหรับ OS, Database และ Logs |

**3. การบันทึกผล**

กรอกข้อมูลในตาราง:
```
CPU ที่จัดสรร: _____ cores
RAM ที่จัดสรร: _____ GB
Storage ที่จัดสรร: _____ GB
```

---

## 3.2 การติดตั้งและตั้งค่า Environment

### 3.2.1 การติดตั้ง Python และ Dependencies

#### วัตถุประสงค์
- ติดตั้ง Python และเครื่องมือที่จำเป็น
- สร้าง Virtual Environment สำหรับโปรเจค

#### ขั้นตอน

**ขั้นตอนที่ 1: ตรวจสอบและติดตั้ง Python**

```bash
# ตรวจสอบ Python version
python3 --version

# ถ้ายังไม่มี ให้ติดตั้ง
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

**ขั้นตอนที่ 2: สร้าง Virtual Environment**

```bash
# สร้างโฟลเดอร์โปรเจค
mkdir ~/fastapi_project
cd ~/fastapi_project

# สร้าง virtual environment
python3 -m venv venv

# เปิดใช้งาน virtual environment
source venv/bin/activate
```

**ขั้นตอนที่ 3: Upgrade pip**

```bash
pip install --upgrade pip
```

**ขั้นตอนที่ 4: ติดตั้ง Required Packages**

```bash
# ติดตั้ง FastAPI และ dependencies
pip install fastapi uvicorn[standard]

# ติดตั้ง PostgreSQL driver
pip install psycopg2-binary

# ติดตั้ง Pydantic
pip install pydantic

# ติดตั้ง python-dotenv สำหรับจัดการ environment variables
pip install python-dotenv
```

**ขั้นตอนที่ 5: บันทึก Dependencies**

```bash
pip freeze > requirements.txt
```

#### การตรวจสอบ
```bash
# ตรวจสอบ packages ที่ติดตั้ง
pip list

# ควรเห็น packages เหล่านี้:
# - fastapi
# - uvicorn
# - psycopg2-binary
# - pydantic
```

#### บันทึกผล
```
Python Version: _____________
FastAPI Version: _____________
Uvicorn Version: _____________
psycopg2 Version: _____________
```

---

### 3.2.2 การติดตั้งและตั้งค่า PostgreSQL

#### วัตถุประสงค์
- ติดตั้ง PostgreSQL Database Server
- สร้าง Database และ User
- สร้างตารางสำหรับเก็บข้อมูล

#### ขั้นตอน

**ขั้นตอนที่ 1: ติดตั้ง PostgreSQL**

```bash
# Update package list
sudo apt update

# ติดตั้ง PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# ตรวจสอบสถานะ
sudo systemctl status postgresql
```

**ขั้นตอนที่ 2: เข้าสู่ PostgreSQL**

```bash
# สลับไปเป็น postgres user
sudo -i -u postgres

# เข้าสู่ PostgreSQL prompt
psql
```

**ขั้นตอนที่ 3: สร้าง Database และ User**

```sql
-- สร้าง user ใหม่
CREATE USER apiuser WITH PASSWORD 'yourpassword';

-- สร้าง database
CREATE DATABASE apidb OWNER apiuser;

-- ให้สิทธิ์
GRANT ALL PRIVILEGES ON DATABASE apidb TO apiuser;

-- ออกจาก psql
\q
```

**ขั้นตอนที่ 4: สร้างตาราง**

```bash
# เชื่อมต่อกับ database ที่สร้าง
psql -U apiuser -d apidb
```

```sql
-- สร้างตาราง items
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ใส่ข้อมูลทดสอบ
INSERT INTO items (name, description, price, quantity) VALUES
('Laptop', 'High-performance laptop', 25000.00, 10),
('Mouse', 'Wireless mouse', 500.00, 50),
('Keyboard', 'Mechanical keyboard', 2500.00, 30);

-- ตรวจสอบข้อมูล
SELECT * FROM items;

-- ออกจาก psql
\q
```

**ขั้นตอนที่ 5: ตั้งค่าการเชื่อมต่อ (Optional)**

แก้ไขไฟล์ `/etc/postgresql/*/main/pg_hba.conf` หากต้องการให้เชื่อมต่อจากภายนอก:

```bash
sudo nano /etc/postgresql/*/main/pg_hba.conf

# เพิ่มบรรทัด (สำหรับ development only)
# host    all             all             0.0.0.0/0               md5
```

#### การทดสอบ

```bash
# ทดสอบเชื่อมต่อ
psql -U apiuser -d apidb -h localhost -W

# ใน psql ลองคำสั่ง
\dt  # แสดงตาราง
SELECT * FROM items;  # แสดงข้อมูล
```

#### บันทึกผล
```
Database Name: apidb
User Name: apiuser
Table Name: items
Columns: id, name, description, price, quantity, created_at
จำนวนข้อมูลทดสอบ: 3 rows
```

---

### 3.2.3 การติดตั้ง FastAPI + Web Server

#### วัตถุประสงค์
- ตั้งค่า FastAPI Application
- กำหนดค่า Web Server

#### ขั้นตอน

**ขั้นตอนที่ 1: สร้างโครงสร้างโปรเจค**

```bash
cd ~/fastapi_project

# สร้างโครงสร้างโฟลเดอร์
mkdir -p app
touch app/__init__.py
touch app/main.py
touch app/database.py
touch app/models.py
touch .env
```

**ขั้นตอนที่ 2: ตั้งค่า Environment Variables**

สร้างไฟล์ `.env`:
```bash
nano .env
```

เพิ่มเนื้อหา:
```
DATABASE_URL=postgresql://apiuser:yourpassword@localhost/apidb
API_KEY=your-secret-api-key-here
```

**ขั้นตอนที่ 3: สร้างไฟล์ Script**

ใช้ไฟล์ script ที่แยกออกมา:
- `database.py` - การเชื่อมต่อ database
- `models.py` - data models
- `main.py` - FastAPI application

(ดูไฟล์ script แยกที่ให้ไปด้วย)

**ขั้นตอนที่ 4: ทดสอบรัน Application**

```bash
# เปิดใช้งาน virtual environment (ถ้ายังไม่ได้เปิด)
source venv/bin/activate

# รัน FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**ขั้นตอนที่ 5: ทดสอบ API Documentation**

เปิด browser ไปที่:
```
http://localhost:8000/docs
```

คุณจะเห็นหน้า Swagger UI สำหรับทดสอบ API

#### การทดสอบ

```bash
# ทดสอบด้วย curl
curl http://localhost:8000/

# ทดสอบ GET items
curl http://localhost:8000/items

# ทดสอบ GET item by ID
curl http://localhost:8000/items/1
```

#### บันทึกผล
```
FastAPI Server: http://localhost:8000
API Documentation: http://localhost:8000/docs
Port: 8000
Workers: 1 (development)
```

---

## 3.3 การพัฒนาและทดสอบ

### 3.3.1 การสร้าง API Endpoints

#### วัตถุประสงค์
- สร้าง REST API endpoints
- เชื่อมต่อกับ PostgreSQL
- ทดสอบการทำงาน

#### Endpoints ที่ต้องสร้าง

1. **GET /** - Root endpoint
2. **GET /items** - ดึงรายการสินค้าทั้งหมด
3. **GET /items/{id}** - ดึงข้อมูลสินค้าตาม ID

#### คำอธิบาย Code (main.py)

**1. Import Libraries**
```python
from fastapi import FastAPI, HTTPException, Depends, Header
```
- FastAPI: main framework
- HTTPException: จัดการ errors
- Depends: dependency injection
- Header: จัดการ HTTP headers

**2. Database Connection**
```python
from app.database import get_db_connection
```
- เชื่อมต่อกับ PostgreSQL

**3. API Key Authentication**
```python
async def verify_api_key(x_api_key: str = Header(...)):
```
- ตรวจสอบ API key ก่อนเข้าใช้งาน endpoint

**4. Endpoints**

```python
@app.get("/")
```
- Root endpoint แสดงข้อมูลพื้นฐาน

```python
@app.get("/items")
```
- ดึงข้อมูลสินค้าทั้งหมด
- มี API Key authentication
- Query จาก database

```python
@app.get("/items/{item_id}")
```
- ดึงข้อมูลสินค้าตาม ID
- มี API Key authentication
- จัดการกรณีไม่พบข้อมูล (404)

#### การทดสอบ

**1. ทดสอบโดยไม่มี API Key (ควรได้ 403 Error)**

```bash
curl http://localhost:8000/items
```

**2. ทดสอบด้วย API Key**

```bash
# เปลี่ยน your-secret-api-key-here เป็น API key จริง
curl -H "X-API-Key: your-secret-api-key-here" http://localhost:8000/items
```

**3. ทดสอบด้วย Swagger UI**

1. เปิด http://localhost:8000/docs
2. คลิก "Authorize" ปุ่ม
3. ใส่ API Key
4. ทดสอบแต่ละ endpoint

**4. ทดสอบ Error Handling**

```bash
# ทดสอบ item ที่ไม่มี (ควรได้ 404)
curl -H "X-API-Key: your-secret-api-key-here" http://localhost:8000/items/999
```

#### การตรวจสอบผลลัพธ์

**Expected Output สำหรับ GET /items:**
```json
[
    {
        "id": 1,
        "name": "Laptop",
        "description": "High-performance laptop",
        "price": 25000.00,
        "quantity": 10,
        "created_at": "2024-01-01T00:00:00"
    },
    ...
]
```

#### บันทึกผล
```
✅ GET / - Working
✅ GET /items - Working
✅ GET /items/{id} - Working
✅ Database Connection - Working
✅ API Key Authentication - Working
✅ Error Handling - Working
```

---

## 3.4 การตั้งค่าความปลอดภัย

### 3.4.1 API Key Authentication

#### วัตถุประสงค์
- เพิ่มความปลอดภัยให้กับ API
- จำกัดการเข้าถึง endpoints

#### ขั้นตอน

**ขั้นตอนที่ 1: สร้าง API Key**

```bash
# สร้าง random API key
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**ขั้นตอนที่ 2: เพิ่มใน .env**

```bash
nano .env
```

เพิ่ม:
```
API_KEY=your-generated-api-key-here
```

**ขั้นตอนที่ 3: ทดสอบ Authentication**

```bash
# ไม่มี API Key - ควรได้ 403
curl http://localhost:8000/items

# มี API Key ที่ถูกต้อง - ควรได้ 200
curl -H "X-API-Key: your-api-key" http://localhost:8000/items

# มี API Key ผิด - ควรได้ 403
curl -H "X-API-Key: wrong-key" http://localhost:8000/items
```

#### บันทึกผล
```
API Key: [REDACTED for security]
Authentication Method: Header-based (X-API-Key)
Protected Endpoints: /items, /items/{id}
Public Endpoints: /
```

---

### 3.4.2 Firewall และ Port Security

#### วัตถุประสงค์
- จำกัดการเข้าถึง ports
- เพิ่มความปลอดภัยของระบบ

#### ขั้นตอน

**ขั้นตอนที่ 1: ติดตั้ง UFW**

```bash
# ติดตั้ง UFW (Uncomplicated Firewall)
sudo apt install ufw -y
```

**ขั้นตอนที่ 2: ตั้งค่า Firewall Rules**

```bash
# อนุญาต SSH (สำคัญ! ห้ามลืม)
sudo ufw allow 22/tcp

# อนุญาต HTTP
sudo ufw allow 80/tcp

# อนุญาต FastAPI port (development)
sudo ufw allow 8000/tcp

# อนุญาต HTTPS (ถ้ามี)
# sudo ufw allow 443/tcp
```

**ขั้นตอนที่ 3: เปิดใช้งาน UFW**

```bash
# ตรวจสอบ rules
sudo ufw show added

# เปิดใช้งาน
sudo ufw enable

# ตรวจสอบสถานะ
sudo ufw status verbose
```

**ขั้นตอนที่ 4: ตั้งค่า PostgreSQL (Production)**

```bash
# สำหรับ production ควรปิด external access
sudo ufw deny 5432/tcp

# PostgreSQL ควรฟังที่ localhost only
# แก้ไข /etc/postgresql/*/main/postgresql.conf
# listen_addresses = 'localhost'
```

#### การทดสอบ

```bash
# ตรวจสอบ ports ที่เปิด
sudo ufw status numbered

# ทดสอบเข้าถึง API จาก network อื่น
curl http://your-server-ip:8000/
```

#### Best Practices
- ปิด ports ที่ไม่จำเป็น
- ใช้ fail2ban สำหรับป้องกัน brute force
- Update security patches สม่ำเสมอ
- ใช้ HTTPS สำหรับ production

#### บันทึกผล
```
Port 22 (SSH): ✅ Open (restricted to trusted IPs)
Port 80 (HTTP): ✅ Open
Port 8000 (FastAPI): ✅ Open (development only)
Port 5432 (PostgreSQL): ❌ Closed (localhost only)
UFW Status: Active
```

---

## 3.5 การ Deploy และ Monitoring

### 3.5.1 Process Management

#### วัตถุประสงค์
- ให้ API รันต่อเนื่องแม้ปิด terminal
- Auto-restart เมื่อเกิด error

#### วิธีที่ 1: ใช้ systemd (แนะนำสำหรับ Production)

**ขั้นตอนที่ 1: สร้าง systemd service**

```bash
sudo nano /etc/systemd/system/fastapi.service
```

เพิ่มเนื้อหา:
```ini
[Unit]
Description=FastAPI Application
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/fastapi_project
Environment="PATH=/home/your-username/fastapi_project/venv/bin"
ExecStart=/home/your-username/fastapi_project/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**ขั้นตอนที่ 2: เปิดใช้งาน service**

```bash
# Reload systemd
sudo systemctl daemon-reload

# เปิดใช้งาน service
sudo systemctl enable fastapi

# Start service
sudo systemctl start fastapi

# ตรวจสอบสถานะ
sudo systemctl status fastapi
```

**คำสั่งที่ใช้บ่อย:**
```bash
# ดู logs
sudo journalctl -u fastapi -f

# Restart service
sudo systemctl restart fastapi

# Stop service
sudo systemctl stop fastapi
```

#### วิธีที่ 2: ใช้ screen (ง่ายสำหรับ Development)

**ขั้นตอนที่ 1: ติดตั้ง screen**

```bash
sudo apt install screen -y
```

**ขั้นตอนที่ 2: สร้าง session**

```bash
# สร้าง screen session
screen -S fastapi

# รัน FastAPI
cd ~/fastapi_project
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000

# กด Ctrl+A+D เพื่อ detach
```

**คำสั่งที่ใช้บ่อย:**
```bash
# ดู sessions
screen -ls

# กลับเข้า session
screen -r fastapi

# Kill session
screen -X -S fastapi quit
```

#### วิธีที่ 3: ใช้ supervisor

**ขั้นตอนที่ 1: ติดตั้ง supervisor**

```bash
sudo apt install supervisor -y
```

**ขั้นตอนที่ 2: สร้าง config**

```bash
sudo nano /etc/supervisor/conf.d/fastapi.conf
```

เพิ่มเนื้อหา:
```ini
[program:fastapi]
command=/home/your-username/fastapi_project/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
directory=/home/your-username/fastapi_project
user=your-username
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/fastapi.log
```

**ขั้นตอนที่ 3: เปิดใช้งาน**

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start fastapi
sudo supervisorctl status
```

#### บันทึกผล
```
Process Manager: systemd / screen / supervisor (เลือก 1)
Auto-restart: ✅ Enabled
Log Location: /var/log/fastapi.log หรือ journal
Service Status: Active and Running
```

---

### 3.5.2 Monitoring Tools

#### วัตถุประสงค์
- ติดตามสถานะระบบ
- ดู logs และ performance
- แก้ไขปัญหาได้รวดเร็ว

#### 1. Application Logs (บังคับ)

**ขั้นตอนที่ 1: ตั้งค่า Logging ใน FastAPI**

สร้างไฟล์ `app/logger.py`:
```python
import logging

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

เพิ่มใน `main.py`:
```python
from app.logger import logger

@app.get("/items")
async def get_items(...):
    logger.info("Fetching all items")
    # ...
```

**ขั้นตอนที่ 2: ดู Logs**

```bash
# ดู logs แบบ real-time
tail -f app.log

# หรือถ้าใช้ systemd
sudo journalctl -u fastapi -f

# ค้นหา errors
grep "ERROR" app.log

# ดู logs 100 บรรทัดล่าสุด
tail -n 100 app.log
```

#### 2. System Monitoring - htop (บังคับ)

**ขั้นตอนที่ 1: ติดตั้ง htop**

```bash
sudo apt install htop -y
```

**ขั้นตอนที่ 2: ใช้งาน htop**

```bash
# รัน htop
htop

# ฟีเจอร์ที่สำคัญ:
# - F3: ค้นหา process (พิมพ์ "uvicorn")
# - F4: กรอง process
# - F6: เรียงลำดับ
# - F9: Kill process
# - F10: ออก
```

**สิ่งที่ต้องสังเกต:**
- CPU usage ของ uvicorn process
- Memory usage
- Load average
- Running processes

#### 3. เครื่องมือเพิ่มเติม 

**Option A: PostgreSQL Monitoring**

```bash
# ดู active connections
psql -U apiuser -d apidb -c "SELECT count(*) FROM pg_stat_activity;"

# ดู database size
psql -U apiuser -d apidb -c "SELECT pg_size_pretty(pg_database_size('apidb'));"

# ดู query statistics
psql -U apiuser -d apidb -c "SELECT * FROM pg_stat_statements LIMIT 10;"
```

**Option B: Disk Usage Monitoring**

```bash
# ดู disk usage
df -h

# ดู folder size
du -sh ~/fastapi_project

# ดู log size
du -sh /var/log
```

**Option C: Network Monitoring**

```bash
# ติดตั้ง nethogs
sudo apt install nethogs -y

# ดู network usage by process
sudo nethogs

# ดู active connections
ss -tuln | grep 8000
```

**Option D: API Response Time**

สร้าง script `monitor_api.sh`:
```bash
#!/bin/bash
while true; do
    echo "Testing API response time..."
    time curl -s -H "X-API-Key: your-api-key" http://localhost:8000/items > /dev/null
    sleep 5
done
```

```bash
chmod +x monitor_api.sh
./monitor_api.sh
```

#### การตั้งค่า Monitoring Dashboard (Advanced)

**ใช้ Prometheus + Grafana (Optional)**

```bash
# ติดตั้ง prometheus client
pip install prometheus-client

# เพิ่มใน main.py
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

REQUEST_COUNT = Counter('request_count', 'Total request count')
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')
```

#### บันทึกผล

**Metrics Tracked:**
```
✅ CPU Usage
✅ Memory Usage
✅ Disk I/O
✅ API Response Time
✅ Error Rate
✅ Database Connections

Log Location: ~/fastapi_project/app.log
Monitoring Tools:
1. Application Logs - ✅ Configured
2. htop - ✅ Installed and Running
3. Additional Tool: __________________
```

**สรุป Monitoring Setup:**
```
- Log Rotation: ⬜ Enabled / ⬜ Disabled
- Alert System: ⬜ Enabled / ⬜ Disabled
- Backup Strategy: ⬜ Enabled / ⬜ Disabled
```

---

## 📊 การทดสอบและ Validation

### Checklist ทดสอบ

#### 1. Functionality Tests
```
⬜ API ตอบกลับถูกต้อง
⬜ Database connection ทำงาน
⬜ Authentication ทำงาน
⬜ Error handling ถูกต้อง
```

#### 2. Performance Tests
```
⬜ Response time < 1 second
⬜ CPU usage < 70%
⬜ Memory usage < 80%
⬜ No memory leaks
```

#### 3. Security Tests
```
⬜ API Key required
⬜ Firewall configured
⬜ Database password protected
⬜ No sensitive data in logs
```

---

## 🔍 Troubleshooting

### ปัญหาที่พบบ่อยและวิธีแก้

#### 1. Database Connection Error

**ปัญหา:** `psycopg2.OperationalError: could not connect`

**แก้ไข:**
```bash
# ตรวจสอบ PostgreSQL running
sudo systemctl status postgresql

# ตรวจสอบ connection string ใน .env
cat .env

# ทดสอบเชื่อมต่อด้วย psql
psql -U apiuser -d apidb -h localhost
```

#### 2. Port Already in Use

**ปัญหา:** `OSError: [Errno 98] Address already in use`

**แก้ไข:**
```bash
# หา process ที่ใช้ port 8000
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>

# หรือเปลี่ยน port
uvicorn app.main:app --port 8001
```

#### 3. Permission Denied

**ปัญหา:** `PermissionError: [Errno 13]`

**แก้ไข:**
```bash
# ตรวจสอบ file permissions
ls -la

# แก้ไข ownership
sudo chown -R $USER:$USER ~/fastapi_project

# แก้ไข permissions
chmod -R 755 ~/fastapi_project
```

#### 4. Module Not Found

**ปัญหา:** `ModuleNotFoundError: No module named 'fastapi'`

**แก้ไข:**
```bash
# ตรวจสอบ virtual environment
which python

# เปิดใช้งาน venv
source venv/bin/activate

# ติดตั้ง dependencies
pip install -r requirements.txt
```

---

## 📋 สรุปและการส่งงาน

### สิ่งที่ต้องส่ง

1. **เอกสาร Lab Report** (lablogs.md)
   - กรอกข้อมูลครบทุกส่วน
   - บันทึกปัญหาและวิธีแก้

2. **Source Code**
   - `main.py`
   - `database.py`
   - `models.py`
   - `.env.example` (ไม่ใช่ .env จริง!)
   - `requirements.txt`

3. **Screenshots**
   - API Documentation (Swagger UI)
   - Successful API Response
   - Database Tables
   - Monitoring Dashboard
   - UFW Status

4. **Documentation**
   - README.md
   - API Documentation
   - Setup Instructions

### คะแนนที่ได้

| รายการ | คะแนนเต็ม |
|---|:---:|
| 3.1 การวางแผนระบบ | 5 |
| 3.2 ติดตั้งและตั้งค่า Environment | 5 |
| 3.3 พัฒนาและทดสอบ | 5 |
| 3.4 ตั้งค่าความปลอดภัย | 5 |
| 3.5 Deploy และ Monitor | 5 |
| **รวม** | **25** |

---

## 📚 แหล่งข้อมูลเพิ่มเติม

### Documentation
- FastAPI: https://fastapi.tiangolo.com/
- PostgreSQL: https://www.postgresql.org/docs/
- Uvicorn: https://www.uvicorn.org/
- Pydantic: https://docs.pydantic.dev/

### Tutorials
- FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/
- PostgreSQL Tutorial: https://www.postgresqltutorial.com/
- Python Best Practices: https://docs.python-guide.org/

### Tools
- Postman: API Testing
- DBeaver: Database Management
- VS Code: Code Editor

---

## 💡 Tips & Best Practices

### Development Tips
1. ใช้ virtual environment เสมอ
2. เก็บ sensitive data ใน .env
3. ใช้ .gitignore สำหรับ .env และ venv/
4. Test API ก่อน deploy
5. เขียน documentation ให้ชัดเจน

### Security Tips
1. อย่าใช้ default passwords
2. อย่า hardcode credentials
3. ใช้ HTTPS สำหรับ production
4. Update dependencies สม่ำเสมอ
5. Backup database เป็นประจำ

### Production Tips
1. ใช้ process manager (systemd)
2. ตั้งค่า log rotation
3. Monitor resource usage
4. มี backup strategy
5. Document everything

---

## ✅ Checklist สำหรับการทำ Lab

### ก่อนเริ่ม
```
⬜ อ่านคู่มือทั้งหมด
⬜ เตรียม Ubuntu VM
⬜ เช็ค internet connection
⬜ เตรียม text editor
```

### ระหว่างทำ
```
⬜ ทำตามขั้นตอนทีละขั้น
⬜ บันทึกคำสั่งที่ใช้
⬜ Capture screenshots
⬜ บันทึกปัญหาที่พบ
```

### หลังเสร็จ
```
⬜ ทดสอบ API ทุก endpoints
⬜ ตรวจสอบ security
⬜ Review code
⬜ เตรียมเอกสารส่งงาน
```

---

**จัดทำโดย:** Prapakorn Srisawangwong 
**เวอร์ชัน:** 1.0  
**วันที่:** November 2025

---

**หมายเหตุ:** หากพบปัญหาหรือข้อสงสัย กรุณาติดต่ออาจารย์ผู้สอนหรือ TA
