# แบบประเมินข้อสอบปฏิบัติ Docker
## ระบบจองตั๋วคอนเสิร์ต (Concert Ticket Booking System)

---

## ส่วนที่ 1: ความเข้าใจเกี่ยวกับสถาปัตยกรรมระบบ (20 คะแนน)

### 1.1 ระบุชนิดของสถาปัตยกรรมที่ใช้ในระบบนี้ (10 คะแนน)

**คำถามที่ 1:** ระบบที่ให้มาใช้สถาปัตยกรรมแบบใด (2-tier, 3-tier, microservices)?

**คำถามที่ 2:** อธิบายความหมายของสถาปัตยกรรมที่ระบุ

**คำถามที่ 3:** ระบบนี้มีกี่ layers/tiers และหน้าที่ของแต่ละ layer คืออะไร?

**คำถามที่ 4:** เปรียบเทียบข้อดี-ข้อเสียของสถาปัตยกรรมที่ใช้กับสถาปัตยกรรมแบบ 3-tier

---

### 1.2 ระบุเทคโนโลยีที่ใช้ในระบบ (10 คะแนน)

**คำถามที่ 5:** Frontend/Presentation Layer ใช้เทคโนโลยีอะไร และเพราะเหตุใด?

**คำถามที่ 6:** Backend/Application Layer ใช้เทคโนโลยีอะไร และเพราะเหตุใด?

**คำถามที่ 7:** Database Layer ใช้เทคโนโลยีอะไร และเพราะเหตุใด?

**คำถามที่ 8:** อธิบาย Docker components ที่ใช้ในระบบ (images, networks, volumes)

**คำถามที่ 9:** อธิบายการเชื่อมต่อระหว่าง services ในระบบ

---

## ส่วนที่ 2: Software Quality Attributes Testing (60 คะแนน)

### 2.1 Performance Testing (ประสิทธิภาพ) - 20 คะแนน

**มาตรฐานที่กำหนด:**
- API response time ≤ 200ms
- Database query time ≤ 100ms
- รองรับ concurrent requests อย่างน้อย 10 requests พร้อมกัน

**คำสั่งทดสอบ:**

```bash
# ทดสอบ API Response Time
for i in {1..10}; do
  curl -w "\nTime: %{time_total}s\n" -s http://localhost:3000/api/concerts
done

# ทดสอบ Concurrent Requests
ab -n 100 -c 10 http://localhost:3000/api/concerts

# ทดสอบ Database Query
docker exec concert-database psql -U concert_user -d concert_db -c "\timing on" -c "SELECT * FROM concerts;"
```

**คำถามที่ 10:** บันทึกผลการทดสอบ API Response Time (ค่าเฉลี่ย)

**คำถามที่ 11:** บันทึกผลการทดสอบ Database Query Time

**คำถามที่ 12:** บันทึกผลการทดสอบ Concurrent Requests (success rate)

**คำถามที่ 13:** ระบบผ่านมาตรฐาน Performance ที่กำหนดหรือไม่? เพราะอะไร?

**คำถามที่ 14:** หากไม่ผ่าน ควรแก้ไขตรงไหนและอย่างไร? (ให้แนวทางอย่างน้อย 3 ข้อ)

**คำถามที่ 15:** คุณจะปรับปรุง Performance ของระบบอย่างไร?

---

### 2.2 Availability Testing (ความพร้อมใช้งาน) - 20 คะแนน

**มาตรฐานที่กำหนด:**
- Services ต้องรันได้ต่อเนื่อง
- Health endpoint ตอบกลับ status 200
- Auto-restart เมื่อเกิดข้อผิดพลาด
- Availability ≥ 99%

**คำสั่งทดสอบ:**

```bash
# ตรวจสอบ Container Status
docker-compose ps

# ทดสอบ Health Check
curl -i http://localhost:3000/health

# ทดสอบ Auto-restart
docker stop concert-frontend
sleep 5
docker-compose ps

# ทดสอบ Database Health
docker exec concert-database pg_isready -U concert_user -d concert_db

# ทดสอบ Continuous Availability (60 วินาที)
./scripts/test_availability.sh
```

**คำถามที่ 16:** บันทึกสถานะของ containers ทั้งหมด

**คำถามที่ 17:** บันทึกผลการทดสอบ Health Check (HTTP status code และ response time)

**คำถามที่ 18:** Restart policy ที่ระบบใช้คืออะไร?

**คำถามที่ 19:** Container restart อัตโนมัติหลังจาก stop หรือไม่?

**คำถามที่ 20:** บันทึก Availability percentage จากการทดสอบ 60 วินาที

**คำถามที่ 21:** ระบบมีความพร้อมใช้งานตามมาตรฐานหรือไม่?

**คำถามที่ 22:** Restart policy ที่ใช้เหมาะสมกับระบบหรือไม่? เพราะอะไร?

**คำถามที่ 23:** หากต้องการเพิ่มความพร้อมใช้งานเป็น 99.9% ควรทำอย่างไร?

---

