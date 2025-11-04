#!/usr/bin/env python3
"""
โปรแกรม Buffered I/O
วัตถุประสงค์: เปรียบเทียบความเร็วระหว่าง Buffered และ Unbuffered I/O

Buffer ช่วยเพิ่มประสิทธิภาพโดยลดจำนวนครั้งในการเข้าถึง disk
"""

import time

def write_without_buffer(filename, num_writes=1000):
    """
    เขียนไฟล์แบบไม่ใช้ buffer (buffer size = 0)
    
    Args:
        filename (str): ชื่อไฟล์
        num_writes (int): จำนวนครั้งที่เขียน
    
    Returns:
        float: เวลาที่ใช้ (วินาที)
    """
    start_time = time.time()
    
    # buffering=0 = unbuffered (ต้องใช้ binary mode)
    with open(filename, 'wb', buffering=0) as f:
        for i in range(num_writes):
            f.write(f"Line {i}\n".encode())
    
    elapsed_time = time.time() - start_time
    return elapsed_time


def write_with_buffer(filename, num_writes=1000, buffer_size=8192):
    """
    เขียนไฟล์แบบใช้ buffer
    
    Args:
        filename (str): ชื่อไฟล์
        num_writes (int): จำนวนครั้งที่เขียน
        buffer_size (int): ขนาด buffer (bytes)
    
    Returns:
        float: เวลาที่ใช้ (วินาที)
    """
    start_time = time.time()
    
    with open(filename, 'w', buffering=buffer_size) as f:
        for i in range(num_writes):
            f.write(f"Line {i}\n")
    
    elapsed_time = time.time() - start_time
    return elapsed_time


def read_with_different_buffers(filename):
    """
    อ่านไฟล์ด้วยขนาด buffer ต่างๆ
    
    Args:
        filename (str): ชื่อไฟล์
    """
    print("\n📖 อ่านไฟล์ด้วยขนาด buffer ต่างๆ")
    print("-" * 60)
    
    buffer_sizes = [512, 1024, 4096, 8192]
    
    for buffer_size in buffer_sizes:
        start_time = time.time()
        
        with open(filename, 'r', buffering=buffer_size) as f:
            data = f.read()
        
        elapsed_time = time.time() - start_time
        print(f"Buffer {buffer_size:5d} bytes: {elapsed_time:.6f} วินาที")


def main():
    """ฟังก์ชันหลักของโปรแกรม"""
    print("=" * 70)
    print("โปรแกรม Buffered I/O")
    print("=" * 70)
    
    num_writes = 1000
    
    # 1. เขียนแบบไม่ใช้ buffer
    print(f"\n1️⃣  เขียนไฟล์แบบไม่ใช้ Buffer (Unbuffered)")
    print("-" * 70)
    
    unbuffered_file = "unbuffered.txt"
    unbuffered_time = write_without_buffer(unbuffered_file, num_writes)
    print(f"✅ เขียน {num_writes} บรรทัด")
    print(f"⏱️  เวลา: {unbuffered_time:.6f} วินาที")
    
    # 2. เขียนแบบใช้ buffer (ค่า default)
    print(f"\n2️⃣  เขียนไฟล์แบบใช้ Buffer (Default)")
    print("-" * 70)
    
    buffered_file = "buffered_default.txt"
    buffered_time = write_with_buffer(buffered_file, num_writes)
    print(f"✅ เขียน {num_writes} บรรทัด")
    print(f"⏱️  เวลา: {buffered_time:.6f} วินาที")
    
    # 3. เขียนแบบใช้ buffer (ขนาดต่างๆ)
    print(f"\n3️⃣  เขียนไฟล์ด้วยขนาด Buffer ต่างๆ")
    print("-" * 70)
    
    buffer_sizes = [1024, 4096, 8192, 16384]
    
    for buffer_size in buffer_sizes:
        test_file = f"buffered_{buffer_size}.txt"
        elapsed = write_with_buffer(test_file, num_writes, buffer_size)
        print(f"Buffer {buffer_size:5d} bytes: {elapsed:.6f} วินาที")
    
    # 4. อ่านด้วย buffer ขนาดต่างๆ
    print(f"\n4️⃣  อ่านไฟล์")
    read_with_different_buffers(buffered_file)
    
    # 5. เปรียบเทียบผลลัพธ์
    print(f"\n5️⃣  เปรียบเทียบประสิทธิภาพ")
    print("-" * 70)
    
    speedup = unbuffered_time / buffered_time if buffered_time > 0 else 0
    
    print(f"Unbuffered: {unbuffered_time:.6f} วินาที")
    print(f"Buffered:   {buffered_time:.6f} วินาที")
    print(f"\n🚀 เร็วขึ้น: {speedup:.2f}x")
    
    # 6. สรุปข้อดี
    print(f"\n6️⃣  ข้อดีของ Buffered I/O")
    print("-" * 70)
    print("✅ ลดจำนวนครั้งในการเข้าถึง disk")
    print("✅ เพิ่มประสิทธิภาพอย่างมาก")
    print("✅ Python ใช้ buffer โดย default")
    print("✅ สามารถปรับขนาด buffer ได้")
    
    print("\n" + "=" * 70)
    print("เสร็จสิ้นการทำงาน")
    print("=" * 70)


if __name__ == "__main__":
    main()
