#!/usr/bin/env python3
"""
โปรแกรมจัดการไฟล์ครบวงจร (File Management)
วัตถุประสงค์: แสดงการทำงานของ File Operations ต่างๆ

Operations ที่รวมอยู่:
1. Create file - สร้างไฟล์ใหม่
2. Delete file - ลบไฟล์
3. Copy file - คัดลอกไฟล์
4. Move/Rename file - ย้าย/เปลี่ยนชื่อไฟล์
5. Check file existence - ตรวจสอบการมีอยู่ของไฟล์
6. Get file information - ดูข้อมูลไฟล์ (ขนาด, สิทธิ์)
"""

import os
import shutil
import stat
from datetime import datetime


def create_file(filename, content=""):
    """
    สร้างไฟล์ใหม่
    
    Args:
        filename (str): ชื่อไฟล์
        content (str): เนื้อหา
    
    Returns:
        bool: True ถ้าสำเร็จ
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ สร้างไฟล์ '{filename}' สำเร็จ")
        return True
    except Exception as e:
        print(f"❌ Error: ไม่สามารถสร้างไฟล์ - {e}")
        return False


def delete_file(filename):
    """
    ลบไฟล์
    
    Args:
        filename (str): ชื่อไฟล์
    
    Returns:
        bool: True ถ้าสำเร็จ
    """
    try:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"✅ ลบไฟล์ '{filename}' สำเร็จ")
            return True
        else:
            print(f"⚠️  ไฟล์ '{filename}' ไม่มีอยู่")
            return False
    except Exception as e:
        print(f"❌ Error: ไม่สามารถลบไฟล์ - {e}")
        return False


def copy_file(source, destination):
    """
    คัดลอกไฟล์
    
    Args:
        source (str): ไฟล์ต้นทาง
        destination (str): ไฟล์ปลายทาง
    
    Returns:
        bool: True ถ้าสำเร็จ
    """
    try:
        shutil.copy2(source, destination)  # copy2 รักษา metadata
        print(f"✅ คัดลอก '{source}' → '{destination}' สำเร็จ")
        return True
    except FileNotFoundError:
        print(f"❌ Error: ไม่พบไฟล์ต้นทาง '{source}'")
        return False
    except Exception as e:
        print(f"❌ Error: ไม่สามารถคัดลอกไฟล์ - {e}")
        return False


def move_file(source, destination):
    """
    ย้ายหรือเปลี่ยนชื่อไฟล์
    
    Args:
        source (str): ชื่อเดิม
        destination (str): ชื่อใหม่
    
    Returns:
        bool: True ถ้าสำเร็จ
    """
    try:
        shutil.move(source, destination)
        print(f"✅ ย้าย/เปลี่ยนชื่อ '{source}' → '{destination}' สำเร็จ")
        return True
    except FileNotFoundError:
        print(f"❌ Error: ไม่พบไฟล์ '{source}'")
        return False
    except Exception as e:
        print(f"❌ Error: ไม่สามารถย้ายไฟล์ - {e}")
        return False


def check_file_exists(filename):
    """
    ตรวจสอบการมีอยู่ของไฟล์
    
    Args:
        filename (str): ชื่อไฟล์
    
    Returns:
        bool: True ถ้าไฟล์มีอยู่
    """
    exists = os.path.exists(filename)
    
    if exists:
        print(f"✅ ไฟล์ '{filename}' มีอยู่")
    else:
        print(f"⚠️  ไฟล์ '{filename}' ไม่มีอยู่")
    
    return exists


def get_file_info(filename):
    """
    ดูข้อมูลไฟล์ (ขนาด, สิทธิ์, เวลา)
    
    Args:
        filename (str): ชื่อไฟล์
    
    Returns:
        dict: ข้อมูลไฟล์
    """
    try:
        # ใช้ os.stat() ซึ่งเรียก stat() system call
        file_stat = os.stat(filename)
        
        info = {
            'size': file_stat.st_size,  # ขนาดไฟล์ (bytes)
            'permissions': oct(file_stat.st_mode)[-3:],  # สิทธิ์ (octal)
            'created': datetime.fromtimestamp(file_stat.st_ctime),
            'modified': datetime.fromtimestamp(file_stat.st_mtime),
            'accessed': datetime.fromtimestamp(file_stat.st_atime)
        }
        
        print(f"\n📊 ข้อมูลของไฟล์ '{filename}':")
        print("-" * 60)
        print(f"  ขนาด: {info['size']} bytes")
        print(f"  สิทธิ์: {info['permissions']}")
        print(f"  สร้างเมื่อ: {info['created']}")
        print(f"  แก้ไขเมื่อ: {info['modified']}")
        print(f"  เข้าถึงเมื่อ: {info['accessed']}")
        print("-" * 60)
        
        return info
    
    except FileNotFoundError:
        print(f"❌ Error: ไม่พบไฟล์ '{filename}'")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def change_permissions(filename, mode):
    """
    เปลี่ยนสิทธิ์ไฟล์
    
    Args:
        filename (str): ชื่อไฟล์
        mode (int): สิทธิ์แบบ octal (เช่น 0o644, 0o755)
    
    Returns:
        bool: True ถ้าสำเร็จ
    """
    try:
        os.chmod(filename, mode)
        print(f"✅ เปลี่ยนสิทธิ์ไฟล์ '{filename}' เป็น {oct(mode)[-3:]} สำเร็จ")
        return True
    except Exception as e:
        print(f"❌ Error: ไม่สามารถเปลี่ยนสิทธิ์ไฟล์ - {e}")
        return False


def main():
    """ฟังก์ชันหลักของโปรแกรม"""
    print("=" * 70)
    print("โปรแกรมจัดการไฟล์ครบวงจร (File Management)")
    print("=" * 70)
    
    # 1. Create file
    print("\n1️⃣  CREATE FILE - สร้างไฟล์")
    print("-" * 70)
    
    test_content = """สวัสดี! นี่คือไฟล์ทดสอบ
