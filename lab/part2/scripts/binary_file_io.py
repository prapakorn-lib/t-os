#!/usr/bin/env python3
"""
โปรแกรม Binary File I/O
วัตถุประสงค์: อ่าน/เขียนไฟล์ binary
"""

def write_binary_file(filename, data):
    """เขียนไฟล์ binary"""
    try:
        with open(filename, 'wb') as f:
            f.write(data)
        print(f"✅ เขียนไฟล์ binary '{filename}' สำเร็จ")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def read_binary_file(filename):
    """อ่านไฟล์ binary"""
    try:
        with open(filename, 'rb') as f:
            data = f.read()
        print(f"✅ อ่านไฟล์ '{filename}' สำเร็จ ({len(data)} bytes)")
        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    """ฟังก์ชันหลัก"""
    print("=" * 60)
    print("โปรแกรม Binary File I/O")
    print("=" * 60)
    
    # 1. เขียนไฟล์ binary
    print("\n1️⃣  เขียนไฟล์ Binary")
    print("-" * 60)
    
    binary_data = b"Hello Binary World!\x00\x01\x02\x03"
    write_binary_file("test.bin", binary_data)
    
    # 2. อ่านไฟล์ binary
    print("\n2️⃣  อ่านไฟล์ Binary")
    print("-" * 60)
    
    data = read_binary_file("test.bin")
    if data:
        print(f"ข้อมูล: {data}")
        print(f"Hex: {data.hex()}")
    
    # 3. เขียนไฟล์ binary จากข้อความ
    print("\n3️⃣  แปลงข้อความเป็น Binary")
    print("-" * 60)
    
    text = "สวัสดี Operating Systems!"
    binary = text.encode('utf-8')
    write_binary_file("text_binary.bin", binary)
    
    # อ่านกลับมาแปลงเป็นข้อความ
    data = read_binary_file("text_binary.bin")
    if data:
        decoded = data.decode('utf-8')
        print(f"ข้อความ: {decoded}")
    
    print("\n" + "=" * 60)
    print("เสร็จสิ้น")
    print("=" * 60)


if __name__ == "__main__":
    main()
