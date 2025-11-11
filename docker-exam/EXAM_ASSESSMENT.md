# แบบประเมินข้อสอบปฏิบัติ Docker
## ระบบจองตั๋วคอนเสิร์ต (Concert Ticket Booking System)

---

## ส่วนที่ 1: ความเข้าใจเกี่ยวกับสถาปัตยกรรมระบบ (20 คะแนน)

### 1.1 ระบุชนิดของสถาปัตยกรรมที่ใช้ในระบบนี้ (10 คะแนน)

**คำถาม:** ระบบที่ให้มาใช้สถาปัตยกรรมแบบใด อธิบายความหมายและลักษณะเด่นของสถาปัตยกรรมนี้

**หัวข้อที่ต้องตอบ:**
- [ ] ระบุชนิดของสถาปัตยกรรม (2-tier, 3-tier, microservices, etc.)
- [ ] อธิบายความหมายของสถาปัตยกรรมที่ระบุ
- [ ] บอกจำนวน layers/tiers และอธิบายหน้าที่ของแต่ละ layer
- [ ] เปรียบเทียบกับสถาปัตยกรรมแบบอื่น (เช่น 2-tier vs 3-tier)

**เกณฑ์การให้คะแนน:**
- ระบุชนิดถูกต้อง (3 คะแนน)
- อธิบายความหมายชัดเจน (3 คะแนน)
- บอก layers และหน้าที่ได้ถูกต้อง (2 คะแนน)
- เปรียบเทียบได้ถูกต้อง (2 คะแนน)

---

### 1.2 ระบุเทคโนโลยีที่ใช้ในระบบ (10 คะแนน)

**คำถาม:** ระบุและอธิบายเทคโนโลยีที่ใช้ในแต่ละ layer ของระบบ

**หัวข้อที่ต้องตอบ:**
- [ ] Frontend/Presentation Layer: เทคโนโลยีที่ใช้และเหตุผล
- [ ] Backend/Application Layer: เทคโนโลยีที่ใช้และเหตุผล
- [ ] Database/Data Layer: เทคโนโลยีที่ใช้และเหตุผล
- [ ] Container Technology: Docker components ที่ใช้
- [ ] Network: การเชื่อมต่อระหว่าง services

**เกณฑ์การให้คะแนน:**
- ระบุเทคโนโลยีในแต่ละ layer ถูกต้องครบถ้วน (5 คะแนน)
- อธิบายเหตุผลและข้อดีของการใช้เทคโนโลยีแต่ละตัว (3 คะแนน)
- อธิบาย Docker components (docker-compose, network, volumes) (2 คะแนน)

---

## ส่วนที่ 2: Software Quality Attributes Testing (60 คะแนน)

### 2.1 Performance (ประสิทธิภาพ) - 20 คะแนน

#### มาตรฐานที่กำหนด (Performance Benchmarks):
1. **Response Time**: API response time ต้องไม่เกิน 200ms สำหรับ simple queries
2. **Query Performance**: Database query execution time ต้องไม่เกิน 100ms
3. **Concurrent Users**: ระบบต้องรองรับ concurrent requests ได้อย่างน้อย 10 requests พร้อมกัน

#### คำสั่งทดสอบ Performance:

```bash
# 1. ทดสอบ Response Time ของ API
echo "=== Testing API Response Time ==="
for i in {1..10}; do
  curl -w "\nTime: %{time_total}s\n" -s http://localhost:3000/api/concerts | grep -E "(responseTime|Time:)"
done

# 2. ทดสอบ Health Check Response
echo -e "\n=== Testing Health Check ==="
time curl -s http://localhost:3000/health

# 3. ทดสอบ Concurrent Requests (ใช้ Apache Bench หรือ curl loop)
echo -e "\n=== Testing Concurrent Requests ==="
# ติดตั้ง apache2-utils ถ้ายังไม่มี: sudo apt-get install apache2-utils
ab -n 100 -c 10 http://localhost:3000/api/concerts

# หรือใช้ curl แบบ parallel
for i in {1..10}; do
  curl -s http://localhost:3000/api/concerts > /dev/null &
done
wait
echo "Concurrent requests completed"

# 4. ตรวจสอบ Database Query Performance
docker exec concert-database psql -U concert_user -d concert_db -c "\timing on" -c "SELECT * FROM concerts;"
```

