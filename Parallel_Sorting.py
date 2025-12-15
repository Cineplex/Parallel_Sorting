import concurrent.futures
import random
import time
import os
import threading

# --- Configuration ---
DATA_SIZE = 50
MIN_VAL = 0
MAX_VAL = 100  
NUM_BUCKETS = 5

class ParallelBucketSort:
    def __init__(self, num_buckets=NUM_BUCKETS):
        self.num_buckets = num_buckets
        self.range_per_bucket = (MAX_VAL - MIN_VAL) / num_buckets
        
    def _get_bucket_index(self, value):
        """คำนวณว่าค่านี้ควรอยู่ถังไหน (Scatter Logic)"""
        index = int((value - MIN_VAL) / self.range_per_bucket)
        if index >= self.num_buckets:
            index = self.num_buckets - 1
        return index

    def _sort_bucket(self, bucket_id, data):
        """ฟังก์ชันสำหรับ Worker Thread: เรียงข้อมูลในถังเดียว"""
        print(f"   [Worker-{bucket_id}] กำลังเรียงข้อมูล {len(data)} ตัว... (Thread ID: {threading.get_ident()})")
        # Simulate processing time
        time.sleep(random.uniform(0.2, 0.8)) 
        sorted_data = sorted(data)
        print(f"   [Worker-{bucket_id}] เรียงเสร็จแล้ว: {sorted_data}")
        return bucket_id, sorted_data

    def visualize_buckets(self, buckets, stage_name):
        """แสดงภาพข้อมูลในถังแบบ ASCII"""
        print(f"\n--- {stage_name} ---")
        for i, bucket in enumerate(buckets):
            # สร้างกราฟแท่งง่ายๆ จากจำนวนข้อมูล
            bar = "█" * len(bucket)
            # คำนวณช่วง: start ถึง end-1 (เช่น 0-19, 20-39)
            start_val = int(MIN_VAL + (i * self.range_per_bucket))
            end_val = int(MIN_VAL + ((i + 1) * self.range_per_bucket)) - 1
            range_str = f"{start_val}-{end_val}"
            print(f"Bucket {i} [{range_str:<7}]: {bar} ({len(bucket)} items) -> {bucket}")
        print("-" * 40)

    def run(self):
        print(f"=== เริ่มต้น Parallel Bucket Sort (PID: {os.getpid()}) ===")
        
        # 1. Generate Data
        raw_data = [random.randint(MIN_VAL, MAX_VAL - 1) for _ in range(DATA_SIZE)]
        print(f"ข้อมูลดิบ ({DATA_SIZE} ตัว): {raw_data}")

        # 2. Scatter (กระจายข้อมูลลงถัง)
        print("\n[Phase 1] Scattering: กระจายข้อมูลลงถัง...")
        buckets = [[] for _ in range(self.num_buckets)]
        for num in raw_data:
            idx = self._get_bucket_index(num)
            buckets[idx].append(num)
            
        self.visualize_buckets(buckets, "สถานะถังก่อนเรียง (Unsorted Buckets)")

        # 3. Parallel Sort (ส่งงานให้ Workers)
        print("\n[Phase 2] Parallel Sorting: ส่งให้ Worker Threads เรียงพร้อมกัน...")
        sorted_buckets = [None] * self.num_buckets
        
        # ใช้ ThreadPoolExecutor เพื่อจัดการ Parallelism
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_buckets) as executor:
            # Submit งานทั้งหมด
            future_to_bucket = {executor.submit(self._sort_bucket, i, buckets[i]): i for i in range(self.num_buckets)}
            
            # รอรับผลลัพธ์เมื่อเสร็จ (Asynchronous)
            for future in concurrent.futures.as_completed(future_to_bucket):
                bucket_id, result = future.result()
                sorted_buckets[bucket_id] = result
                
        self.visualize_buckets(sorted_buckets, "สถานะถังหลังเรียง (Sorted Buckets)")

        # 4. Gather (รวมผลลัพธ์)
        print("\n[Phase 3] Gathering: รวมข้อมูลกลับเป็นอาเรย์เดียว...")
        final_result = []
        for b in sorted_buckets:
            final_result.extend(b)
            
        print(f"\n=== ผลลัพธ์สุดท้าย ===")
        print(f"Sorted Data: {final_result}")
        
        # Verify
        if final_result == sorted(raw_data):
            print("Status: ✅ ถูกต้อง (Verified)")
        else:
            print("Status: ❌ ผิดพลาด (Error)")

if __name__ == "__main__":
    sorter = ParallelBucketSort()
    sorter.run()
