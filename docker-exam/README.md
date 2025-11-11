# ข้อสอบปฏิบัติ Docker: ระบบจองตั๋วคอนเสิร์ต
## Concert Ticket Booking System - 2-Tier Architecture

---

## 📋 ภาพรวมข้อสอบ

ข้อสอบนี้ออกแบบมาเพื่อทดสอบความสามารถของนักศึกษาในการ:
- ใช้งาน Docker และ Docker Compose
- เข้าใจสถาปัตยกรรมระบบแบบ 2-tier และ 3-tier
- ทดสอบระบบตาม Software Quality Attributes
- วิเคราะห์และเสนอแนวทางปรับปรุงระบบ

---

## 🎯 วัตถุประสงค์การเรียนรู้

หลังจากทำข้อสอบนี้ นักศึกษาจะสามารถ:

1. **Docker Skills**
   - เขียนและใช้งาน docker-compose.yml
   - สร้างและจัดการ Docker containers
   - ใช้งาน Docker networks และ volumes
   - Debug และแก้ไขปัญหา containers

2. **Architecture Knowledge**
   - อธิบายความแตกต่างระหว่างสถาปัตยกรรมแบบต่างๆ
   - เลือกสถาปัตยกรรมที่เหมาะสมกับความต้องการ
   - วิเคราะห์ข้อดี-ข้อเสียของแต่ละสถาปัตยกรรม

3. **Quality Assurance**
   - ทดสอบ Performance ของระบบ
   - ทดสอบ Availability และ Reliability
   - วิเคราะห์ผลทดสอบและเสนอแนวทางแก้ไข

---

## 📁 โครงสร้างไฟล์

```
docker-exam/
├── README.md                      # คู่มือนี้
├── EXAM_ASSESSMENT.md             # แบบประเมินและเกณฑ์การให้คะแนน
├── EXAM_WORKSHEET.md              # แบบบันทึกสำหรับนักศึกษา
├── docker-compose.yml             # Docker Compose configuration
├── frontend/                      # Frontend application
│   ├── Dockerfile
│   ├── package.json
│   ├── server.js
│   └── public/
│       └── index.html
├── database/                      # Database initialization
│   └── init.sql
└── scripts/                       # Test scripts
    ├── test_performance.sh
    ├── test_availability.sh
    └── test_reliability.sh
```

---

## 🚀 เริ่มต้นใช้งาน

### ข้อกำหนดเบื้องต้น (Prerequisites)

```bash
# ตรวจสอบ Docker
docker --version
# ควรได้ Docker version 20.10 หรือสูงกว่า

# ตรวจสอบ Docker Compose
docker-compose --version
# ควรได้ Docker Compose version 2.0 หรือสูงกว่า

# ติดตั้ง tools เพิ่มเติม
sudo apt-get update
sudo apt-get install -y curl postgresql-client apache2-utils jq
```

### การติดตั้งและรันระบบ

#### 1. Clone หรือ Download โปรเจ็กต์

```bash
# ถ้ามี Git repository
git clone <repository-url>
cd docker-exam

# หรือ extract จาก zip file
unzip docker-exam.zip
cd docker-exam
```

#### 2. Build และ Start Services

```bash
# Build images และ start containers
docker-compose up -d

# ตรวจสอบสถานะ
docker-compose ps

# ดู logs
docker-compose logs -f
```

#### 3. ทดสอบการเข้าถึง

```bash
# ทดสอบ Frontend
curl http://localhost:3000/health

# เปิด browser
xdg-open http://localhost:3000  # Linux
open http://localhost:3000      # macOS
start http://localhost:3000     # Windows
```

---

## 🧪 การทดสอบระบบ

### ทดสอบ Manual

#### 1. เข้าใช้งาน Web Interface

เปิด browser ไปที่ `http://localhost:3000`

คุณจะเห็น:
- รายการคอนเสิร์ตทั้งหมด
- สถิติการจองตั๋ว
- ฟอร์มจองตั๋ว
- ประวัติการจอง

