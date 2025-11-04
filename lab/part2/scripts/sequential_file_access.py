#!/usr/bin/env python3
"""
โปรแกรม Sequential File Access
วัตถุประสงค์: อ่านไฟล์แบบเรียงลำดับทีละบรรทัด

เหมาะสำหรับ:
- ไฟล์ขนาดใหญ่
- การประมวลผลข้อมูลทีละส่วน
- ประหยัด memory
"""

def sequential_read_lines(filename):
    """
    อ่านไฟล์ทีละบรรทัดแบบเรียงลำดับ
    
    Args:
        filename (str): ชื่อไฟล์
    """
    print(f"📖 อ่านไฟล์แบบ Sequential: {filename}")
    print("-" * 60)
    
    try:
        line_count = 0
        word_count = 0
        char_count = 0
        
        with open(filename, 'r', encoding='utf-8') as f:
            # อ่านทีละบรรทัด (sequential)
            for line in f:
                line_count += 1
                word_count += len(line.split())
                char_count += len(line)
                
                print(f"บรรทัด {line_count}: {line.rstrip()}")
        
        print("-" * 60)
        print(f"\n📊 สถิติ:")
        print(f"  จำนวนบรรทัด: {line_count}")
        print(f"  จำนวนคำ: {word_count}")
        print(f"  จำนวนตัวอักษร: {char_count}")
        
    except FileNotFoundError:
        print(f"❌ ไม่พบไฟล์ '{filename}'")
    except Exception as e:
        print(f"❌ Error: {e}")


def sequential_process_chunks(filename, chunk_size=1024):
    """
    อ่านไฟล์ทีละ chunk (เหมาะสำหรับไฟล์ขนาดใหญ่)
    
    Args:
        filename (str): ชื่อไฟล์
        chunk_size (int): ขนาด chunk (bytes)
    """
    print(f"\n📖 อ่านไฟล์แบบ Chunks (chunk_size={chunk_size} bytes)")
    print("-" * 60)
    
    try:
        chunk_count = 0
        total_size = 0
        
        with open(filename, 'r', encoding='utf-8') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                chunk_count += 1
                total_size += len(chunk)
                print(f"Chunk {chunk_count}: {len(chunk)} bytes")
        
        print("-" * 60)
        print(f"อ่าน {chunk_count} chunks, รวม {total_size} bytes")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """ฟังก์ชันหลักของโปรแกรม"""
    print("=" * 70)
    print("โปรแกรม Sequential File Access")
    print("=" * 70)
    
    # สร้างไฟล์ทดสอบ
    test_file = "sequential_test.txt"
    print(f"\n1️⃣  สร้างไฟล์ทดสอบ: {test_file}")
    print("-" * 70)
    
    with open(test_file, 'w', encoding='utf-8') as f:
        for i in range(1, 11):
            f.write(f"บรรทัดที่ {i}: ข้อมูลทดสอบสำหรับ Sequential Access\n")
    
    print(f"✅ สร้างไฟล์ทดสอบสำเร็จ (10 บรรทัด)")
    
    # อ่านทีละบรรทัด
    print(f"\n2️⃣  อ่านไฟล์ทีละบรรทัด (Sequential)")
    print("-" * 70)
    sequential_read_lines(test_file)
    
    # อ่านแบบ chunks
    print(f"\n3️⃣  อ่านไฟล์แบบ Chunks")
    print("-" * 70)
    sequential_process_chunks(test_file, chunk_size=50)
    
    # ข้อดีของ Sequential Access
    print(f"\n4️⃣  ข้อดีของ Sequential File Access")
    print("-" * 70)
    print("✅ ประหยัด Memory - ไม่ต้องโหลดทั้งไฟล์")
    print("✅ เหมาะสำหรับไฟล์ขนาดใหญ่")
    print("✅ ประมวลผลได้ทันทีโดยไม่ต้องรอ")
    print("✅ Simple และ Efficient")
    
    print("\n" + "=" * 70)
    print("เสร็จสิ้นการทำงาน")
    print("=" * 70)


if __name__ == "__main__":
    main()