### 2.3 Reliability Testing (ความน่าเชื่อถือ) - 20 คะแนน

**มาตรฐานที่กำหนด:**
- Transaction ทำงานแบบ ACID compliant
- ป้องกัน double booking
- Data consistency ระหว่าง tables
- Error handling ที่เหมาะสม

**คำสั่งทดสอบ:**

```bash
# ทดสอบ Transaction Integrity
docker exec concert-database psql -U concert_user -d concert_db << EOF
BEGIN;
UPDATE concerts SET sold_tickets = total_tickets + 1000 WHERE id = 1;
ROLLBACK;
EOF

# ทดสอบ Concurrent Booking
for i in {1..5}; do
  curl -X POST http://localhost:3000/api/book \
    -H "Content-Type: application/json" \
    -d '{"concert_id": 5, "customer_name": "User '$i'",
         "customer_email": "user'$i'@test.com", "quantity": 1}' &
done
wait

# ทดสอบ Data Consistency
docker exec concert-database psql -U concert_user -d concert_db << EOF
SELECT c.id, c.sold_tickets, COALESCE(SUM(b.quantity), 0) as total_booked
FROM concerts c
LEFT JOIN bookings b ON c.id = b.concert_id
GROUP BY c.id, c.sold_tickets;
EOF

# ทดสอบ Error Handling
curl -X POST http://localhost:3000/api/book \
  -H "Content-Type: application/json" \
  -d '{"concert_id": 999, "customer_name": "Test", "customer_email": "test@test.com", "quantity": 1}'
```

**คำถามที่ 24:** บันทึกผลการทดสอบ Transaction Rollback (rollback สำเร็จหรือไม่)

**คำถามที่ 25:** บันทึกผลการทดสอบ Concurrent Booking (มีกี่ booking ที่สำเร็จ ควรเป็น 1 เท่านั้น)

**คำถามที่ 26:** บันทึกผลการตรวจสอบ Data Consistency (มี inconsistency หรือไม่)

**คำถามที่ 27:** บันทึก error message จากการ book concert ที่ไม่มี

**คำถามที่ 28:** ระบบป้องกัน race condition ในการ book ตั๋วได้หรือไม่? อธิบายกลไก

**คำถามที่ 29:** ACID properties ใดบ้างที่ระบบรองรับ? ยกตัวอย่างประกอบ
- Atomicity:
- Consistency:
- Isolation:
- Durability:

**คำถามที่ 30:** หากพบ data inconsistency ควรแก้ไขอย่างไร?

---

## ส่วนที่ 3: การปรับปรุงและพัฒนาระบบ (20 คะแนน)

### 3.1 วิเคราะห์จุดอ่อนของสถาปัตยกรรมปัจจุบัน (10 คะแนน)

**คำถามที่ 31:** ระบุจุดอ่อนของสถาปัตยกรรม 2-tier ที่ใช้ในระบบนี้ (อย่างน้อย 3 ข้อ)

**คำถามที่ 32:** ปัญหาใดบ้างที่อาจเกิดขึ้นเมื่อระบบมีผู้ใช้งานเพิ่มขึ้นมาก?
- Scalability issues:
- Performance issues:
- Maintenance issues:

**คำถามที่ 33:** เปรียบเทียบข้อดี-ข้อเสียของ 2-tier กับ 3-tier architecture
- ข้อดีของ 2-tier:
- ข้อเสียของ 2-tier:
- ข้อดีของ 3-tier:
- ข้อเสียของ 3-tier:

---

### 3.2 เสนอแนวทางปรับปรุงระบบ (10 คะแนน)

**คำถามที่ 34:** หากต้องการอัพเกรดเป็น 3-tier architecture ควรทำอย่างไร? (อธิบายขั้นตอน)

**คำถามที่ 35:** เสนอแนวทางเพิ่ม Scalability ของระบบ (อย่างน้อย 3 วิธี)
- วิธีที่ 1:
- วิธีที่ 2:
- วิธีที่ 3:

**คำถามที่ 36:** เสนอแนวทางเพิ่ม Security ของระบบ (อย่างน้อย 5 ข้อ)
- Frontend security:
- Backend security:
- Database security:
- Network security:
- Container security:

---

## สรุปคะแนน

**คะแนนเต็ม: 100 คะแนน**

- ส่วนที่ 1: ความเข้าใจสถาปัตยกรรม (คำถามที่ 1-9) = 20 คะแนน
- ส่วนที่ 2.1: Performance Testing (คำถามที่ 10-15) = 20 คะแนน
- ส่วนที่ 2.2: Availability Testing (คำถามที่ 16-23) = 20 คะแนน
- ส่วนที่ 2.3: Reliability Testing (คำถามที่ 24-30) = 20 คะแนน
- ส่วนที่ 3: การปรับปรุงระบบ (คำถามที่ 31-36) = 20 คะแนน

---

## เกณฑ์การให้คะแนนแต่ละคำถาม

