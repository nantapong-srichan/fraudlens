# FraudLens

Mini project ด้าน FinTech สำหรับตรวจจับธุรกรรมผิดปกติด้วยกฎที่อธิบายได้ (explainable rules)

## ความสามารถ

- ตรวจจับยอดเงินสูงผิดปกติ
- ตรวจจับประเทศที่ไม่ตรงกับประเทศหลักของผู้ใช้
- ตรวจจับธุรกรรมถี่เกินไปภายใน 10 นาที
- แสดง risk score, risk level และเหตุผลของแต่ละรายการ
- รองรับการอัปโหลด CSV และดาวน์โหลดผลลัพธ์

## วิธีรันฟรีบนเครื่อง

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

จากนั้นเปิด URL ที่ Streamlit แสดง เช่น `http://localhost:8501`

## ทดสอบ

```bash
python -m unittest -v
```

ไฟล์ `sample_transactions.csv` ใช้ทดลองอัปโหลดเข้า Dashboard ได้ทันที

## Deploy ฟรี

สามารถนำโฟลเดอร์นี้ไปสร้าง GitHub repository แล้ว deploy ผ่าน Streamlit Community Cloud ได้ โดยเลือกไฟล์ `app.py` เป็น entrypoint

> โปรเจกต์นี้ใช้ข้อมูลจำลองเท่านั้น ห้ามใช้ตัดสินใจธุรกรรมจริงโดยไม่ผ่านการตรวจสอบและ validation เพิ่มเติม

