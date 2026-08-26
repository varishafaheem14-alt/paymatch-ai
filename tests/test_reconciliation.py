"""
Unit Tests for PayMatch AI Reconciliation Engine and Utilities.
"""

import unittest
import pandas as pd
from src.utils import format_inr, sanitize_and_validate_csv
from src.reconciliation import (
    reconcile_transactions,
    reconcile_two_files,
    STATUS_MATCHED,
    STATUS_MISMATCH,
    STATUS_MISSING,
    STATUS_DUPLICATE,
    STATUS_PENDING,
)
from src.ai_assistant import analyze_portfolio_health, answer_finance_query


class TestPayMatchReconciliation(unittest.TestCase):
    def setUp(self):
        self.sample_data = pd.DataFrame([
            {
                "transaction_id": "TXN-101",
                "invoice_id": "INV-001",
                "customer_name": "Acme Corp",
                "invoice_amount": 5000.0,
                "paid_amount": 5000.0,
                "payment_date": "2026-08-01",
                "payment_method": "Razorpay UPI",
                "status": "SUCCESS",
            },
            {
                "transaction_id": "TXN-102",
                "invoice_id": "INV-002",
                "customer_name": "Beta Tech",
                "invoice_amount": 10000.0,
                "paid_amount": 9800.0, # 2% MDR fee difference
                "payment_date": "2026-08-02",
                "payment_method": "Razorpay Cards",
                "status": "SUCCESS",
            },
            {
                "transaction_id": "TXN-103",
                "invoice_id": "INV-003",
                "customer_name": "Gamma Ltd",
                "invoice_amount": 8000.0,
                "paid_amount": 0.0, # Missing payment
                "payment_date": "2026-08-03",
                "payment_method": "None",
                "status": "FAILED",
            },
            {
                "transaction_id": "TXN-104",
                "invoice_id": "INV-004",
                "customer_name": "Delta Inc",
                "invoice_amount": 15000.0,
                "paid_amount": 15000.0,
                "payment_date": "2026-08-04",
                "payment_method": "Netbanking",
                "status": "SUCCESS",
            },
            {
                "transaction_id": "TXN-104", # Duplicate of TXN-104
                "invoice_id": "INV-004",
                "customer_name": "Delta Inc",
                "invoice_amount": 15000.0,
                "paid_amount": 15000.0,
                "payment_date": "2026-08-04",
                "payment_method": "Netbanking",
                "status": "SUCCESS",
            },
            {
                "transaction_id": "TXN-105",
                "invoice_id": "INV-005",
                "customer_name": "Epsilon Retail",
                "invoice_amount": 6000.0,
                "paid_amount": 6000.0,
                "payment_date": "2026-08-05",
                "payment_method": "Bank Transfer",
                "status": "PENDING",
            }
        ])

    def test_reconciliation_statuses(self):
        rec_df, metrics = reconcile_transactions(self.sample_data)
        
        self.assertEqual(len(rec_df), 6)
        
        # Check TXN-101 is MATCHED
        row_101 = rec_df[rec_df["transaction_id"] == "TXN-101"].iloc[0]
        self.assertEqual(row_101["reconciliation_status"], STATUS_MATCHED)
        self.assertEqual(row_101["difference"], 0.0)
        
        # Check TXN-102 is MISMATCH with 2% MDR explanation
        row_102 = rec_df[rec_df["transaction_id"] == "TXN-102"].iloc[0]
        self.assertEqual(row_102["reconciliation_status"], STATUS_MISMATCH)
        self.assertEqual(row_102["difference"], 200.0)
        self.assertIn("Razorpay", row_102["ai_reason"])
        
        # Check TXN-103 is MISSING PAYMENT
        row_103 = rec_df[rec_df["transaction_id"] == "TXN-103"].iloc[0]
        self.assertEqual(row_103["reconciliation_status"], STATUS_MISSING)
        
        # Check TXN-104 is DUPLICATE
        row_104 = rec_df[rec_df["transaction_id"] == "TXN-104"]
        for _, r in row_104.iterrows():
            self.assertEqual(r["reconciliation_status"], STATUS_DUPLICATE)
            
        # Check TXN-105 is PENDING
        row_105 = rec_df[rec_df["transaction_id"] == "TXN-105"].iloc[0]
        self.assertEqual(row_105["reconciliation_status"], STATUS_PENDING)

    def test_metrics_calculation(self):
        rec_df, metrics = reconcile_transactions(self.sample_data)
        self.assertEqual(metrics["total_transactions"], 6)
        self.assertEqual(metrics["matched_count"], 1)
        self.assertEqual(metrics["mismatch_count"], 1)
        self.assertEqual(metrics["missing_count"], 1)
        self.assertEqual(metrics["duplicate_count"], 2)
        self.assertEqual(metrics["pending_count"], 1)
        self.assertGreater(metrics["total_mismatch_amount"], 0)

    def test_currency_formatting(self):
        self.assertEqual(format_inr(5000), "₹5,000.00")
        self.assertEqual(format_inr(125000), "₹1,25,000.00")
        self.assertEqual(format_inr(10000000), "₹1,00,00,000.00")
        self.assertEqual(format_inr(0), "₹0.00")

    def test_csv_validation(self):
        clean_df, err = sanitize_and_validate_csv(self.sample_data)
        self.assertIsNone(err)
        self.assertIsNotNone(clean_df)

        # Empty DF check
        empty_df, err_empty = sanitize_and_validate_csv(pd.DataFrame())
        self.assertIsNotNone(err_empty)

    def test_ai_fallback_assistant(self):
        rec_df, metrics = reconcile_transactions(self.sample_data)
        ans_risk = answer_finance_query("What is our biggest risk?", rec_df, metrics)
        self.assertTrue("exposure" in ans_risk.lower() or "risk" in ans_risk.lower())
        
        ans_missing = answer_finance_query("Show missing payments", rec_df, metrics)
        self.assertIn("missing", ans_missing.lower())

    def test_dual_file_reconciliation(self):
        inv_df = pd.DataFrame([
            {"invoice_id": "INV-100", "customer_name": "Test Co", "invoice_amount": 5000.0}
        ])
        pay_df = pd.DataFrame([
            {"payment_id": "PAY-100", "invoice_id": "INV-100", "paid_amount": 5000.0, "status": "SUCCESS"}
        ])
        rec_df, metrics = reconcile_two_files(inv_df, pay_df)
        self.assertEqual(len(rec_df), 1)
        self.assertEqual(rec_df.iloc[0]["reconciliation_status"], STATUS_MATCHED)
        self.assertEqual(metrics["matched_count"], 1)


if __name__ == "__main__":
    unittest.main()
