import pandas as pd
import streamlit as st

from detector import detect_anomalies


st.set_page_config(page_title="FraudLens", layout="wide")
st.title("FraudLens")
st.caption("ระบบตรวจจับธุรกรรมผิดปกติแบบอธิบายได้ สำหรับการเรียนรู้ด้าน FinTech")


@st.cache_data
def sample_data() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["TX001", "U001", "2026-10-28 09:00", 850, "TH", "TH", "ร้านกาแฟ"],
            ["TX002", "U001", "2026-10-28 09:04", 1200, "TH", "TH", "ร้านอาหาร"],
            ["TX003", "U001", "2026-10-28 09:08", 990, "TH", "TH", "ร้านค้าออนไลน์"],
            ["TX004", "U002", "2026-10-28 10:30", 78000, "TH", "TH", "โอนเงิน"],
            ["TX005", "U003", "2026-10-28 11:15", 2400, "SG", "TH", "ออนไลน์"],
            ["TX006", "U004", "2026-10-28 12:00", 450, "TH", "TH", "ร้านค้า"],
        ],
        columns=["transaction_id", "user_id", "timestamp", "amount", "country", "home_country", "merchant"],
    )


with st.sidebar:
    st.header("ข้อมูลธุรกรรม")
    uploaded = st.file_uploader("อัปโหลด CSV", type="csv")
    st.info("CSV ต้องมีคอลัมน์: transaction_id, user_id, timestamp, amount, country, home_country, merchant")

data = pd.read_csv(uploaded) if uploaded else sample_data()
result = detect_anomalies(data)

with st.sidebar:
    st.header("ตัวกรอง")
    selected_levels = st.multiselect(
        "ระดับความเสี่ยง",
        options=["ปกติ", "เฝ้าระวัง", "เสี่ยงสูง"],
        default=["ปกติ", "เฝ้าระวัง", "เสี่ยงสูง"],
    )
    available_dates = sorted(pd.to_datetime(result["timestamp"]).dt.date.unique())
    selected_dates = st.multiselect(
        "วันที่",
        options=available_dates,
        default=available_dates,
        format_func=lambda value: value.strftime("%Y-%m-%d"),
    )

result["date"] = pd.to_datetime(result["timestamp"]).dt.date
filtered = result[
    result["risk_level"].isin(selected_levels) & result["date"].isin(selected_dates)
].copy()

high_risk = int((filtered["risk_level"] == "เสี่ยงสูง").sum())
watch = int((filtered["risk_level"] == "เฝ้าระวัง").sum())
c1, c2, c3 = st.columns(3)
c1.metric("ธุรกรรมทั้งหมด", len(filtered))
c2.metric("เสี่ยงสูง", high_risk)
c3.metric("เฝ้าระวัง", watch)

st.subheader("ภาพรวมความเสี่ยง")
chart = filtered["risk_level"].value_counts().reindex(["ปกติ", "เฝ้าระวัง", "เสี่ยงสูง"], fill_value=0)
st.bar_chart(chart)

st.subheader("ยอดธุรกรรมรายวัน")
daily_amount = filtered.groupby("date", as_index=True)["amount"].sum()
st.line_chart(daily_amount)

st.subheader("รายการที่ตรวจพบ")
display = filtered.drop(columns=["date"]).copy()
display["amount"] = display["amount"].map(lambda value: f"฿{value:,.0f}")
st.dataframe(display, use_container_width=True, hide_index=True)

if not filtered.empty:
    st.subheader("รายละเอียดธุรกรรม")
    selected_transaction = st.selectbox("เลือก transaction ID", filtered["transaction_id"].tolist())
    detail = filtered[filtered["transaction_id"] == selected_transaction].iloc[0]
    d1, d2, d3 = st.columns(3)
    d1.metric("Risk score", int(detail["risk_score"]))
    d2.metric("ระดับความเสี่ยง", str(detail["risk_level"]))
    d3.metric("ยอดเงิน", f"฿{detail['amount']:,.0f}")
    st.write(f"เหตุผล: {detail['reasons'] or 'ไม่พบสัญญาณผิดปกติ'}")

st.download_button(
    "ดาวน์โหลดผลตรวจเป็น CSV",
    data=filtered.drop(columns=["date"]).to_csv(index=False).encode("utf-8-sig"),
    file_name="fraudlens_results.csv",
    mime="text/csv",
)

