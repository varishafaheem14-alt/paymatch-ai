"""
Reconciliation Engine for PayMatch AI.
Performs deterministic multi-rule matching, duplicate detection, discrepancy calculation,
MDR fee / tax analysis, and risk scoring.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np


STATUS_MATCHED = "MATCHED"
STATUS_MISMATCH = "MISMATCH"
STATUS_MISSING = "MISSING PAYMENT"
STATUS_DUPLICATE = "DUPLICATE"
STATUS_PENDING = "PENDING"

RISK_HIGH = "High Risk"
RISK_MEDIUM = "Medium Risk"
RISK_LOW = "Low Risk"
RISK_NONE = "Resolved / None"


def reconcile_transactions(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Reconciles transaction dataset, flags anomalies, determines discrepancy cause,
    and returns an enriched DataFrame along with high-level KPI metrics.
    """
    if df is None or df.empty:
        return pd.DataFrame(), {}

    rec_df = df.copy()

    # Calculate raw numerical difference: invoice_amount - paid_amount
    rec_df["difference"] = rec_df["invoice_amount"] - rec_df["paid_amount"]
    rec_df["difference"] = rec_df["difference"].round(2)
    
    # Calculate percentage variance
    rec_df["variance_pct"] = np.where(
        rec_df["invoice_amount"] > 0,
        ((rec_df["difference"] / rec_df["invoice_amount"]) * 100).round(2),
        0.0
    )

    # Initialize columns
    reconciliation_statuses = []
    ai_reasons = []
    recommended_actions = []
    risk_levels = []

    # Step 1: Duplicate identification
    # Check duplicate transaction IDs
    duplicate_txns = rec_df[rec_df["transaction_id"] != "N/A"]["transaction_id"].duplicated(keep=False)
    # Check duplicate invoice IDs with multiple paid payments
    duplicate_invs = (rec_df["paid_amount"] > 0) & rec_df["invoice_id"].duplicated(keep=False)

    for idx, row in rec_df.iterrows():
        inv_amt = float(row["invoice_amount"])
        paid_amt = float(row["paid_amount"])
        diff = float(row["difference"])
        var_pct = float(row["variance_pct"])
        raw_status = str(row.get("status", "")).upper()
        txn_id = str(row.get("transaction_id", ""))
        is_dup = duplicate_txns.get(idx, False) or duplicate_invs.get(idx, False)

        # Rule 1: Duplicate Transaction
        if is_dup:
            reconciliation_statuses.append(STATUS_DUPLICATE)
            ai_reasons.append(
                f"Duplicate record detected for Transaction ID {txn_id}. Multiple identical charges or logs recorded."
            )
            recommended_actions.append("Flag for audit. Check bank gateway settlement logs and initiate refund if double-charged.")
            risk_levels.append(RISK_HIGH if paid_amt > 10000 else RISK_MEDIUM)

        # Rule 2: Missing Payment (Invoice issued but zero amount received or failed)
        elif paid_amt == 0.0 or raw_status in ["FAILED", "UNPAID", "CANCELLED"]:
            reconciliation_statuses.append(STATUS_MISSING)
            ai_reasons.append(
                f"No payment received for invoice {row['invoice_id']} (Uncollected amount: ₹{inv_amt:,.2f})."
            )
            recommended_actions.append("Trigger automated payment reminder email/SMS to customer with direct payment link.")
            risk_levels.append(RISK_HIGH if inv_amt > 15000 else RISK_MEDIUM)

        # Rule 3: Pending Settlement
        elif raw_status in ["PENDING", "PROCESSING", "INITIATED", "ON_HOLD", "IN_TRANSIT"]:
            reconciliation_statuses.append(STATUS_PENDING)
            ai_reasons.append(
                f"Payment of ₹{paid_amt:,.2f} is currently in gateway processing / bank settlement transit."
            )
            recommended_actions.append("Monitor gateway webhook. Allow T+2 settlement window before escalating.")
            risk_levels.append(RISK_LOW)

        # Rule 4: Perfectly Matched (Difference is zero within 1 cent tolerance)
        elif abs(diff) < 0.01:
            reconciliation_statuses.append(STATUS_MATCHED)
            ai_reasons.append("Invoice amount matches received settlement perfectly (100% Match).")
            recommended_actions.append("Reconciled successfully. Auto-archive to general ledger.")
            risk_levels.append(RISK_NONE)

        # Rule 5: Amount Mismatch (Difference > 0 or < 0)
        else:
            reconciliation_statuses.append(STATUS_MISMATCH)
            # Sub-case A: Razorpay / Gateway MDR fee (~2% deduction)
            if 1.7 <= var_pct <= 2.5:
                ai_reasons.append(
                    f"Discrepancy of ₹{diff:,.2f} ({var_pct}%). Matches standard 2% Razorpay Payment Gateway MDR transaction fee."
                )
                recommended_actions.append("Post variance to 'Payment Gateway Fees & Processing Expenses' ledger account.")
                risk_levels.append(RISK_LOW)
            
            # Sub-case B: GST / TDS withholding (~18% or ~10%)
            elif 17.0 <= var_pct <= 19.0:
                ai_reasons.append(
                    f"Discrepancy of ₹{diff:,.2f} ({var_pct}%). Matches standard 18% GST tax deduction."
                )
                recommended_actions.append("Verify customer TDS/GST certificate and reconcile against tax credit ledger.")
                risk_levels.append(RISK_MEDIUM)
                
            # Sub-case C: Partial Underpayment
            elif diff > 0:
                ai_reasons.append(
                    f"Short payment of ₹{diff:,.2f} detected against total invoice of ₹{inv_amt:,.2f}."
                )
                recommended_actions.append(f"Generate partial payment receipt and request remaining balance of ₹{diff:,.2f}.")
                risk_levels.append(RISK_HIGH if diff > 5000 else RISK_MEDIUM)
                
            # Sub-case D: Overpayment
            else:
                ai_reasons.append(
                    f"Overpayment of ₹{abs(diff):,.2f} received (Total paid: ₹{paid_amt:,.2f} vs Invoiced: ₹{inv_amt:,.2f})."
                )
                recommended_actions.append("Credit balance to customer advance wallet or issue surplus refund.")
                risk_levels.append(RISK_LOW)

    rec_df["reconciliation_status"] = reconciliation_statuses
    rec_df["ai_reason"] = ai_reasons
    rec_df["recommended_action"] = recommended_actions
    rec_df["risk_level"] = risk_levels

    # Compute KPI metrics
    total_txns = len(rec_df)
    total_invoiced = float(rec_df["invoice_amount"].sum())
    total_paid = float(rec_df["paid_amount"].sum())

    matched_mask = rec_df["reconciliation_status"] == STATUS_MATCHED
    mismatch_mask = rec_df["reconciliation_status"] == STATUS_MISMATCH
    missing_mask = rec_df["reconciliation_status"] == STATUS_MISSING
    duplicate_mask = rec_df["reconciliation_status"] == STATUS_DUPLICATE
    pending_mask = rec_df["reconciliation_status"] == STATUS_PENDING

    matched_count = int(matched_mask.sum())
    mismatch_count = int(mismatch_mask.sum())
    missing_count = int(missing_mask.sum())
    duplicate_count = int(duplicate_mask.sum())
    pending_count = int(pending_mask.sum())

    matched_amount = float(rec_df[matched_mask]["paid_amount"].sum())
    mismatch_diff = float(rec_df[mismatch_mask]["difference"].abs().sum())
    missing_amount = float(rec_df[missing_mask]["invoice_amount"].sum())
    duplicate_amount = float(rec_df[duplicate_mask]["paid_amount"].sum())

    reconciliation_rate = (matched_count / total_txns * 100) if total_txns > 0 else 0.0
    total_risk_amount = missing_amount + mismatch_diff

    metrics = {
        "total_transactions": total_txns,
        "total_invoiced_amount": total_invoiced,
        "total_paid_amount": total_paid,
        "matched_count": matched_count,
        "matched_amount": matched_amount,
        "mismatch_count": mismatch_count,
        "mismatch_diff": mismatch_diff,
        "missing_count": missing_count,
        "missing_amount": missing_amount,
        "duplicate_count": duplicate_count,
        "duplicate_amount": duplicate_amount,
        "pending_count": pending_count,
        "reconciliation_rate": reconciliation_rate,
        "total_mismatch_amount": total_risk_amount,
    }

    return rec_df, metrics


