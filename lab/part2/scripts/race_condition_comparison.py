#!/usr/bin/env python3
"""
โปรแกรมเปรียบเทียบ Race Condition
วัตถุประสงค์: เปรียบเทียบผลลัพธ์ระหว่างมี Race Condition และไม่มี

หมายเหตุ: โปรแกรมนี้ให้อาจารย์แจก นักศึกษาไม่ต้องเขียนเอง
"""

import threading
import time

# ตัวแปรสำหรับทดสอบ
counter_without_lock = 0
counter_with_lock = 0
lock = threading.Lock()


def increment_without_lock(num_increments):
    """เพิ่มค่า counter โดยไม่มี lock (มี race condition)"""
    global counter_without_lock
    
    for _ in range(num_increments):
        temp = counter_without_lock
        time.sleep(0.00001)  # สร้าง race condition
        counter_without_lock = temp + 1


def increment_with_lock(num_increments):
    """เพิ่มค่า counter โดยมี lock (ไม่มี race condition)"""
    global counter_with_lock
    
    for _ in range(num_increments):
        with lock:
            temp = counter_with_lock
            time.sleep(0.00001)
            counter_with_lock = temp + 1


def run_test(use_lock, num_threads, increments_per_thread):
    """
    รันการทดสอบ
    
    Args:
        use_lock (bool): ใช้ lock หรือไม่
        num_threads (int): จำนวน threads
        increments_per_thread (int): จำนวนการเพิ่มค่าต่อ thread
    
    Returns:
        tuple: (result, elapsed_time)
    """
    global counter_without_lock, counter_with_lock
    
    # รีเซ็ต counter
    if use_lock:
        counter_with_lock = 0
        target_func = increment_with_lock
        counter_ref = lambda: counter_with_lock
    else:
        counter_without_lock = 0
        target_func = increment_without_lock
        counter_ref = lambda: counter_without_lock
    
    threads = []
    start_time = time.time()
    
    # สร้างและเริ่ม threads
    for _ in range(num_threads):
        thread = threading.Thread(target=target_func, args=(increments_per_thread,))
        threads.append(thread)
        thread.start()
    
    # รอให้ threads ทำงานเสร็จ
    for thread in threads:
        thread.join()
    
    elapsed_time = time.time() - start_time
    
    return counter_ref(), elapsed_time


def main():
    """ฟังก์ชันหลักของโปรแกรม"""
    print("=" * 80)
    print("โปรแกรมเปรียบเทียบ Race Condition")
    print("=" * 80)
    
    num_threads = 10
    increments_per_thread = 100
    expected_value = num_threads * increments_per_thread
    
    print(f"\n⚙️  การตั้งค่า:")
    print(f"  จำนวน Threads: {num_threads}")
    print(f"  การเพิ่มค่าต่อ Thread: {increments_per_thread}")
    print(f"  ค่าที่คาดหวัง: {expected_value}")
    
    # ทดสอบแบบไม่มี lock (มี race condition)
    print(f"\n{'=' * 80}")
    print("1️⃣  ทดสอบแบบไม่มี Lock (มี Race Condition)")
    print("=" * 80)
    
    result_no_lock, time_no_lock = run_test(False, num_threads, increments_per_thread)
    
    print(f"\n📊 ผลลัพธ์:")
    print(f"  ค่าที่คาดหวัง: {expected_value}")
    print(f"  ค่าที่ได้จริง: {result_no_lock}")
    print(f"  สูญหาย: {expected_value - result_no_lock} ({((expected_value - result_no_lock)/expected_value*100):.1f}%)")
    print(f"  เวลาที่ใช้: {time_no_lock:.4f} วินาที")
    
    if result_no_lock != expected_value:
        print(f"\n❌ เกิด Race Condition!")
    else:
        print(f"\n⚠️  ค่าถูกต้อง แต่เป็นเพราะโชค (ลองรันอีกครั้ง)")
    
    # ทดสอบแบบมี lock (ไม่มี race condition)
    print(f"\n{'=' * 80}")
    print("2️⃣  ทดสอบแบบมี Lock (แก้ไข Race Condition)")
    print("=" * 80)
    
    result_with_lock, time_with_lock = run_test(True, num_threads, increments_per_thread)
    
    print(f"\n📊 ผลลัพธ์:")
    print(f"  ค่าที่คาดหวัง: {expected_value}")
    print(f"  ค่าที่ได้จริง: {result_with_lock}")
    print(f"  สูญหาย: {expected_value - result_with_lock}")
    print(f"  เวลาที่ใช้: {time_with_lock:.4f} วินาที")
    
    if result_with_lock == expected_value:
        print(f"\n✅ ค่าถูกต้อง! Lock ทำงานได้ดี")
    else:
        print(f"\n⚠️  ค่าไม่ถูกต้อง (ไม่ควรเกิด)")
    
    # สรุปเปรียบเทียบ
    print(f"\n{'=' * 80}")
    print("📊 สรุปเปรียบเทียบ")
    print("=" * 80)
    
    print(f"\n{'':.<30} {'ไม่มี Lock':>15} {'มี Lock':>15}")
    print("-" * 80)
    print(f"{'ค่าที่ได้':.<30} {result_no_lock:>15} {result_with_lock:>15}")
    print(f"{'ความถูกต้อง':.<30} {'❌ ไม่ถูก':>15} {'✅ ถูก':>15}")
    print(f"{'เวลา (วินาที)':.<30} {time_no_lock:>15.4f} {time_with_lock:>15.4f}")
    print(f"{'Race Condition':.<30} {'❌ มี':>15} {'✅ ไม่มี':>15}")
    
    print(f"\n💡 สังเกต:")
    print(f"  - แบบไม่มี lock: เร็วกว่าเล็กน้อย แต่ผลลัพธ์ผิด")
    print(f"  - แบบมี lock: ช้ากว่าเล็กน้อย แต่ผลลัพธ์ถูกต้อง")
    print(f"  - ความถูกต้องสำคัญกว่าความเร็ว!")
    
    print("\n" + "=" * 80)
    print("เสร็จสิ้นการทำงาน")
    print("=" * 80)


if __name__ == "__main__":
    main()