#### แบบบันทึกผลการทดสอบ Performance:

| การทดสอบ | มาตรฐาน | ผลที่ได้ | ผ่าน/ไม่ผ่าน | หมายเหตุ |
|---------|---------|----------|-------------|----------|
| API Response Time (avg) | ≤ 200ms | _____ ms | ⬜ ผ่าน / ⬜ ไม่ผ่าน | |
| Health Check Time | ≤ 100ms | _____ ms | ⬜ ผ่าน / ⬜ ไม่ผ่าน | |
| Concurrent Requests (10 req) | Success rate ≥ 95% | _____ % | ⬜ ผ่าน / ⬜ ไม่ผ่าน | |
| Database Query Time | ≤ 100ms | _____ ms | ⬜ ผ่าน / ⬜ ไม่ผ่าน | |

**คำถาม:**
1. ระบบผ่านมาตรฐาน Performance ที่กำหนดหรือไม่? เพราะอะไร?
2. หากไม่ผ่าน ควรแก้ไขตรงไหนและอย่างไร? (ให้แนวทางอย่างน้อย 3 ข้อ)
3. คุณจะปรับปรุง Performance ของระบบอย่างไร?

**เกณฑ์การให้คะแนน:**
- ทดสอบและบันทึกผลถูกต้องครบถ้วน (8 คะแนน)
- วิเคราะห์ผลและตอบคำถามถูกต้อง (8 คะแนน)
- เสนอแนวทางแก้ไขหรือปรับปรุงที่เหมาะสม (4 คะแนน)

---

### 2.2 Availability (ความพร้อมใช้งาน) - 20 คะแนน

#### มาตรฐานที่กำหนด (Availability Requirements):
1. **Uptime**: Services ต้องรันได้ต่อเนื่องโดยไม่ crash
2. **Health Check**: Health endpoint ต้องตอบกลับ status 200 และข้อมูลที่ถูกต้อง
3. **Auto-restart**: Services ต้อง auto-restart เมื่อเกิดข้อผิดพลาด
4. **Database Connectivity**: ต้องเชื่อมต่อ database ได้ตลอดเวลา

#### คำสั่งทดสอบ Availability:

```bash
# 1. ตรวจสอบ Container Status
echo "=== Checking Container Status ==="
docker-compose ps

# 2. ทดสอบ Health Check
echo -e "\n=== Testing Health Endpoint ==="
curl -i http://localhost:3000/health

# 3. ตรวจสอบ Restart Policy
echo -e "\n=== Checking Restart Policies ==="
docker inspect concert-frontend | grep -A 5 RestartPolicy
docker inspect concert-database | grep -A 5 RestartPolicy

# 4. ทดสอบ Auto-restart (จำลองการ crash)
echo -e "\n=== Testing Auto-restart ==="
echo "Stopping frontend container..."
docker stop concert-frontend
sleep 5
echo "Checking if container restarted..."
docker-compose ps

# 5. ทดสอบ Database Health Check
echo -e "\n=== Testing Database Health ==="
docker exec concert-database pg_isready -U concert_user -d concert_db

# 6. ตรวจสอบ Logs สำหรับ errors
echo -e "\n=== Checking Container Logs ==="
docker-compose logs --tail=50 frontend
docker-compose logs --tail=50 database

# 7. Uptime Test (รัน 1 นาที)
echo -e "\n=== Continuous Availability Test (60 seconds) ==="
end=$((SECONDS+60))
success=0
fail=0
while [ $SECONDS -lt $end ]; do
  if curl -s http://localhost:3000/health > /dev/null; then
    ((success++))
  else
    ((fail++))
  fi
  sleep 2
done
echo "Success: $success, Failed: $fail"
echo "Availability: $(echo "scale=2; $success / ($success + $fail) * 100" | bc)%"
```

