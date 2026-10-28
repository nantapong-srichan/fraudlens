"""Rule-based anomaly detection for demo transactions."""

import pandas as pd


def detect_anomalies(transactions: pd.DataFrame) -> pd.DataFrame:
    """Return transactions with transparent, explainable risk flags."""
    df = transactions.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["risk_score"] = 0
    df["reasons"] = ""

    def add_flag(mask: pd.Series, points: int, reason: str) -> None:
        df.loc[mask, "risk_score"] += points
        df.loc[mask, "reasons"] = df.loc[mask, "reasons"].apply(
            lambda current: f"{current}; {reason}".strip("; ")
        )

    add_flag(df["amount"] >= 50000, 40, "ยอดเงินสูง")
    add_flag(df["country"] != df["home_country"], 25, "ประเทศไม่ตรงกับบัญชี")

    # More than three transactions by the same user within ten minutes.
    velocity = df.apply(
        lambda row: (
            (df["user_id"] == row["user_id"])
            & df["timestamp"].between(
                row["timestamp"] - pd.Timedelta(minutes=10), row["timestamp"]
            )
        ).sum(),
        axis=1,
    )
    add_flag(velocity >= 3, 35, "ธุรกรรมถี่ผิดปกติ")

    df["risk_level"] = pd.cut(
        df["risk_score"],
        bins=[-1, 29, 59, float("inf")],
        labels=["ปกติ", "เฝ้าระวัง", "เสี่ยงสูง"],
    )
    return df.sort_values("risk_score", ascending=False)