#### 2. ทดสอบการจองตั๋ว

1. คลิกปุ่ม "จองตั๋ว" ที่คอนเสิร์ตที่ต้องการ
2. กรอกข้อมูล:
   - ชื่อผู้จอง
   - อีเมล
   - จำนวนตั๋ว
3. คลิก "ยืนยันการจอง"
4. ตรวจสอบว่าการจองสำเร็จและตั๋วที่เหลือลดลง

#### 3. ทดสอบ API Endpoints

```bash
# Get all concerts
curl http://localhost:3000/api/concerts | jq

# Get specific concert
curl http://localhost:3000/api/concerts/1 | jq

# Get statistics
curl http://localhost:3000/api/stats | jq

# Get all bookings
curl http://localhost:3000/api/bookings | jq

# Health check
curl http://localhost:3000/health | jq

# Book tickets
curl -X POST http://localhost:3000/api/book \
  -H "Content-Type: application/json" \
  -d '{
    "concert_id": 1,
    "customer_name": "Test User",
    "customer_email": "test@example.com",
    "quantity": 2
  }' | jq
```

### ทดสอบด้วย Scripts

เราได้เตรียม test scripts ไว้ให้แล้วใน folder `scripts/`:

```bash
# ทดสอบ Performance
./scripts/test_performance.sh

# ทดสอบ Availability
./scripts/test_availability.sh

# ทดสอบ Reliability
./scripts/test_reliability.sh
```

---

## 📊 Software Quality Attributes

### 1. Performance (ประสิทธิภาพ)

**มาตรฐานที่กำหนด:**
- API Response Time ≤ 200ms
- Database Query Time ≤ 100ms
- รองรับ 10+ concurrent requests

**วิธีทดสอบ:**
```bash
# Response time test
time curl -s http://localhost:3000/api/concerts

# Load test with Apache Bench
ab -n 100 -c 10 http://localhost:3000/api/concerts

# Database query test
docker exec concert-database psql -U concert_user -d concert_db \
  -c "\timing on" -c "SELECT * FROM concerts;"
```

### 2. Availability (ความพร้อมใช้งาน)

**มาตรฐานที่กำหนด:**
- Uptime ≥ 99%
- Health check ตอบสนอง
- Auto-restart เมื่อเกิดปัญหา

**วิธีทดสอบ:**
```bash
# Check container status
docker-compose ps

# Health check
curl http://localhost:3000/health

# Test auto-restart
docker stop concert-frontend
sleep 5
docker-compose ps
```

### 3. Reliability (ความน่าเชื่อถือ)

**มาตรฐานที่กำหนด:**
- ACID transactions
- ไม่มี double booking
- Data consistency

**วิธีทดสอบ:**
```bash
# Test transaction rollback
docker exec concert-database psql -U concert_user -d concert_db \
  -c "BEGIN; UPDATE concerts SET sold_tickets = 99999 WHERE id = 1; ROLLBACK;"

# Test concurrent booking
for i in {1..5}; do
  curl -X POST http://localhost:3000/api/book \
    -H "Content-Type: application/json" \
    -d "{\"concert_id\": 5, \"customer_name\": \"User $i\",
         \"customer_email\": \"user$i@test.com\", \"quantity\": 1}" &
done
wait
```

---

## 🔧 คำสั่ง Docker ที่ใช้บ่อย

### Container Management

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f frontend

# Check container status
docker-compose ps

# Check resource usage
docker stats
```

### Database Operations

```bash
# Access database
docker exec -it concert-database psql -U concert_user -d concert_db

# Run SQL query
docker exec concert-database psql -U concert_user -d concert_db \
  -c "SELECT * FROM concerts;"

# Backup database
docker exec concert-database pg_dump -U concert_user concert_db > backup.sql

# Restore database
cat backup.sql | docker exec -i concert-database \
  psql -U concert_user -d concert_db

# View database logs
docker-compose logs database
```

### Network & Volume

```bash
# List networks
docker network ls

# Inspect network
docker network inspect docker-exam_concert-network