#### แบบบันทึกผลการทดสอบ Availability:

| การทดสอบ | มาตรฐาน | ผลที่ได้ | ผ่าน/ไม่ผ่าน | หมายเหตุ |
|---------|---------|----------|-------------|----------|
| Container Status | All running | _______ | ⬜ ผ่าน / ⬜ ไม่ผ่าน | |
| Health Check Response | Status 200 | HTTP _____ | ⬜ ผ่าน / ⬜ ไม่ผ่าน | |
| Restart Policy | unless-stopped | _______ | ⬜ ผ่าน / ⬜ ไม่ผ่าน | |
| Auto-restart Test | Restarts automatically | _______ | ⬜ ผ่าน / ⬜ ไม่ผ่าน | |
| Database Health | Ready | _______ | ⬜ ผ่าน / ⬜ ไม่ผ่าน | |
| Continuous Availability | ≥ 99% | _____ % | ⬜ ผ่าน / ⬜ ไม่ผ่าน | |

**คำถาม:**
1. ระบบมีความพร้อมใช้งานตามมาตรฐานหรือไม่?
2. Restart policy ที่ใช้คืออะไร และเหมาะสมกับระบบหรือไม่?
3. หากต้องการเพิ่มความพร้อมใช้งานเป็น 99.9% ควรทำอย่างไร?

**เกณฑ์การให้คะแนน:**
- ทดสอบและบันทึกผลถูกต้องครบถ้วน (8 คะแนน)
- วิเคราะห์ผลและตอบคำถามถูกต้อง (8 คะแนน)
- เสนอแนวทางเพิ่ม availability ที่เหมาะสม (4 คะแนน)

---

### 2.3 Reliability (ความน่าเชื่อถือ) - 20 คะแนน

#### มาตรฐานที่กำหนด (Reliability Requirements):
1. **Data Integrity**: Transaction ต้องทำงานแบบ ACID compliant
2. **Concurrent Booking**: ป้องกัน double booking (race condition)
3. **Data Consistency**: ข้อมูลต้องสอดคล้องกันระหว่าง tables
4. **Error Handling**: ระบบต้องจัดการ error ได้อย่างเหมาะสม

#### คำสั่งทดสอบ Reliability:

