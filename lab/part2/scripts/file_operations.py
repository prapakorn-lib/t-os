#!/usr/bin/env python3
"""
โปรแกรมจัดการไฟล์แบบครบวงจร
วัตถุประสงค์: แสดงการอ่าน/เขียนไฟล์พร้อม Error Handling ที่ครบถ้วน

System Calls ที่ใช้:
- open() - เปิดไฟล์
- read(), write() - อ่าน/เขียนข้อมูล
- close() - ปิดไฟล์
- os.path.exists() - ตรวจสอบไฟล์
"""

import os
import sys

def check_file_exists(filename):
    """
    ตรวจสอบว่าไฟล์มีอยู่หรือไม่
    
    Args:
        filename (str): ชื่อไฟล์
    
    Returns:
        bool: True ถ้าไฟล์มีอยู่, False ถ้าไม่มี
    """
    return os.path.exists(filename)


def safe_read_file(filename):
    """
    อ่านไฟล์อย่างปลอดภัยพร้อม error handling ครบถ้วน
    
    Args:
        filename (str): ชื่อไฟล์
    
    Returns:
        tuple: (success, content/error_message)
    """
    # ตรวจสอบว่าไฟล์มีอยู่หรือไม่
    if not check_file_exists(filename):
        return (False, f"ไม่พบไฟล์ '{filename}'")
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            return (True, content)
    
    except PermissionError:
        return (False, "ไม่มีสิทธิ์อ่านไฟล์")
    
    except UnicodeDecodeError:
        return (False, "ไฟล์ไม่ใช่ text file หรือใช้ encoding ที่ไม่รองรับ")
    
    except IOError as e:
        return (False, f"I/O Error: {e}")
    
    except Exception as e:
        return (False, f"Unexpected error: {e}")


def safe_write_file(filename, content):
    """
    เขียนไฟล์อย่างปลอดภัยพร้อม error handling ครบถ้วน
    
    Args:
        filename (str): ชื่อไฟล์
        content (str): เนื้อหา
    
    Returns:
        tuple: (success, success_message/error_message)
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
            return (True, f"เขียนไฟล์ '{filename}' สำเร็จ")
    
    except PermissionError:
        return (False, "ไม่มีสิทธิ์เขียนไฟล์")
    
    except IOError as e:
        return (False, f"I/O Error: {e}")
    
    except Exception as e:
        return (False, f"Unexpected error: {e}")


def copy_file_content(source, destination):
    """
    คัดลอกเนื้อหาจากไฟล์หนึ่งไปยังอีกไฟล์หนึ่ง
    
    Args:
        source (str): ไฟล์ต้นทาง
        destination (str): ไฟล์ปลายทาง
    
    Returns:
        tuple: (success, message)
    """
    # อ่านไฟล์ต้นทาง
    success, result = safe_read_file(source)
    
    if not success:
        return (False, f"อ่านไฟล์ต้นทางไม่สำเร็จ: {result}")
    
    content = result
    
    # เขียนไปยังไฟล์ปลายทาง
    success, result = safe_write_file(destination, content)
    
    if not success:
        return (False, f"เขียนไฟล์ปลายทางไม่สำเร็จ: {result}")
    
    return (True, f"คัดลอก '{source}' ไปยัง '{destination}' สำเร็จ")


def main():
    """ฟังก์ชันหลักของโปรแกรม"""
    print("=" * 70)
    print("โปรแกรมจัดการไฟล์แบบครบวงจร")
    print("=" * 70)
    
    # 1. สร้างไฟล์ทดสอบ
    test_file = "test_data.txt"
    test_content = """ข้อมูลทดสอบสำหรับโปรแกรม File Operations
บรรทัดที่ 2: Python Programming
บรรทัดที่ 3: Operating Systems
บรรทัดที่ 4: System Calls
บรรทัดที่ 5: Error Handling
"""
    
    print(f"\n1️⃣  สร้างไฟล์ทดสอบ: {test_file}")
    print("-" * 70)
    
    success, message = safe_write_file(test_file, test_content)
    
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ Error: {message}")
        sys.exit(1)
    
    # 2. ตรวจสอบว่าไฟล์มีอยู่
    print(f"\n2️⃣  ตรวจสอบการมีอยู่ของไฟล์")
    print("-" * 70)
    
    if check_file_exists(test_file):
        print(f"✅ ไฟล์ '{test_file}' มีอยู่")
    else:
        print(f"❌ ไฟล์ '{test_file}' ไม่มีอยู่")
    
    # 3. อ่านไฟล์
    print(f"\n3️⃣  อ่านเนื้อหาจากไฟล์")
    print("-" * 70)
    
    success, result = safe_read_file(test_file)
    
    if success:
        print(f"✅ อ่านไฟล์สำเร็จ")
        print("\n📄 เนื้อหา:")
        print("-" * 70)
        print(result)
        print("-" * 70)
    else:
        print(f"❌ Error: {result}")
    
    # 4. คัดลอกไฟล์
    backup_file = "test_data_backup.txt"
    print(f"\n4️⃣  คัดลอกไฟล์: {test_file} → {backup_file}")
    print("-" * 70)
    
    success, message = copy_file_content(test_file, backup_file)
    
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ Error: {message}")
    
    # 5. ลองอ่านไฟล์ที่ไม่มีอยู่
    print(f"\n5️⃣  ทดสอบ Error Handling: อ่านไฟล์ที่ไม่มีอยู่")
    print("-" * 70)
    
    nonexistent_file = "this_file_does_not_exist.txt"
    success, result = safe_read_file(nonexistent_file)
    
    if not success:
        print(f"✅ Error Handling ทำงานถูกต้อง")
        print(f"   Message: {result}")
    else:
        print(f"⚠️  Error Handling อาจมีปัญหา")
    
    # 6. แสดง System Calls ที่เกิดขึ้น
    print(f"\n6️⃣  System Calls ที่ใช้ในโปรแกรม")
    print("-" * 70)
    print("1. os.path.exists() - ตรวจสอบการมีอยู่ของไฟล์")
    print("2. open()           - เปิดไฟล์")
    print("3. file.read()      - อ่านข้อมูล")
    print("4. file.write()     - เขียนข้อมูล")
    print("5. file.close()     - ปิดไฟล์ (อัตโนมัติใน with statement)")
    
    # 7. สรุปผล
    print(f"\n7️⃣  สรุปการทำงาน")
    print("-" * 70)
    print(f"✅ ไฟล์ที่สร้าง: {test_file}")
    print(f"✅ ไฟล์ที่คัดลอก: {backup_file}")
    print(f"✅ การจัดการ Error: ผ่าน")
    print(f"✅ System Calls: ครบถ้วน")
    
    print("\n" + "=" * 70)
    print("เสร็จสิ้นการทำงาน")
    print("=" * 70)


if __name__ == "__main__":
    main()
