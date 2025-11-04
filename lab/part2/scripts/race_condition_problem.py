#!/usr/bin/env python3
"""
โปรแกรม Race Condition Problem
วัตถุประสงค์: แสดงปัญหา Race Condition เมื่อหลาย threads เข้าถึงตัวแปรเดียวกัน

หมายเหตุ: โปรแกรมนี้ให้อาจารย์แจก นักศึกษาไม่ต้องเขียนเอง
"""

import threading
import time

# ตัวแปรที่ใช้ร่วมกัน (shared variable)
shared_counter = 0

def increment_counter(thread_id, num_increments):
    """
    เพิ่มค่า counter (ไม่มีการป้องกัน race condition)
    
    Args:
        thread_id (int): หมายเลข thread
        num_increments (int): จำนวนครั้งที่เพิ่มค่า
    """
    global shared_counter
    
    print(f"Thread {thread_id} เริ่มทำงาน")
    
    for i in range(num_increments):
        # อ่านค่าปัจจุบัน
        current_value = shared_counter
        
        # จำลองการประมวลผล (ทำให้เกิด race condition ง่ายขึ้น)
        time.sleep(0.0001)
        
        # เขียนค่าใหม่
        shared_counter = current_value + 1
    
    print(f"Thread {thread_id} เสร็จสิ้น")


def main():
    """ฟังก์ชันหลักของโปรแกรม"""
    global shared_counter
    
    print("=" * 70)
    print("โปรแกรม Race Condition Problem")
    print("=" * 70)
    
    print("\n⚠️  โปรแกรมนี้มี Race Condition (บั๊ก)!")
    print("   หลาย threads เข้าถึงตัวแปรเดียวกันโดยไม่มีการป้องกัน")
    
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
                target=increment_counter,
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
        
        if shared_counter != expected_value:
            print(f"\n❌ เกิด Race Condition! ค่าไม่ถูกต้อง")
            print(f"   สูญหาย: {expected_value - shared_counter} ครั้ง")
        else:
            print(f"\n✅ ค่าถูกต้อง (โชคดี! หรือ race condition ไม่เกิด)")
    
    # สรุป
    print(f"\n{'=' * 70}")
    print("สรุป Race Condition")
    print("=" * 70)
    print("\n🔍 ทำไมเกิดปัญหา?")
    print("  1. หลาย threads อ่านค่าเดียวกันพร้อมกัน")
    print("  2. แต่ละ thread คำนวณ +1 จากค่าที่อ่าน")
    print("  3. threads เขียนค่าใหม่ทับกัน")
    print("  4. ทำให้บางครั้งสูญหายไป")
    
    print("\n💡 ตัวอย่าง:")
    print("  Thread A อ่าน counter = 10")
    print("  Thread B อ่าน counter = 10 (ยังไม่ได้อัพเดต)")
    print("  Thread A เขียน counter = 11")
    print("  Thread B เขียน counter = 11 (ทับ!)")
    print("  → ควรได้ 12 แต่ได้ 11")
    
    print("\n🔧 วิธีแก้:")
    print("  ใช้ Lock, Semaphore หรือ Mutex")
    print("  ดูโปรแกรม race_condition_fixed.py")
    
    print("\n" + "=" * 70)
    print("เสร็จสิ้นการทำงาน")
    print("=" * 70)


if __name__ == "__main__":
    main()