```bash
# 1. ทดสอบ Transaction (ACID Properties)
echo "=== Testing Transaction Integrity ==="
docker exec concert-database psql -U concert_user -d concert_db << EOF
BEGIN;
-- Try to book more tickets than available
UPDATE concerts SET sold_tickets = sold_tickets + 100 WHERE id = 1;
SELECT concert_name, total_tickets, sold_tickets,
       (total_tickets - sold_tickets) as available
FROM concerts WHERE id = 1;
-- This should fail due to constraint
ROLLBACK;
SELECT 'Transaction rolled back successfully' as result;
EOF

# 2. ทดสอบ Data Integrity Constraints
echo -e "\n=== Testing Data Integrity ==="
docker exec concert-database psql -U concert_user -d concert_db << EOF
-- Try to insert invalid data (negative tickets)
INSERT INTO bookings (concert_id, customer_name, customer_email, quantity)
VALUES (1, 'Test User', 'test@test.com', -1);
EOF

# 3. ทดสอบ Concurrent Booking (Race Condition)
echo -e "\n=== Testing Concurrent Booking ==="
# สร้างไฟล์ test script
cat > /tmp/test_booking.sh << 'SCRIPT'
#!/bin/bash
curl -X POST http://localhost:3000/api/book \
  -H "Content-Type: application/json" \
  -d '{
    "concert_id": 5,
    "customer_name": "Test User '$1'",
    "customer_email": "test'$1'@email.com",
    "quantity": 1
  }' &
SCRIPT

chmod +x /tmp/test_booking.sh

# รัน 5 bookings พร้อมกัน สำหรับคอนเสิร์ตที่เหลือ 1 ตั๋ว
for i in {1..5}; do
  /tmp/test_booking.sh $i
done
wait

# ตรวจสอบผลลัพธ์
echo -e "\n=== Checking Results ==="
curl -s http://localhost:3000/api/concerts/5 | grep -E "(available_tickets|sold_tickets)"

# 4. ทดสอบ Data Consistency
echo -e "\n=== Testing Data Consistency ==="
docker exec concert-database psql -U concert_user -d concert_db << EOF
-- ตรวจสอบว่า sold_tickets ตรงกับจำนวน bookings
SELECT
  c.id,
  c.concert_name,
  c.sold_tickets,
  COALESCE(SUM(b.quantity), 0) as total_booked,
  CASE
    WHEN c.sold_tickets = COALESCE(SUM(b.quantity), 0)
    THEN 'CONSISTENT'
    ELSE 'INCONSISTENT'
  END as status
FROM concerts c
LEFT JOIN bookings b ON c.id = b.concert_id
GROUP BY c.id, c.concert_name, c.sold_tickets;
EOF

# 5. ทดสอบ Error Handling
echo -e "\n=== Testing Error Handling ==="
# ลอง book คอนเสิร์ตที่ไม่มี
curl -i -X POST http://localhost:3000/api/book \
  -H "Content-Type: application/json" \
  -d '{
    "concert_id": 999,
    "customer_name": "Test User",
    "customer_email": "test@email.com",
    "quantity": 1
  }'

# ลอง book เกินจำนวนที่มี
curl -i -X POST http://localhost:3000/api/book \
  -H "Content-Type: application/json" \
  -d '{
    "concert_id": 1,
    "customer_name": "Test User",
    "customer_email": "test@email.com",
    "quantity": 99999
  }'

# 6. ทดสอบ Database Backup/Recovery
echo -e "\n=== Testing Data Persistence ==="
echo "Creating backup..."
docker exec concert-database pg_dump -U concert_user concert_db > /tmp/backup.sql
echo "Backup created: $(wc -l < /tmp/backup.sql) lines"
```

#### แบบบันทึกผลการทดสอบ Reliability:

| การทดสอบ | มาตรฐาน | ผลที่ได้ | ผ่าน/ไม่ผ่าน | หมายเหตุ |
|---------|---------|----------|-------------|----------|
| Transaction Rollback | Works correctly | _______ | ⬜ ผ่าน / ⬜ ไม่ผ่าน | |
| Data Constraints | Enforced properly | _______ | ⬜ ผ่าน / ⬜ ไม่ผ่าน | |
| Concurrent Booking | No double booking | _______ | ⬜ ผ่าน / ⬜ ไม่ผ่าน | |
| Data Consistency | All data consistent | _______ | ⬜ ผ่าน / ⬜ ไม่ผ่าน | |
| Error Handling | Proper error messages | _______ | ⬜ ผ่าน / ⬜ ไม่ผ่าน | |
| Data Persistence | Backup successful | _______ | ⬜ ผ่าน / ⬜ ไม่ผ่าน | |

**คำถาม:**
1. ระบบป้องกัน race condition ในการ book ตั๋วได้หรือไม่? อธิบายกลไก
2. ACID properties ใดบ้างที่ระบบรองรับ? ยกตัวอย่างประกอบ
3. หากพบ data inconsistency ควรแก้ไขอย่างไร?

**เกณฑ์การให้คะแนน:**
- ทดสอบและบันทึกผลถูกต้องครบถ้วน (8 คะแนน)
- วิเคราะห์ผลและตอบคำถามถูกต้อง (8 คะแนน)
- เสนอแนวทางแก้ไขปัญหาที่เหมาะสม (4 คะแนน)