# List volumes
docker volume ls

# Inspect volume
docker volume inspect docker-exam_postgres-data

# Remove unused volumes
docker volume prune
```

### Troubleshooting

```bash
# View container details
docker inspect concert-frontend

# Execute command in container
docker exec -it concert-frontend sh

# Check environment variables
docker exec concert-frontend env

# View container processes
docker top concert-frontend

# Check port mappings
docker port concert-frontend
```

---

## 📝 วิธีการทำข้อสอบ

### สำหรับนักศึกษา

1. **อ่านคู่มือ** (15 นาที)
   - อ่าน README.md ฉบับนี้
   - อ่าน EXAM_ASSESSMENT.md เพื่อทำความเข้าใจเกณฑ์การให้คะแนน
   - ดู EXAM_WORKSHEET.md ที่จะใช้บันทึกคำตอบ

2. **ติดตั้งและทดสอบระบบ** (15 นาที)
   - Clone/Download โปรเจ็กต์
   - รัน `docker-compose up -d`
   - ตรวจสอบว่าระบบทำงานปกติ
   - ทดลองใช้งานผ่าน web browser

3. **ทำข้อสอบส่วนที่ 1: ความเข้าใจสถาปัตยกรรม** (30 นาที)
   - วิเคราะห์ docker-compose.yml
   - ศึกษาโครงสร้างของ frontend และ database
   - ตอบคำถามใน EXAM_WORKSHEET.md

4. **ทำข้อสอบส่วนที่ 2: Quality Attributes Testing** (90 นาที)
   - ทดสอบ Performance (30 นาที)
   - ทดสอบ Availability (30 นาที)
   - ทดสอบ Reliability (30 นาที)
   - บันทึกผลการทดสอบทั้งหมด

5. **ทำข้อสอบส่วนที่ 3: การปรับปรุงระบบ** (30 นาที)
   - วิเคราะห์จุดอ่อนของระบบ
   - เสนอแนวทางปรับปรุง
   - เขียน architecture diagram ใหม่

6. **ตรวจสอบและส่งงาน** (10 นาที)
   - ตรวจสอบคำตอบทั้งหมด
   - แนบ logs/screenshots ที่จำเป็น
   - บันทึกไฟล์ EXAM_WORKSHEET.md

**เวลารวม: 3 ชั่วโมง (180 นาที)**

### สำหรับผู้สอน

1. **เตรียมสภาพแวดล้อม**
   - ติดตั้ง Docker และ Docker Compose บนเครื่องนักศึกษา
   - ติดตั้ง tools ที่จำเป็น (curl, postgresql-client, ab, jq)
   - แจก zip file หรือ git repository

2. **แนะนำข้อสอบ** (15 นาที)
   - อธิบายภาพรวมของข้อสอบ
   - อธิบายเกณฑ์การให้คะแนน
   - ตอบคำถามของนักศึกษา

3. **คุมสอบ**
   - ให้นักศึกษาทำข้อสอบ 3 ชั่วโมง
   - ช่วยแก้ปัญหาทางเทคนิค (เช่น Docker ไม่ทำงาน)
   - ไม่ช่วยตอบคำถามเนื้อหาข้อสอบ

4. **ตรวจข้อสอบ**
   - ใช้ EXAM_ASSESSMENT.md เป็นเกณฑ์ในการให้คะแนน
   - ตรวจสอบผลการทดสอบที่นักศึกษาบันทึกไว้
   - ให้ feedback เพื่อการเรียนรู้

---

## 🎓 เฉลยและคำแนะนำ (สำหรับผู้สอน)

### ส่วนที่ 1: ความเข้าใจสถาปัตยกรรม

**คำตอบที่คาดหวัง:**

#### 1.1 ชนิดของสถาปัตยกรรม
- **สถาปัตยกรรม:** 2-Tier (Client-Server)
- **อธิบาย:** เป็นสถาปัตยกรรมที่แบ่งระบบออกเป็น 2 layers คือ Presentation Tier (Frontend) และ Data Tier (Database)
- **Layers:**
  - **Tier 1 (Frontend):** Node.js + Express server ที่รวม presentation logic และ business logic
  - **Tier 2 (Database):** PostgreSQL database ที่เก็บข้อมูล

#### 1.2 เทคโนโลยีที่ใช้
- **Frontend:** Node.js 18, Express.js 4.x, HTML5, JavaScript
- **Database:** PostgreSQL 15-alpine
- **Container:** Docker, Docker Compose 3.8
- **Network:** Bridge network
- **Volume:** Named volume สำหรับ persistent data

### ส่วนที่ 2: Quality Attributes Testing

#### 2.1 Performance
**ค่าที่คาดหวัง:**
- API Response Time: 10-50ms (ควรผ่านมาตรฐาน ≤ 200ms)
- Database Query: 5-20ms (ควรผ่านมาตรฐาน ≤ 100ms)
- Concurrent Requests: 100% success rate

**ถ้าไม่ผ่าน แนวทางแก้ไข:**
1. เพิ่ม database indexing
2. ใช้ connection pooling
3. เพิ่ม caching (Redis)
4. Optimize queries

#### 2.2 Availability
**ค่าที่คาดหวัง:**
- Container Status: All running
- Health Check: HTTP 200
- Restart Policy: unless-stopped ✓
- Auto-restart: ใช่
- Availability: ≥ 99%

**ถ้าไม่ผ่าน แนวทางแก้ไข:**
1. ตั้ง restart policy เป็น always หรือ unless-stopped
2. เพิ่ม healthcheck ใน docker-compose.yml
3. ใช้ monitoring tools (Prometheus, Grafana)

#### 2.3 Reliability
**ค่าที่คาดหวัง:**
- Transaction Rollback: ✓ ทำงานถูกต้อง
- Data Constraints: ✓ Enforced
- Concurrent Booking: ✓ ไม่มี double booking (ใช้ SELECT FOR UPDATE)
- Data Consistency: ✓ Consistent
- Error Handling: ✓ มี error messages ที่เหมาะสม

**ถ้าไม่ผ่าน แนวทางแก้ไข:**
1. ใช้ database transactions
2. ใช้ row-level locking (FOR UPDATE)
3. เพิ่ม constraints ใน database
4. Implement proper error handling

### ส่วนที่ 3: การปรับปรุงระบบ

#### 3.1 จุดอ่อนของ 2-Tier
1. **Scalability:** ยาก scale แยกส่วน (ต้อง scale ทั้ง frontend + business logic)
2. **Maintainability:** Business logic ผสมกับ presentation logic
3. **Security:** Client เชื่อมต่อ database โดยตรง (ในบางกรณี)
4. **Flexibility:** ยากเปลี่ยน frontend โดยไม่กระทบ business logic
5. **Testing:** ยากทดสอบแยกส่วน

#### 3.2 แนวทางปรับปรุง

**Upgrade เป็น 3-Tier:**
1. แยก Business Logic Layer ออกมาเป็น API Service
2. Frontend เป็นเพียง Pure Web UI
3. มี API Gateway สำหรับจัดการ requests
4. แยก services ตาม domain (concerts, bookings, users)

**เพิ่ม Scalability:**
1. Load Balancer (Nginx, HAProxy)
2. Horizontal scaling (multiple containers)
3. Database replication (Master-Slave)
4. Caching layer (Redis, Memcached)
5. CDN สำหรับ static files

**เพิ่ม Security:**
1. HTTPS/TLS encryption
2. Authentication & Authorization (JWT)
3. Rate limiting
4. Input validation & sanitization
5. SQL injection prevention
6. Secrets management (Docker secrets, Vault)
7. Network policies

---

## 🐛 Troubleshooting

### ปัญหาที่พบบ่อยและวิธีแก้ไข

#### 1. Container ไม่ start

```bash
# ดู logs
docker-compose logs

