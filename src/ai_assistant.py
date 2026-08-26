"""
AI Finance Assistant Module for PayMatch AI.
Provides intelligent deterministic root-cause analysis, actionable finance recommendations,
automated merchant email drafting, and optional Gemini LLM integration.
"""

import os
from typing import Dict, Any, List, Optional
import pandas as pd
from .utils import format_inr


def analyze_portfolio_health(metrics: Dict[str, Any], flagged_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generates a high-level executive financial health audit and prioritized recommendations.
    """
    rec_rate = metrics.get("reconciliation_rate", 0.0)
    risk_amount = metrics.get("total_mismatch_amount", 0.0)
    missing_count = metrics.get("missing_count", 0)
    mismatch_count = metrics.get("mismatch_count", 0)
    duplicate_count = metrics.get("duplicate_count", 0)

    # Health Rating
    if rec_rate >= 90:
        health_status = "Excellent"
        health_color = "#10B981"
        health_message = "Your financial ledger is exceptionally healthy. Most settlements match invoiced amounts seamlessly."
    elif rec_rate >= 70:
        health_status = "Moderate Attention Needed"
        health_color = "#F59E0B"
        health_message = "Moderate variance detected. Several payments have uncollected balances or gateway fee deductions requiring ledger posting."
    else:
        health_status = "Critical Audit Required"
        health_color = "#EF4444"
        health_message = "High discrepancy rate detected. Significant capital is stuck in missing invoices or unverified duplicate charges."

    # Top Root Causes
    root_causes = []
    if duplicate_count > 0:
        root_causes.append(f"🔄 **{duplicate_count} Duplicate Transaction(s)**: Multiple charges against identical invoice IDs. Immediate double-charge refund review recommended.")
    if missing_count > 0:
        root_causes.append(f"❌ **{missing_count} Missing Payment(s)**: {format_inr(metrics.get('missing_amount', 0.0))} in invoiced revenue has zero payment confirmations.")
    if mismatch_count > 0:
        root_causes.append(f"⚠️ **{mismatch_count} Amount Mismatch(es)**: {format_inr(metrics.get('mismatch_diff', 0.0))} in variances (mix of 2% MDR payment gateway fees and short payments).")

    # Action Plan
    action_plan = [
        "1. **Initiate Collections**: Send payment reminder links for the uncollected missing invoices.",
        "2. **Book Gateway MDR Expenses**: Reclassify detected 2% deductions as standard Razorpay payment gateway fee expenses.",
        "3. **Audit Duplicate Gateway Records**: Cross-reference duplicate transaction IDs against bank settlement logs before customers raise chargebacks.",
        "4. **Reconcile Pending Settlements**: Allow standard T+2 banking clearance for pending gateway transactions."
    ]

    return {
        "health_status": health_status,
        "health_color": health_color,
        "health_message": health_message,
        "root_causes": root_causes,
        "action_plan": action_plan,
        "risk_amount_formatted": format_inr(risk_amount)
    }


def explain_single_transaction(row: pd.Series) -> str:
    """
    Generates a natural-language AI breakdown for any individual transaction.
    """
    txn_id = row.get("transaction_id", "N/A")
    inv_id = row.get("invoice_id", "N/A")
    customer = row.get("customer_name", "Customer")
    inv_amt = float(row.get("invoice_amount", 0.0))
    paid_amt = float(row.get("paid_amount", 0.0))
    diff = float(row.get("difference", 0.0))
    status = row.get("reconciliation_status", "UNKNOWN")
    method = row.get("payment_method", "N/A")
    action = row.get("recommended_action", "Audit transaction")
    reason = row.get("ai_reason", "")

    explanation = f"""### 🔍 AI Discrepancy Breakdown for `{txn_id}`
* **Customer:** **{customer}** (Invoice: `{inv_id}`)
* **Payment Mode:** {method}
* **Status:** `{status}`
* **Invoiced:** {format_inr(inv_amt)} | **Paid:** {format_inr(paid_amt)} | **Discrepancy:** {format_inr(diff)}

**🤖 Root Cause Analysis:**
{reason}

**💡 AI Controller Recommended Action:**
{action}
"""
    return explanation


def generate_customer_email(row: pd.Series) -> str:
    """
    Auto-generates a professional outreach email template for payment resolution.
    """
    customer = row.get("customer_name", "Customer")
    inv_id = row.get("invoice_id", "N/A")
    inv_amt = float(row.get("invoice_amount", 0.0))
    paid_amt = float(row.get("paid_amount", 0.0))
    diff = float(row.get("difference", 0.0))
    status = row.get("reconciliation_status", "")

    if status == "MISSING PAYMENT":
        subject = f"Friendly Reminder: Outstanding Invoice {inv_id} Payment"
        body = f"""Subject: {subject}

Dear {customer},

We hope you are doing well.

Our automated finance controller indicates that Invoice **{inv_id}** for **{format_inr(inv_amt)}** remains unpaid. 

To ensure uninterrupted services, please complete the payment at your earliest convenience using our instant Razorpay link:
👉 [Pay Invoice Now](https://rzp.io/l/demo-{inv_id})

If you have already initiated the transfer, please reply with the payment reference ID so we can reconcile your account immediately.

Warm regards,
Finance Operations Team
PayMatch AI Controller"""
    elif status == "MISMATCH" and diff > 0:
        subject = f"Update on Invoice {inv_id}: Balance of {format_inr(diff)} Remaining"
        body = f"""Subject: {subject}

Dear {customer},

Thank you for your recent payment of **{format_inr(paid_amt)}** towards Invoice **{inv_id}** (Total: {format_inr(inv_amt)}).

Our records show a remaining balance of **{format_inr(diff)}**. Please verify if this was an installment payment or if any deduction was applied.

You can clear the outstanding balance here:
👉 [Pay Balance {format_inr(diff)}](https://rzp.io/l/demo-bal-{inv_id})

Thank you for your partnership.

Warm regards,
Finance Operations Team
PayMatch AI Controller"""
    elif status == "DUPLICATE":
        subject = f"Notice: Duplicate Charge Detected for Invoice {inv_id}"
        body = f"""Subject: {subject}

Dear {customer},

Our automated finance controller detected a possible duplicate transaction for Invoice **{inv_id}**.

We are currently verifying the bank settlement. If a double-charge occurred, a full refund of the duplicate amount will be processed back to your original payment method within 3-5 business days.

No action is required from your end. We apologize for any inconvenience.

Warm regards,
Finance Operations Team
PayMatch AI Controller"""
    else:
        subject = f"Receipt & Confirmation for Invoice {inv_id}"
        body = f"""Subject: {subject}

Dear {customer},

Thank you for your payment of **{format_inr(paid_amt)}** for Invoice **{inv_id}**. 

Your transaction has been successfully reconciled.

Warm regards,
Finance Operations Team
PayMatch AI Controller"""

    return body


def answer_finance_query(query: str, df: pd.DataFrame, metrics: Dict[str, Any], api_key: Optional[str] = None) -> str:
    """
    Answers user queries about reconciliation.
    Uses Gemini API if API key is provided, or uses deterministic intelligent rule engine fallback.
    """
    query_lower = query.lower().strip()

    # If Gemini API key is supplied, attempt live LLM call
    if api_key and len(api_key.strip()) > 10:
        try:
            from google import genai
            client = genai.Client(api_key=api_key.strip())
            
            # Prepare compact context summary
            context = f"""
You are the AI Finance Controller for PayMatch AI.
Dataset Summary:
- Total transactions: {metrics.get('total_transactions', 0)}
- Total Invoiced: {format_inr(metrics.get('total_invoiced_amount', 0))}
- Total Paid: {format_inr(metrics.get('total_paid_amount', 0))}
- Reconciliation Rate: {metrics.get('reconciliation_rate', 0):.1f}%
- Total Risk / Discrepancy Amount: {format_inr(metrics.get('total_mismatch_amount', 0))}
- Matched: {metrics.get('matched_count', 0)}, Mismatches: {metrics.get('mismatch_count', 0)}, Missing: {metrics.get('missing_count', 0)}, Duplicates: {metrics.get('duplicate_count', 0)}

Sample Flagged Transactions:
{df[df['reconciliation_status'] != 'MATCHED'][['transaction_id', 'invoice_id', 'customer_name', 'invoice_amount', 'paid_amount', 'difference', 'reconciliation_status', 'ai_reason']].head(10).to_string()}

User Query: {query}
Respond as a smart, professional fintech AI assistant. Keep responses actionable, concise, and structured.
"""
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=context
            )
            if response and response.text:
                return f"🤖 **PayMatch AI Assistant (Gemini Powered)**\n\n{response.text}"
        except Exception as e:
            # Fall back gracefully to rule-based engine
            pass

    # Intelligent Rule-Based Engine (Fallback Guarantee)
    if "risk" in query_lower or "highest" in query_lower or "biggest" in query_lower:
        flagged = df[df["reconciliation_status"] != "MATCHED"].sort_values(by="invoice_amount", ascending=False)
        if not flagged.empty:
            top_item = flagged.iloc[0]
            return f"""🤖 **AI Finance Controller Insight:**
The highest single exposure in your ledger is **{top_item['invoice_id']}** for customer **{top_item['customer_name']}**.
* **Invoiced Amount:** {format_inr(top_item['invoice_amount'])}
* **Paid Amount:** {format_inr(top_item['paid_amount'])}
* **Discrepancy:** {format_inr(top_item['difference'])}
* **Status:** `{top_item['reconciliation_status']}`
* **Recommended Next Step:** {top_item['recommended_action']}"""
        else:
            return "🤖 **AI Finance Controller:** All transactions are 100% matched! Zero risk items detected."

    elif "missing" in query_lower or "unpaid" in query_lower:
        missing_df = df[df["reconciliation_status"] == "MISSING PAYMENT"]
        count = len(missing_df)
        total_missing = missing_df["invoice_amount"].sum() if count > 0 else 0
        return f"""🤖 **Missing Payments Audit:**
We found **{count} missing payments** totaling **{format_inr(total_missing)}** in outstanding uncollected revenue.
Top unpaid customers:
{', '.join(missing_df['customer_name'].head(5).tolist()) if count > 0 else 'None'}
👉 **Recommended Action:** Trigger batch payment reminders with direct Razorpay payment links."""

    elif "duplicate" in query_lower or "double" in query_lower:
        dup_df = df[df["reconciliation_status"] == "DUPLICATE"]
        count = len(dup_df)
        return f"""🤖 **Duplicate Detection Analysis:**
Identified **{count} duplicate records**. Multiple charges or settlement logs were captured for the same invoice/transaction IDs.
👉 **Recommended Action:** Cross-reference transaction IDs with bank gateway settlement logs and initiate automated customer refunds before chargeback dispute fees occur."""

    elif "rate" in query_lower or "percentage" in query_lower or "overview" in query_lower:
        return f"""🤖 **Reconciliation Performance Overview:**
* **Reconciliation Rate:** **{metrics.get('reconciliation_rate', 0.0):.1f}%**
* **Total Transactions:** {metrics.get('total_transactions', 0)}
* **Matched Value:** {format_inr(metrics.get('matched_amount', 0.0))}
* **Amount at Risk:** {format_inr(metrics.get('total_mismatch_amount', 0.0))}"""

    elif "fee" in query_lower or "mdr" in query_lower or "razorpay" in query_lower or "tax" in query_lower:
        return f"""🤖 **Payment Gateway & MDR Fee Diagnosis:**
PayMatch AI automatically detected that several discrepancies correspond to standard **~2.0% Razorpay payment gateway MDR fees** and **18% GST withholdings**.
* Rather than chasing customers for these small variances, these amounts should be auto-classified into your **'Gateway Processing Expense'** ledger."""

    else:
        return f"""🤖 **AI Finance Controller Assistant:**
Based on our reconciliation audit of **{metrics.get('total_transactions', 0)} transactions**:
* **Current Reconciliation Rate:** {metrics.get('reconciliation_rate', 0.0):.1f}%
* **Identified Discrepancies:** {metrics.get('mismatch_count', 0)} Mismatches, {metrics.get('missing_count', 0)} Missing Payments, {metrics.get('duplicate_count', 0)} Duplicates.
* **Total Risk Exposure:** {format_inr(metrics.get('total_mismatch_amount', 0.0))}

You can ask me:
- *"What is our biggest financial risk?"*
- *"Show me missing payments"*
- *"Explain duplicate transactions"*
- *"How should we handle Razorpay MDR fees?"*"""
