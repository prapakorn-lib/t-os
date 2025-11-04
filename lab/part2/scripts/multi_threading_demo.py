#!/usr/bin/env python3
"""
โปรแกรม Multi-threading Demo
วัตถุประสงค์: แสดงการทำงานของ threads หลายตัวพร้อมกัน

หมายเหตุ: โปรแกรมนี้ให้อาจารย์แจก นักศึกษาไม่ต้องเขียนเอง
"""

import threading
import time
import random

# ตัวนับสำหรับแสดงผล
counter = 0

def worker_task(worker_id, num_operations):
    """
    งานที่ thread จะทำ
    
    Args:
        worker_id (int): หมายเลข worker
        num_operations (int): จำนวนครั้งที่ทำงาน
    """
    global counter
    
    print(f"🔹 Worker {worker_id} เริ่มทำงาน (Thread ID: {threading.get_ident()})")
    
    for i in range(num_operations):
        # จำลองการทำงาน
        time.sleep(random.uniform(0.1, 0.3))
        counter += 1
        print(f"  Worker {worker_id}: ทำงานครั้งที่ {i+1}/{num_operations}")
    
    print(f"✅ Worker {worker_id} เสร็จสิ้น")


def download_file(file_id):
    """
    จำลองการดาวน์โหลดไฟล์
    
    Args:
        file_id (int): หมายเลขไฟล์
    """
    print(f"📥 เริ่มดาวน์โหลดไฟล์ {file_id}")
    
    # จำลองเวลาดาวน์โหลด
    download_time = random.uniform(1, 3)
    time.sleep(download_time)
    
    print(f"✅ ดาวน์โหลดไฟล์ {file_id} เสร็จสิ้น ({download_time:.2f} วินาที)")


def main():
    """ฟังก์ชันหลักของโปรแกรม"""
    print("=" * 70)
    print("โปรแกรม Multi-threading Demo")
    print("=" * 70)
    
    # ตัวอย่างที่ 1: Worker Threads
    print("\n1️⃣  ตัวอย่าง: Worker Threads")
    print("-" * 70)
    
    num_workers = 3
    operations_per_worker = 3
    threads = []
    
    start_time = time.time()
    
    # สร้าง threads
    for i in range(num_workers):
        thread = threading.Thread(
            target=worker_task,
            args=(i+1, operations_per_worker)
        )
        threads.append(thread)
        thread.start()
    
    # รอให้ threads ทำงานเสร็จ
    for thread in threads:
        thread.join()
    
    elapsed_time = time.time() - start_time
    
    print(f"\n📊 สรุป:")
    print(f"  จำนวน Workers: {num_workers}")
    print(f"  งานต่อ Worker: {operations_per_worker}")
    print(f"  Counter รวม: {counter}")
    print(f"  เวลารวม: {elapsed_time:.2f} วินาที")
    
    # ตัวอย่างที่ 2: Parallel Download
    print("\n2️⃣  ตัวอย่าง: Parallel File Download")
    print("-" * 70)
    
    num_files = 4
    download_threads = []
    
    start_time = time.time()
    
    # สร้าง threads สำหรับดาวน์โหลดแต่ละไฟล์
    for i in range(num_files):
        thread = threading.Thread(target=download_file, args=(i+1,))
        download_threads.append(thread)
        thread.start()
    
    # รอให้ดาวน์โหลดเสร็จทั้งหมด
    for thread in download_threads:
        thread.join()
    
    elapsed_time = time.time() - start_time
    
    print(f"\n📊 สรุป:")
    print(f"  ดาวน์โหลด {num_files} ไฟล์พร้อมกัน")
    print(f"  เวลารวม: {elapsed_time:.2f} วินาที")
    print(f"  (ถ้าดาวน์โหลดทีละไฟล์จะใช้เวลานานกว่า)")
    
    # ตัวอย่างที่ 3: Thread Information
    print("\n3️⃣  ข้อมูล Threading")
    print("-" * 70)
    print(f"  Main Thread ID: {threading.main_thread().ident}")
    print(f"  Active Threads: {threading.active_count()}")
    print(f"  Thread Objects: {threading.enumerate()}")
    
    print("\n" + "=" * 70)
    print("เสร็จสิ้นการทำงาน")
    print("=" * 70)
    
    print("\n💡 สังเกต:")
    print("  - Threads ทำงานพร้อมกัน (concurrent)")
    print("  - ลำดับการทำงานอาจเปลี่ยนในแต่ละครั้ง")
    print("  - เวลารวมน้อยกว่าการทำงานแบบเรียงลำดับ")


if __name__ == "__main__":
    main()