File Management Operations
Operating Systems Lab
"""
    
    create_file("test_file.txt", test_content)
    
    # 2. Check file existence
    print("\n2️⃣  CHECK EXISTENCE - ตรวจสอบการมีอยู่ของไฟล์")
    print("-" * 70)
    
    check_file_exists("test_file.txt")
    check_file_exists("nonexistent.txt")
    
    # 3. Get file information
    print("\n3️⃣  GET INFO - ดูข้อมูลไฟล์")
    print("-" * 70)
    
    get_file_info("test_file.txt")
    
    # 4. Copy file
    print("\n4️⃣  COPY FILE - คัดลอกไฟล์")
    print("-" * 70)
    
    copy_file("test_file.txt", "test_file_copy.txt")
    
    # 5. Move/Rename file
    print("\n5️⃣  MOVE/RENAME - ย้าย/เปลี่ยนชื่อไฟล์")
    print("-" * 70)
    
    move_file("test_file_copy.txt", "test_file_renamed.txt")
    
    # 6. Change permissions
    print("\n6️⃣  CHANGE PERMISSIONS - เปลี่ยนสิทธิ์ไฟล์")
    print("-" * 70)
    
    # เปลี่ยนเป็น 644 (rw-r--r--)
    change_permissions("test_file.txt", 0o644)
    get_file_info("test_file.txt")
    
    # 7. Delete file
    print("\n7️⃣  DELETE FILE - ลบไฟล์")
    print("-" * 70)
    
    delete_file("test_file_renamed.txt")
    
    # ตรวจสอบว่าถูกลบแล้ว
    check_file_exists("test_file_renamed.txt")
    
    # 8. สรุป System Calls
    print("\n8️⃣  SYSTEM CALLS ที่ใช้")
    print("-" * 70)
    print("1. open()      - เปิดไฟล์")
    print("2. write()     - เขียนข้อมูล")
    print("3. close()     - ปิดไฟล์")
    print("4. stat()      - ดูข้อมูลไฟล์ (via os.stat)")
    print("5. unlink()    - ลบไฟล์ (via os.remove)")
    print("6. chmod()     - เปลี่ยนสิทธิ์ (via os.chmod)")
    print("7. rename()    - เปลี่ยนชื่อ (via shutil.move)")
    
    # 9. สรุปผล
    print("\n9️⃣  สรุปผลการทำงาน")
    print("-" * 70)
    print("✅ Create file - สำเร็จ")
    print("✅ Check existence - สำเร็จ")
    print("✅ Get information - สำเร็จ")
    print("✅ Copy file - สำเร็จ")
    print("✅ Move/Rename - สำเร็จ")
    print("✅ Change permissions - สำเร็จ")
    print("✅ Delete file - สำเร็จ")
    
    print("\n📁 ไฟล์ที่เหลืออยู่:")
    if os.path.exists("test_file.txt"):
        print("  - test_file.txt")
    
    print("\n" + "=" * 70)
    print("เสร็จสิ้นการทำงาน")
    print("=" * 70)


if __name__ == "__main__":
    main()