### ส่วนที่ 1 (คำถามละ 2-3 คะแนน)
- คำถาม 1-4: คำถามละ 2-3 คะแนน (รวม 10 คะแนน)
- คำถาม 5-9: คำถามละ 2 คะแนน (รวม 10 คะแนน)

### ส่วนที่ 2.1 Performance (รวม 20 คะแนน)
- คำถาม 10-12: บันทึกผลถูกต้อง คำถามละ 2 คะแนน (6 คะแนน)
- คำถาม 13: วิเคราะห์ผ่าน/ไม่ผ่าน (4 คะแนน)
- คำถาม 14: เสนอแนวทางแก้ไข 3 ข้อ (6 คะแนน)
- คำถาม 15: เสนอแนวทางปรับปรุง (4 คะแนน)

### ส่วนที่ 2.2 Availability (รวม 20 คะแนน)
- คำถาม 16-20: บันทึกผลถูกต้อง คำถามละ 2 คะแนน (10 คะแนน)
- คำถาม 21-22: วิเคราะห์ผล คำถามละ 3 คะแนน (6 คะแนน)
- คำถาม 23: เสนอแนวทาง (4 คะแนน)

### ส่วนที่ 2.3 Reliability (รวม 20 คะแนน)
- คำถาม 24-27: บันทึกผลถูกต้อง คำถามละ 2 คะแนน (8 คะแนน)
- คำถาม 28: อธิบายกลไกป้องกัน race condition (4 คะแนน)
- คำถาม 29: อธิบาย ACID properties (4 คะแนน)
- คำถาม 30: เสนอแนวทางแก้ไข (4 คะแนน)

### ส่วนที่ 3 การปรับปรุงระบบ (รวม 20 คะแนน)
- คำถาม 31: ระบุจุดอ่อน 3 ข้อ (4 คะแนน)
- คำถาม 32: วิเคราะห์ปัญหา (3 คะแนน)
- คำถาม 33: เปรียบเทียบ architecture (3 คะแนน)
- คำถาม 34: แผน upgrade เป็น 3-tier (4 คะแนน)
- คำถาม 35: เสนอแนวทางเพิ่ม scalability (3 คะแนน)
- คำถาม 36: เสนอแนวทางเพิ่ม security (3 คะแนน)

---

## หมายเหตุสำหรับผู้ตรวจ

1. การทดสอบใน Part 2 ต้องมีหลักฐาน (screenshots หรือ log output)
2. คำตอบที่ดีควรมีการวิเคราะห์และให้เหตุผลประกอบ
3. คะแนนเต็มต้องแสดงความเข้าใจลึกและให้รายละเอียดครบถ้วน
4. คะแนนผ่าน: 60 คะแนนขึ้นไป (60%)

---

## เฉลยคำถามสำหรับผู้สอน

**คำถามที่ 1:** 2-Tier Architecture (Client-Server)

**คำถามที่ 2:** สถาปัตยกรรมที่แบ่งระบบออกเป็น 2 ชั้น คือ Frontend (Client) และ Database (Server) โดย business logic อยู่ที่ Frontend

**คำถามที่ 3:**
- Tier 1: Frontend (Node.js + Express) - รับคำร้อง, business logic, presentation
- Tier 2: Database (PostgreSQL) - จัดเก็บข้อมูล

**คำถามที่ 4:**
- 2-tier: ง่าย, พัฒนาเร็ว, แต่ scale ยาก, maintain ยาก
- 3-tier: แยก business logic ออกมา, scale ง่าย, แต่ซับซ้อนกว่า

**คำถามที่ 5:** Node.js + Express - เบา, รวดเร็ว, JavaScript ทั้งระบบ

**คำถามที่ 6:** รวมอยู่ใน Frontend (Express.js) - ทำ REST API

**คำถามที่ 7:** PostgreSQL - Open source, ACID compliant, รองรับ transaction

**คำถามที่ 8:** Docker Compose, Networks (bridge), Volumes (persistent data)

**คำถามที่ 9:** ผ่าน Docker network, Frontend เชื่อม Database ด้วย service name

**คำถามที่ 28:** ใช่, ใช้ SELECT FOR UPDATE (row-level locking) ใน transaction

**คำถามที่ 29:**
- A: Transaction rollback เมื่อ error
- C: Constraints ป้องกันข้อมูลผิดพลาด
- I: Row-level locking
- D: Volume persistent data

**คำถามที่ 31:**
1. Business logic ผสม presentation logic
2. Scale ยาก (ต้อง scale ทั้ง frontend)
3. Maintenance ยาก
4. Security ระดับต่ำกว่า 3-tier

**คำถามที่ 34:** แยก API layer ออกมาเป็น Tier กลาง ระหว่าง Frontend กับ Database

**คำถามที่ 35:**
1. Load Balancer
2. Database Replication
3. Horizontal scaling with multiple containers
4. Caching (Redis)

**คำถามที่ 36:**
1. HTTPS/TLS
2. JWT Authentication
3. Rate limiting
4. Input validation
5. Database encryption
6. Docker secrets
7. Network policies