def reconcile_two_files(invoices_df: pd.DataFrame, payments_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Reconciles separate Invoices dataset and Gateway Payments dataset by joining on invoice_id.
    """
    # Normalize headers
    inv_clean = invoices_df.copy()
    inv_clean.columns = [str(c).strip().lower() for c in inv_clean.columns]
    
    pay_clean = payments_df.copy()
    pay_clean.columns = [str(c).strip().lower() for c in pay_clean.columns]

    # Map invoice columns
    if "invoice_id" not in inv_clean.columns and "inv_id" in inv_clean.columns:
        inv_clean["invoice_id"] = inv_clean["inv_id"]
    if "invoice_amount" not in inv_clean.columns and "amount" in inv_clean.columns:
        inv_clean["invoice_amount"] = inv_clean["amount"]
    if "customer_name" not in inv_clean.columns and "customer" in inv_clean.columns:
        inv_clean["customer_name"] = inv_clean["customer"]

    # Map payment columns
    if "invoice_id" not in pay_clean.columns and "inv_id" in pay_clean.columns:
        pay_clean["invoice_id"] = pay_clean["inv_id"]
    if "paid_amount" not in pay_clean.columns and "amount" in pay_clean.columns:
        pay_clean["paid_amount"] = pay_clean["amount"]
    if "payment_id" in pay_clean.columns:
        pay_clean["transaction_id"] = pay_clean["payment_id"]

    # Outer join to capture un-invoiced payments and unpaid invoices
    merged = pd.merge(inv_clean, pay_clean, on="invoice_id", how="outer", suffixes=("_inv", "_pay"))

    # Synthesize unified format
    now_date = pd.Timestamp.now().strftime("%Y-%m-%d")
    combined_df = pd.DataFrame()
    combined_df["invoice_id"] = merged["invoice_id"].fillna("INV-UNKNOWN")
    
    if "transaction_id" in merged.columns:
        combined_df["transaction_id"] = merged["transaction_id"].fillna("N/A")
    elif "payment_id" in merged.columns:
        combined_df["transaction_id"] = merged["payment_id"].fillna("N/A")
    else:
        combined_df["transaction_id"] = "N/A"

    if "customer_name" in merged.columns:
        combined_df["customer_name"] = merged["customer_name"].fillna("Valued Customer")
    else:
        combined_df["customer_name"] = "Valued Customer"

    combined_df["invoice_amount"] = pd.to_numeric(merged["invoice_amount"] if "invoice_amount" in merged.columns else 0.0, errors="coerce").fillna(0.0)
    combined_df["paid_amount"] = pd.to_numeric(merged["paid_amount"] if "paid_amount" in merged.columns else 0.0, errors="coerce").fillna(0.0)

    if "payment_date" in merged.columns:
        combined_df["payment_date"] = merged["payment_date"].fillna(now_date)
    elif "issue_date" in merged.columns:
        combined_df["payment_date"] = merged["issue_date"].fillna(now_date)
    else:
        combined_df["payment_date"] = now_date

    if "payment_method" in merged.columns:
        combined_df["payment_method"] = merged["payment_method"].fillna("Gateway Settlement")
    else:
        combined_df["payment_method"] = "Gateway Settlement"

    if "gateway_status" in merged.columns:
        combined_df["status"] = merged["gateway_status"].fillna("SUCCESS")
    elif "status" in merged.columns:
        combined_df["status"] = merged["status"].fillna("SUCCESS")
    else:
        combined_df["status"] = "SUCCESS"

    return reconcile_transactions(combined_df)