# ลอง rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

#### 2. Database connection error

```bash
# ตรวจสอบว่า database container running
docker-compose ps

# ตรวจสอบ database logs
docker-compose logs database

# ทดสอบ connection
docker exec concert-database pg_isready -U concert_user
```

#### 3. Port already in use

```bash
# หา process ที่ใช้ port 3000
sudo lsof -i :3000
# หรือ
sudo netstat -tulpn | grep 3000

# Kill process หรือเปลี่ยน port ใน docker-compose.yml
```

#### 4. Permission denied

```bash
# ให้สิทธิ์ execute scripts
chmod +x scripts/*.sh

# หรือรัน docker ด้วย sudo
sudo docker-compose up -d
```

#### 5. Out of disk space

```bash
# ลบ unused images
docker image prune -a

# ลบ unused volumes
docker volume prune

# ลบทุกอย่างที่ไม่ใช้
docker system prune -a --volumes
```

---

## 📚 เอกสารอ้างอิง

### Docker Documentation
- [Docker Compose](https://docs.docker.com/compose/)
- [Docker Networking](https://docs.docker.com/network/)
- [Docker Volumes](https://docs.docker.com/storage/volumes/)

### Architecture Patterns
- [2-Tier vs 3-Tier Architecture](https://www.ibm.com/topics/three-tier-architecture)
- [Software Architecture Patterns](https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/)

### Software Quality
- [Software Quality Attributes](https://en.wikipedia.org/wiki/List_of_system_quality_attributes)
- [Performance Testing](https://www.softwaretestinghelp.com/performance-testing-tutorial/)

### PostgreSQL
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [PostgreSQL ACID](https://www.postgresql.org/docs/current/tutorial-transactions.html)

---

## 📞 การสนับสนุน

หากมีคำถามหรือปัญหา:

1. **ระหว่างข้อสอบ:** ถามผู้คุมสอบเฉพาะปัญหาทางเทคนิค
2. **หลังข้อสอบ:** ติดต่ออาจารย์ผู้สอนเพื่อขอคำอธิบายเพิ่มเติม
3. **Issues ทางเทคนิค:** สร้าง issue ใน Git repository

---

## 📄 License

This exam material is for educational purposes only.

---

## ✅ Checklist สำหรับนักศึกษา

ก่อนเริ่มทำข้อสอบ ตรวจสอบว่า:

- [ ] Docker และ Docker Compose ติดตั้งและทำงานได้
- [ ] Tools ที่จำเป็น (curl, psql, ab, jq) ติดตั้งแล้ว
- [ ] ได้ไฟล์ข้อสอบครบถ้วน
- [ ] เปิดไฟล์ EXAM_WORKSHEET.md เพื่อบันทึกคำตอบ
- [ ] เข้าใจเกณฑ์การให้คะแนนใน EXAM_ASSESSMENT.md
- [ ] รัน `docker-compose up -d` สำเร็จ
- [ ] เข้าถึง http://localhost:3000 ได้
- [ ] ทดสอบการจองตั๋วได้

---

## 🎯 เป้าหมายการเรียนรู้และ Bloom's Taxonomy

| Level | Cognitive Process | จำนวนข้อ | ตัวอย่างคำถาม |
|-------|------------------|---------|---------------|
| 1. Remember | ระบุ, บอก | 5 | ระบุเทคโนโลยีที่ใช้ |
| 2. Understand | อธิบาย, สรุป | 8 | อธิบายความแตกต่างระหว่าง 2-tier และ 3-tier |
| 3. Apply | นำไปใช้, ทดสอบ | 12 | ทดสอบ performance ของระบบ |
| 4. Analyze | วิเคราะห์, เปรียบเทียบ | 10 | วิเคราะห์จุดอ่อนของสถาปัตยกรรม |
| 5. Evaluate | ประเมิน, วิจารณ์ | 8 | ประเมินว่าระบบผ่านมาตรฐานหรือไม่ |
| 6. Create | สร้าง, เสนอแนะ | 7 | เสนอแนวทางปรับปรุงระบบ |

---

**Good Luck! / ขอให้โชคดี!** 🎉
