# FraudLens

Mini project สำหรับตรวจจับธุรกรรมผิดปกติด้วยกฎที่อธิบายได้ (explainable rules)

## รายละเอียดระบบ

- ตรวจจับยอดเงินสูงผิดปกติ
- ตรวจจับประเทศที่ไม่ตรงกับประเทศหลักของผู้ใช้
- ตรวจจับธุรกรรมถี่เกินไปภายใน 10 นาที
- แสดง risk score, risk level และเหตุผลของแต่ละรายการ
- รองรับการอัปโหลด CSV และดาวน์โหลดผลลัพธ์

## วิธีรัน

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
## ทดสอบ

```bash
python -m unittest -v
```

ไฟล์ `sample_transactions.csv` ใช้ทดลองอัปโหลดเข้า Dashboard


> โปรเจกต์นี้ใช้ข้อมูลจำลองเท่านั้น ห้ามใช้ตัดสินใจธุรกรรมจริงโดยไม่ผ่านการตรวจสอบและ validation เพิ่มเติม