---

## ส่วนที่ 3: การปรับปรุงและพัฒนาระบบ (20 คะแนน)

### 3.1 วิเคราะห์จุดอ่อนของสถาปัตยกรรมปัจจุบัน (10 คะแนน)

**คำถาม:**
1. ระบุจุดอ่อนของสถาปัตยกรรม 2-tier ที่ใช้ในระบบนี้ (อย่างน้อย 3 ข้อ)
2. ปัญหาใดบ้างที่อาจเกิดขึ้นเมื่อระบบมีผู้ใช้งานเพิ่มขึ้นมาก?
3. เปรียบเทียบข้อดี-ข้อเสียกับสถาปัตยกรรมแบบอื่น

**เกณฑ์การให้คะแนน:**
- ระบุจุดอ่อนได้ถูกต้องและชัดเจน (4 คะแนน)
- วิเคราะห์ปัญหาที่อาจเกิดได้ครบถ้วน (3 คะแนน)
- เปรียบเทียบได้ถูกต้อง (3 คะแนน)

---

### 3.2 เสนอแนวทางปรับปรุงระบบ (10 คะแนน)

**คำถาม:**
1. หากต้องการอัพเกรดเป็น 3-tier architecture ควรทำอย่างไร?
2. เสนอแนวทางเพิ่ม scalability ของระบบ
3. เสนอแนวทางเพิ่ม security ของระบบ

**เกณฑ์การให้คะแนน:**
- เสนอแนวทาง upgrade เป็น 3-tier ได้ถูกต้อง (4 คะแนน)
- เสนอแนวทางเพิ่ม scalability เหมาะสม (3 คะแนน)
- เสนอแนวทางเพิ่ม security เหมาะสม (3 คะแนน)

---

## สรุปคะแนน

| หมวด | คะแนนเต็ม | คะแนนที่ได้ |
|------|----------|------------|
| ส่วนที่ 1: ความเข้าใจสถาปัตยกรรม | 20 | |
| ส่วนที่ 2.1: Performance Testing | 20 | |
| ส่วนที่ 2.2: Availability Testing | 20 | |
| ส่วนที่ 2.3: Reliability Testing | 20 | |
| ส่วนที่ 3: การปรับปรุงระบบ | 20 | |
| **รวม** | **100** | |

---

## หมายเหตุสำหรับผู้สอบ

1. ให้รัน `docker-compose up -d` ก่อนทำการทดสอบ
2. ตรวจสอบให้แน่ใจว่า services ทั้งหมดรันปกติ (`docker-compose ps`)
3. บันทึกผลการทดสอบทุกครั้งด้วย screenshot หรือ log file
4. เมื่อทดสอบเสร็จให้รัน `docker-compose down` เพื่อหยุด services
5. หากมีปัญหาในการทดสอบ ให้ดู logs ด้วย `docker-compose logs`

---

## คำแนะนำเพิ่มเติม

### การติดตั้ง Tools ที่จำเป็น

```bash
# Apache Bench (สำหรับ load testing)
sudo apt-get install apache2-utils

# PostgreSQL Client (สำหรับทดสอบ database)
sudo apt-get install postgresql-client

# jq (สำหรับ parse JSON)
sudo apt-get install jq

# curl (มักมีติดตั้งอยู่แล้ว)
sudo apt-get install curl
```

### การดู Logs

```bash
# ดู logs ของ frontend
docker-compose logs -f frontend

# ดู logs ของ database
docker-compose logs -f database

# ดู logs ทั้งหมด
docker-compose logs -f
```

### การ Restart Services

```bash
# Restart service เดียว
docker-compose restart frontend

# Restart ทั้งหมด
docker-compose restart

# Stop และ Start ใหม่
docker-compose down && docker-compose up -d
```
