"""
threading_demo.py
-----------------
โปรแกรมสาธิตการทำงานของ Multi-threading
นักศึกษา: รันโปรแกรมนี้และสังเกตผลที่ได้
"""

import threading
import time
import random

# ตัวแปรร่วม (shared variable)
counter = 0

def worker_task(thread_id, task_count):
    """ฟังก์ชันที่แต่ละ thread จะทำงาน"""
    global counter
    print(f"[Thread {thread_id}] เริ่มทำงาน...")
    
    for i in range(task_count):
        # จำลองการทำงานที่ใช้เวลาต่างกัน
        sleep_time = random.uniform(0.1, 0.5)
        time.sleep(sleep_time)
        counter += 1
        print(f"[Thread {thread_id}] งานที่ {i+1}/{task_count} เสร็จแล้ว (รอ {sleep_time:.2f}s)")
    
    print(f"[Thread {thread_id}] ✓ เสร็จสิ้นทุกงานแล้ว")


def main():
    print("=" * 50)
    print("  Multi-threading Demo")
    print("=" * 50)
    
    NUM_THREADS = 3
    TASKS_PER_THREAD = 3
    
    print(f"\nกำลังสร้าง {NUM_THREADS} threads, แต่ละ thread ทำ {TASKS_PER_THREAD} งาน\n")
    
    start_time = time.time()
    
    # สร้าง threads
    threads = []
    for i in range(1, NUM_THREADS + 1):
        t = threading.Thread(target=worker_task, args=(i, TASKS_PER_THREAD))
        threads.append(t)
    
    # เริ่ม threads ทั้งหมดพร้อมกัน
    for t in threads:
        t.start()
    
    # รอให้ทุก thread เสร็จ
    for t in threads:
        t.join()
    
    end_time = time.time()
    
    print("\n" + "=" * 50)
    print(f"  ผลสรุป")
    print("=" * 50)
    print(f"  จำนวน threads ที่สร้าง : {NUM_THREADS}")
    print(f"  งานทั้งหมด             : {NUM_THREADS * TASKS_PER_THREAD}")
    print(f"  counter สุดท้าย        : {counter}")
    print(f"  เวลาที่ใช้ทั้งหมด      : {end_time - start_time:.2f} วินาที")
    print("=" * 50)
    print("\nสังเกต: ลำดับการพิมพ์ของแต่ละ thread อาจไม่เหมือนกันทุกครั้งที่รัน")
    print("เพราะ threads ทำงานพร้อมกัน (concurrent execution)\n")


if __name__ == "__main__":
    main()
