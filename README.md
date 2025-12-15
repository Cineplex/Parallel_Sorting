# Proof of Concept: Parallel & Distributed Algorithms

## Parallel Sorting (Bucketing)
**ไฟล์**: `Parallel_Sorting.py`

### หลักการทำงาน
ใช้เทคนิค **Scatter-Gather** ร่วมกับ **Multithreading**:
1. **Scatter (กระจายงาน)**: แบ่งข้อมูลดิบลง "ถัง" (Buckets) ตามช่วงค่า (เช่น 0-20, 21-40)
2. **Parallel Sort (ประมวลผลขนาน)**: ใช้ `ThreadPoolExecutor` เพื่อให้ Worker หลายตัวช่วยกันเรียงข้อมูลในถังของตัวเองพร้อมๆ กัน
3. **Gather (รวมผล)**: นำข้อมูลที่เรียงแล้วจากทุกถังมาต่อกันเป็นผลลัพธ์สุดท้าย

### วิธีรัน
```bash
python Parallel_Sorting.py
```

## ทฤษฎีที่เกี่ยวข้อง (Theoretical Concepts)

### Parallel Computing: Scatter-Gather Pattern
รูปแบบการประมวลผลแบบขนานที่ใช้ใน Bucket Sort คือ **Scatter-Gather**:
- **Scatter (กระจาย)**: ข้อมูลขนาดใหญ่ถูกแบ่ง (Partition) ออกเป็นส่วนย่อยๆ ส่งไปให้หน่วยประมวลผลย่อย (Workers)
- **Compute (ประมวลผล)**: แต่ละหน่วยทำงานของตัวเองอย่างอิสระ (Parallel Execution)
- **Gather (รวบรวม)**: ผลลัพธ์ย่อยถูกนำมารวมกันเพื่อสร้างผลลัพธ์สุดท้าย
- **Multithreading**: ใน Python การใช้ `ThreadPoolExecutor` เหมาะกับงาน I/O Bound หรือการจำลองสถานการณ์ แต่ถ้าเป็น CPU Bound จริงๆ อาจติด Global Interpreter Lock (GIL) ซึ่งในที่นี้ใช้เพื่อสาธิต Concept เท่านั้น
