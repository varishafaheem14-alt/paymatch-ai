"""
Utility and helper functions for PayMatch AI.
Provides currency formatting, CSV validation, column aliasing, and report generation.
"""

from typing import Tuple, Optional, Dict, Any
import pandas as pd
import numpy as np


def format_inr(amount: float) -> str:
    """Format numeric values as Indian Rupee (INR) currency strings."""
    if amount is None or np.isnan(amount):
        return "₹0.00"
    
    is_negative = amount < 0
    amount = abs(amount)
    
    # Split decimal and integer parts
    s = f"{amount:.2f}"
    parts = s.split(".")
    int_part = parts[0]
    dec_part = parts[1]
    
    # Format Indian comma system (last 3, then groups of 2)
    if len(int_part) <= 3:
        formatted_int = int_part
    else:
        last_three = int_part[-3:]
        remaining = int_part[:-3]
        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.insert(0, remaining)
        groups.append(last_three)
        formatted_int = ",".join(groups)
    
    sign = "-" if is_negative else ""
    return f"{sign}₹{formatted_int}.{dec_part}"


# Column mapping dictionary for flexible CSV header matching
COLUMN_ALIASES = {
    "transaction_id": ["transaction_id", "txn_id", "transactionid", "txnid", "txn_no", "reference_no", "payment_id"],
    "invoice_id": ["invoice_id", "inv_id", "invoiceid", "invid", "invoice_no", "bill_no", "order_id"],
    "customer_name": ["customer_name", "customer", "client_name", "client", "buyer", "merchant_name", "user_name"],
    "invoice_amount": ["invoice_amount", "inv_amount", "amount", "billed_amount", "total_amount", "invoice_amt"],
    "paid_amount": ["paid_amount", "amount_paid", "received_amount", "settled_amount", "collected_amount", "payment_amount"],
    "payment_date": ["payment_date", "txn_date", "date", "settlement_date", "paid_at", "created_at"],
    "payment_method": ["payment_method", "method", "mode", "payment_mode", "gateway", "channel"],
    "status": ["status", "txn_status", "payment_status", "state", "transaction_status"]
}


def sanitize_and_validate_csv(df: pd.DataFrame) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Validates and normalizes uploaded transaction CSV data.
    Maps headers using aliases, cleans amounts, handles missing values, and checks minimum requirements.
    """
    if df is None or df.empty:
        return None, "The uploaded file is empty. Please upload a valid CSV file with transaction data."
    
    # Strip whitespace from column headers
    df.columns = [str(c).strip().lower() for c in df.columns]
    
    # Map columns based on aliases
    rename_dict = {}
    for standard_col, aliases in COLUMN_ALIASES.items():
        found = False
        for alias in aliases:
            if alias in df.columns:
                rename_dict[alias] = standard_col
                found = True
                break
    
    df = df.rename(columns=rename_dict)
    
    # Check essential columns
    required_cols = ["invoice_id", "invoice_amount"]
    missing_required = [col for col in required_cols if col not in df.columns]
    if missing_required:
        return None, f"Missing required columns: {', '.join(missing_required)}. Expected at least 'invoice_id' and 'invoice_amount'."
    
    # Fill optional columns if missing
    if "transaction_id" not in df.columns:
        df["transaction_id"] = [f"TXN-AUTO-{i+1000}" for i in range(len(df))]
    if "customer_name" not in df.columns:
        df["customer_name"] = "Unknown Customer"
    if "paid_amount" not in df.columns:
        df["paid_amount"] = 0.0
    if "payment_date" not in df.columns:
        df["payment_date"] = pd.Timestamp.now().strftime("%Y-%m-%d")
    if "payment_method" not in df.columns:
        df["payment_method"] = "Unknown"
    if "status" not in df.columns:
        df["status"] = "SUCCESS"

    # Clean numeric columns
    for num_col in ["invoice_amount", "paid_amount"]:
        if df[num_col].dtype == object:
            # Remove currency symbols, commas, quotes, and whitespace
            df[num_col] = (
                df[num_col].astype(str)
                .str.replace("₹", "", regex=False)
                .str.replace("$", "", regex=False)
                .str.replace(",", "", regex=False)
                .str.replace(" ", "", regex=False)
                .str.strip()
            )
        df[num_col] = pd.to_numeric(df[num_col], errors="coerce").fillna(0.0)

    # Clean text columns
    text_cols = ["transaction_id", "invoice_id", "customer_name", "payment_method", "status"]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan": "N/A", "None": "N/A", "": "N/A"})

    # Clean payment dates
    df["payment_date"] = df["payment_date"].astype(str).str.strip()

    return df, None


def generate_executive_summary(metrics: Dict[str, Any], flagged_df: pd.DataFrame) -> str:
    """Generate a clean executive summary report in Markdown format."""
    now_str = pd.Timestamp.now().strftime("%d %B %Y, %I:%M %p")
    
    summary = f"""# 📑 PayMatch AI — Executive Finance Reconciliation Report
**Generated On:** {now_str}
**Reconciliation Status:** Audit Completed

---

## 1. Key Performance Indicators (KPIs)
* **Total Transactions Processed:** {metrics.get('total_transactions', 0):,}
* **Total Invoiced Value:** {format_inr(metrics.get('total_invoiced_amount', 0.0))}
* **Total Received Amount:** {format_inr(metrics.get('total_paid_amount', 0.0))}
* **Overall Reconciliation Rate:** {metrics.get('reconciliation_rate', 0.0):.1f}%
* **Total Financial Risk / Discrepancy:** {format_inr(metrics.get('total_mismatch_amount', 0.0))}

---

## 2. Reconciliation Status Breakdown
* **✅ Perfectly Matched:** {metrics.get('matched_count', 0):,} transactions ({format_inr(metrics.get('matched_amount', 0.0))})
* **⚠️ Amount Mismatches:** {metrics.get('mismatch_count', 0):,} transactions ({format_inr(metrics.get('mismatch_diff', 0.0))} variance)
* **❌ Missing Payments:** {metrics.get('missing_count', 0):,} transactions ({format_inr(metrics.get('missing_amount', 0.0))} uncollected)
* **🔄 Duplicate Transactions:** {metrics.get('duplicate_count', 0):,} transactions
* **⏳ Pending Settlements:** {metrics.get('pending_count', 0):,} transactions

---

## 3. High-Priority Action Items
"""
    if flagged_df is not None and not flagged_df.empty:
        top_risk = flagged_df.head(5)
        for idx, row in top_risk.iterrows():
            summary += f"""### [{row.get('reconciliation_status', 'FLAGGED')}] {row.get('invoice_id', 'N/A')} - {row.get('customer_name', 'Customer')}
* **Transaction ID:** `{row.get('transaction_id', 'N/A')}`
* **Invoiced:** {format_inr(row.get('invoice_amount', 0.0))} | **Paid:** {format_inr(row.get('paid_amount', 0.0))} | **Variance:** {format_inr(row.get('difference', 0.0))}
* **AI Root Cause:** {row.get('ai_reason', 'Discrepancy detected')}
* **Recommended Next Action:** {row.get('recommended_action', 'Verify transaction records')}

"""
    else:
        summary += "\n*🎉 All transactions are 100% reconciled! No immediate action items required.*\n"

    summary += """
---
*Report generated automatically by PayMatch AI Finance Controller (Track 4 - Razorpay Hackathon)*
"""
    return summary
