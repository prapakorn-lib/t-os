#!/usr/bin/env python3
"""
โปรแกรม Race Condition Fixed
วัตถุประสงค์: แก้ไขปัญหา Race Condition ด้วย Lock

หมายเหตุ: โปรแกรมนี้ให้อาจารย์แจก นักศึกษาไม่ต้องเขียนเอง
"""

import threading
import time

# ตัวแปรที่ใช้ร่วมกัน (shared variable)
shared_counter = 0

# Lock สำหรับป้องกัน race condition
counter_lock = threading.Lock()

def increment_counter_safe(thread_id, num_increments):
    """
    เพิ่มค่า counter แบบปลอดภัย (มีการป้องกัน race condition)
    
    Args:
        thread_id (int): หมายเลข thread
        num_increments (int): จำนวนครั้งที่เพิ่มค่า
    """
    global shared_counter
    
    print(f"Thread {thread_id} เริ่มทำงาน")
    
    for i in range(num_increments):
        # ใช้ Lock เพื่อป้องกัน race condition
        with counter_lock:
            # Critical Section: มีเพียง thread เดียวเท่านั้นที่เข้าได้
            current_value = shared_counter
            time.sleep(0.0001)  # จำลองการประมวลผล
            shared_counter = current_value + 1
    
    print(f"Thread {thread_id} เสร็จสิ้น")


def main():
    """ฟังก์ชันหลักของโปรแกรม"""
    global shared_counter
    
    print("=" * 70)
    print("โปรแกรม Race Condition Fixed")
    print("=" * 70)
    
    print("\n✅ โปรแกรมนี้แก้ไข Race Condition แล้ว!")
    print("   ใช้ Lock เพื่อป้องกันการเข้าถึงตัวแปรพร้อมกัน")
    
    # ทดสอบหลายครั้ง
    num_tests = 3
    num_threads = 5
    increments_per_thread = 1000
    
    for test_num in range(1, num_tests + 1):
        print(f"\n{'=' * 70}")
        print(f"การทดสอบครั้งที่ {test_num}")
        print("=" * 70)
        
        # รีเซ็ต counter
        shared_counter = 0
        
        # คำนวณค่าที่คาดหวัง
        expected_value = num_threads * increments_per_thread
        
        print(f"\nตั้งค่า:")
        print(f"  จำนวน Threads: {num_threads}")
        print(f"  การเพิ่มค่าต่อ Thread: {increments_per_thread}")
        print(f"  ค่าที่คาดหวัง: {expected_value}")
        
        threads = []
        
        # สร้างและเริ่ม threads
        print(f"\n🚀 เริ่มทำงาน...")
        start_time = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(
                target=increment_counter_safe,
                args=(i+1, increments_per_thread)
            )
            threads.append(thread)
            thread.start()
        
        # รอให้ threads ทำงานเสร็จ
        for thread in threads:
            thread.join()
        
        elapsed_time = time.time() - start_time
        
        # แสดงผลลัพธ์
        print(f"\n📊 ผลลัพธ์:")
        print(f"  ค่าที่คาดหวัง: {expected_value}")
        print(f"  ค่าที่ได้จริง: {shared_counter}")
        print(f"  ส่วนต่าง: {expected_value - shared_counter}")
        print(f"  เวลาที่ใช้: {elapsed_time:.4f} วินาที")
        
        if shared_counter == expected_value:
            print(f"\n✅ ค่าถูกต้อง! Lock ทำงานได้ดี")
        else:
            print(f"\n⚠️  ค่าไม่ถูกต้อง (ไม่ควรเกิด)")
    
    # สรุป
    print(f"\n{'=' * 70}")
    print("สรุปการแก้ไข Race Condition")
    print("=" * 70)
    
    print("\n🔐 วิธีแก้ไข:")
    print("  1. ใช้ threading.Lock()")
    print("  2. Lock ก่อนเข้า Critical Section")
    print("  3. Unlock หลังออกจาก Critical Section")
    print("  4. ใช้ 'with lock:' เพื่อ unlock อัตโนมัติ")
    
    print("\n💡 Critical Section คือ:")
    print("  ส่วนของโค้ดที่เข้าถึง shared variable")
    print("  มีเพียง thread เดียวเท่านั้นที่เข้าได้ในแต่ละครั้ง")
    
    print("\n⚖️ Trade-off:")
    print("  ✅ ข้อดี: ค่าถูกต้อง 100%")
    print("  ⚠️  ข้อเสีย: ช้ากว่าเล็กน้อย (threads ต้องรอกัน)")
    
    print("\n📚 Synchronization Mechanisms อื่นๆ:")
    print("  - Semaphore: จำกัดจำนวน threads")
    print("  - RLock: Lock ซ้อน (reentrant)")
    print("  - Condition: รอ event")
    print("  - Event: signal ระหว่าง threads")
    
    print("\n" + "=" * 70)
    print("เสร็จสิ้นการทำงาน")
    print("=" * 70)


if __name__ == "__main__":
    main()
