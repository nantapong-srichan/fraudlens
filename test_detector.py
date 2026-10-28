import unittest

import pandas as pd

from detector import detect_anomalies


class DetectorTests(unittest.TestCase):
    def test_flags_high_amount_and_country_mismatch(self):
        data = pd.DataFrame(
            [
                ["TX1", "U1", "2026-10-28 09:00", 60000, "TH", "TH", "ร้านค้า"],
                ["TX2", "U2", "2026-10-28 09:00", 100, "SG", "TH", "ออนไลน์"],
            ],
            columns=["transaction_id", "user_id", "timestamp", "amount", "country", "home_country", "merchant"],
        )
        result = detect_anomalies(data).set_index("transaction_id")

        self.assertIn("ยอดเงินสูง", result.loc["TX1", "reasons"])
        self.assertIn("ประเทศไม่ตรงกับบัญชี", result.loc["TX2", "reasons"])

    def test_flags_velocity(self):
        rows = [
            [f"TX{i}", "U1", f"2026-10-28 09:0{i}", 100, "TH", "TH", "ร้านค้า"]
            for i in range(1, 4)
        ]
        data = pd.DataFrame(
            rows,
            columns=["transaction_id", "user_id", "timestamp", "amount", "country", "home_country", "merchant"],
        )
        result = detect_anomalies(data)

        flagged = result.loc[result["transaction_id"] == "TX3", "reasons"].iloc[0]
        self.assertIn("ธุรกรรมถี่ผิดปกติ", flagged)


if __name__ == "__main__":
    unittest.main()
