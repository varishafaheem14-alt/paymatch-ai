"""
PayMatch AI — Smart Payment Reconciliation & Finance Controller
Streamlit Web Application
Track 4: AI Finance Controller - Razorpay Internship Hackathon
"""

import os
import io
import streamlit as st
import pandas as pd
import numpy as np

from src.utils import format_inr, sanitize_and_validate_csv, generate_executive_summary
from src.reconciliation import (
    reconcile_transactions,
    reconcile_two_files,
    STATUS_MATCHED,
    STATUS_MISMATCH,
    STATUS_MISSING,
    STATUS_DUPLICATE,
    STATUS_PENDING,
)
from src.ai_assistant import (
    analyze_portfolio_health,
    explain_single_transaction,
    generate_customer_email,
    answer_finance_query,
)
from src.insights import (
    create_status_donut_chart,
    create_method_bar_chart,
    create_timeline_chart,
    get_priority_queue,
)


# ==========================================
# STREAMLIT PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="PayMatch AI — Smart Payment Reconciliation & Finance Controller",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================
# CUSTOM CSS / FINTECH THEME
# ==========================================
st.markdown(
    """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Top Header Branding */
    .brand-header {
        background: linear-gradient(135deg, #0A192F 0%, #0F2D59 50%, #1A4980 100%);
        padding: 24px 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(10, 25, 47, 0.2);
    }
    
    .brand-title {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .brand-badge {
        background: rgba(51, 149, 255, 0.2);
        color: #58A6FF;
        border: 1px solid rgba(88, 166, 255, 0.4);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    .brand-subtitle {
        font-size: 14px;
        color: #94A3B8;
        margin-top: 6px;
        margin-bottom: 0;
    }

    /* KPI Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.2s ease;
        margin-bottom: 12px;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
        border-color: #CBD5E1;
    }
    
    .metric-label {
        font-size: 13px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #0F172A;
        margin-top: 4px;
    }
    
    .metric-sub {
        font-size: 12px;
        font-weight: 500;
        margin-top: 4px;
    }
    
    /* Health Status Card */
    .health-card {
        background: #F8FAFC;
        border-left: 6px solid #10B981;
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    
    /* Status Badges */
    .badge-matched {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
    }
    
    .badge-mismatch {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
    }
    
    .badge-missing {
        background-color: #FDE8E8;
        color: #9B1C1C;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
    }
    
    .badge-duplicate {
        background-color: #EDE9FE;
        color: #5B21B6;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
    }
    
    .badge-pending {
        background-color: #E1EFFE;
        color: #1E429F;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        font-weight: 600;
        border-radius: 8px 8px 0px 0px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "raw_df" not in st.session_state:
    st.session_state["raw_df"] = None

if "reconciled_df" not in st.session_state:
    st.session_state["reconciled_df"] = None

if "metrics" not in st.session_state:
    st.session_state["metrics"] = {}

if "data_source_name" not in st.session_state:
    st.session_state["data_source_name"] = "None"

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "content": "👋 Hello! I am your **PayMatch AI Finance Controller**. How can I assist you with today's reconciliation audit?"}
    ]


def load_default_sample_data():
    """Load built-in realistic Indian demo dataset."""
    sample_path = os.path.join(os.path.dirname(__file__), "sample_data", "sample_transactions.csv")
    if os.path.exists(sample_path):
        df = pd.read_csv(sample_path)
        clean_df, err = sanitize_and_validate_csv(df)
        if clean_df is not None:
            rec_df, metrics = reconcile_transactions(clean_df)
            st.session_state["raw_df"] = clean_df
            st.session_state["reconciled_df"] = rec_df
            st.session_state["metrics"] = metrics
            st.session_state["data_source_name"] = "Sample Demo Dataset (45 transactions)"
            return True
    return False


# Auto-load sample data on initial launch if empty
if st.session_state["reconciled_df"] is None:
    load_default_sample_data()


# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("### ⚡ Control Center")
    
    data_mode = st.radio(
        "Data Ingestion Source:",
        ["⚡ Demo Mode (Instant)", "📤 Single Transaction CSV", "📑 Dual Upload (Invoices + Payments)"],
        index=0,
    )

    st.markdown("---")

    if data_mode == "⚡ Demo Mode (Instant)":
        if st.button("⚡ Reload Sample Demo Dataset", use_container_width=True, type="primary"):
            if load_default_sample_data():
                st.success("Loaded 45 demo transactions successfully!")
                st.rerun()

    elif data_mode == "📤 Single Transaction CSV":
        uploaded_file = st.file_uploader("Upload Transaction / Invoice CSV", type=["csv"])
        if uploaded_file is not None:
            try:
                raw_input_df = pd.read_csv(uploaded_file)
                clean_df, err = sanitize_and_validate_csv(raw_input_df)
                if err:
                    st.error(f"⚠️ {err}")
                else:
                    rec_df, metrics = reconcile_transactions(clean_df)
                    st.session_state["raw_df"] = clean_df
                    st.session_state["reconciled_df"] = rec_df
                    st.session_state["metrics"] = metrics
                    st.session_state["data_source_name"] = uploaded_file.name
                    st.success(f"Successfully processed {len(clean_df)} records!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error reading CSV: {str(e)}")

        with st.expander("ℹ️ Expected CSV Format"):
            st.code(
                """transaction_id,invoice_id,customer_name,invoice_amount,paid_amount,payment_date,payment_method,status
TXN-1001,INV-2026-001,Aarav Sharma,5000.00,5000.00,2026-08-01,Razorpay UPI,SUCCESS
TXN-1002,INV-2026-002,Pooja Patel,12500.00,12250.00,2026-08-02,Razorpay Cards,SUCCESS""",
                language="csv",
            )

    elif data_mode == "📑 Dual Upload (Invoices + Payments)":
        inv_file = st.file_uploader("1. Invoices CSV", type=["csv"], key="inv_file")
        pay_file = st.file_uploader("2. Gateway Payments CSV", type=["csv"], key="pay_file")

        if inv_file and pay_file:
            if st.button("Reconcile Files", type="primary", use_container_width=True):
                try:
                    df_inv = pd.read_csv(inv_file)
                    df_pay = pd.read_csv(pay_file)
                    rec_df, metrics = reconcile_two_files(df_inv, df_pay)
                    st.session_state["raw_df"] = rec_df
                    st.session_state["reconciled_df"] = rec_df
                    st.session_state["metrics"] = metrics
                    st.session_state["data_source_name"] = f"Merged: {inv_file.name} & {pay_file.name}"
                    st.success("Reconciled 2 files successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to reconcile files: {str(e)}")

    st.markdown("---")
    st.markdown("### 🤖 AI Engine Settings")
    api_key_input = st.text_input(
        "Gemini API Key (Optional)",
        value=os.environ.get("GEMINI_API_KEY", ""),
        type="password",
        help="Optional: Enter a Gemini API key for live generative conversational Q&A. The app automatically uses an intelligent zero-dependency fallback engine if no key is provided.",
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 11px; color: #64748B; line-height: 1.4;">
        <b>PayMatch AI — Finance Controller</b><br>
        Track 4: AI Finance Controller<br>
        Razorpay Internship Hackathon<br>
        <i>Built for automated invoice & payment reconciliation.</i>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================
# TOP BRANDING BANNER
# ==========================================
st.markdown(
    """
    <div class="brand-header">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <div class="brand-title">
                    <span>💳 PayMatch AI</span>
                    <span class="brand-badge">Track 4: AI Finance Controller</span>
                </div>
                <div class="brand-subtitle">
                    Autonomous Payment Reconciliation • Discrepancy Diagnostics • MDR Fee Detection • Smart Recovery
                </div>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 12px; color: #94A3B8;">Active Dataset:</span><br>
                <span style="font-size: 14px; font-weight: 600; color: #38BDF8;">"""
    + str(st.session_state.get("data_source_name", "Demo"))
    + """</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# Retrieve current state
df = st.session_state.get("reconciled_df")
metrics = st.session_state.get("metrics", {})

if df is None or df.empty:
    st.warning("⚠️ No transaction data loaded. Please select Demo Mode in the sidebar or upload a CSV file.")
    st.stop()


# ==========================================
# MAIN APPLICATION TABS
# ==========================================
tab_dashboard, tab_transactions, tab_assistant, tab_insights, tab_export = st.tabs(
    [
        "📊 Executive Dashboard",
        "🔍 Transaction Audit",
        "🤖 AI Finance Assistant",
        "📈 Financial Analytics",
        "📥 Export & Reports",
    ]
)


# -------------------------------------------------------------
# TAB 1: EXECUTIVE DASHBOARD
# -------------------------------------------------------------
with tab_dashboard:
    # Portfolio Health Assessment Card
    health_info = analyze_portfolio_health(metrics, df)
    st.markdown(
        f"""
        <div class="health-card" style="border-left-color: {health_info['health_color']};">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <span style="font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">Portfolio Health Audit</span>
                    <h3 style="margin: 2px 0 6px 0; color: #0F172A; font-size: 20px;">{health_info['health_status']}</h3>
                    <p style="margin: 0; font-size: 14px; color: #475569;">{health_info['health_message']}</p>
                </div>
                <div style="text-align: right; padding-top: 6px;">
                    <span style="font-size: 12px; color: #64748B;">Total Amount at Risk</span>
                    <h2 style="margin: 0; color: #EF4444; font-size: 26px; font-weight: 800;">{health_info['risk_amount_formatted']}</h2>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Top KPI Metrics Cards Row (Grid of 4 & 4)
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Total Transactions</div>
                <div class="metric-value">{metrics.get('total_transactions', 0):,}</div>
                <div class="metric-sub" style="color: #64748B;">Total Volume Ingested</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with kpi_col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Invoiced Value</div>
                <div class="metric-value">{format_inr(metrics.get('total_invoiced_amount', 0.0))}</div>
                <div class="metric-sub" style="color: #3B82F6;">Total Billed Revenue</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with kpi_col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Settled Amount</div>
                <div class="metric-value">{format_inr(metrics.get('total_paid_amount', 0.0))}</div>
                <div class="metric-sub" style="color: #10B981;">Total Received Funds</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with kpi_col4:
        rate = metrics.get('reconciliation_rate', 0.0)
        rate_color = "#10B981" if rate >= 85 else ("#F59E0B" if rate >= 65 else "#EF4444")
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Reconciliation Rate</div>
                <div class="metric-value" style="color: {rate_color};">{rate:.1f}%</div>
                <div class="metric-sub" style="color: {rate_color};">Matched Cleanly</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Status Breakdown Mini KPIs
    s_col1, s_col2, s_col3, s_col4 = st.columns(4)
    with s_col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">✅ Matched</div>
                <div class="metric-value" style="color: #10B981;">{metrics.get('matched_count', 0)}</div>
                <div class="metric-sub" style="color: #64748B;">{format_inr(metrics.get('matched_amount', 0.0))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with s_col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">⚠️ Mismatches</div>
                <div class="metric-value" style="color: #F59E0B;">{metrics.get('mismatch_count', 0)}</div>
                <div class="metric-sub" style="color: #F59E0B;">Diff: {format_inr(metrics.get('mismatch_diff', 0.0))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with s_col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">❌ Missing Payments</div>
                <div class="metric-value" style="color: #EF4444;">{metrics.get('missing_count', 0)}</div>
                <div class="metric-sub" style="color: #EF4444;">Unpaid: {format_inr(metrics.get('missing_amount', 0.0))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with s_col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">🔄 Duplicates</div>
                <div class="metric-value" style="color: #8B5CF6;">{metrics.get('duplicate_count', 0)}</div>
                <div class="metric-sub" style="color: #8B5CF6;">Double Charges Detected</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts Row
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.plotly_chart(create_status_donut_chart(metrics), use_container_width=True)
    with chart_col2:
        st.plotly_chart(create_method_bar_chart(df), use_container_width=True)

    # Priority Action Queue
    st.markdown("### 🚨 High-Priority Action Items (Finance Controller Queue)")
    priority_items = get_priority_queue(df)
    
    if priority_items.empty:
        st.success("🎉 All transactions are fully reconciled! No outstanding discrepancies.")
    else:
        # Show top 5 priority items
        for _, item in priority_items.head(4).iterrows():
            status_badge_class = "badge-mismatch"
            if item["reconciliation_status"] == STATUS_MISSING:
                status_badge_class = "badge-missing"
            elif item["reconciliation_status"] == STATUS_DUPLICATE:
                status_badge_class = "badge-duplicate"

            with st.expander(
                f"[{item['risk_level']}] {item['invoice_id']} — {item['customer_name']} | Variance: {format_inr(item['difference'])} ({item['reconciliation_status']})"
            ):
                st.markdown(explain_single_transaction(item))
                
                # Email resolution action
                st.markdown("**✉️ One-Click Resolution Outreach Template:**")
                st.code(generate_customer_email(item), language="markdown")


# -------------------------------------------------------------
# TAB 2: RECONCILED TRANSACTIONS AUDIT TABLE
# -------------------------------------------------------------
with tab_transactions:
    st.markdown("### 🔍 Searchable Reconciliation Audit Table")

    filter_col1, filter_col2, filter_col3 = st.columns([2, 2, 3])

    with filter_col1:
        status_filter = st.selectbox(
            "Filter by Reconciliation Status:",
            ["ALL", STATUS_MATCHED, STATUS_MISMATCH, STATUS_MISSING, STATUS_DUPLICATE, STATUS_PENDING],
            index=0,
        )

    with filter_col2:
        method_filter = st.selectbox(
            "Filter by Payment Channel:",
            ["ALL"] + sorted(df["payment_method"].dropna().unique().tolist()),
            index=0,
        )

    with filter_col3:
        search_term = st.text_input(
            "Search by Transaction ID, Invoice ID, or Customer:",
            "",
            placeholder="e.g. TXN-1003 or Zomato or INV-2026-004",
        )

    # Apply filtering
    filtered_df = df.copy()

    if status_filter != "ALL":
        filtered_df = filtered_df[filtered_df["reconciliation_status"] == status_filter]

    if method_filter != "ALL":
        filtered_df = filtered_df[filtered_df["payment_method"] == method_filter]

    if search_term.strip():
        term = search_term.strip().lower()
        filtered_df = filtered_df[
            filtered_df["transaction_id"].str.lower().str.contains(term, na=False)
            | filtered_df["invoice_id"].str.lower().str.contains(term, na=False)
            | filtered_df["customer_name"].str.lower().str.contains(term, na=False)
        ]

    st.markdown(f"**Showing {len(filtered_df)} of {len(df)} transactions**")

    # Display Table with Formatting
    display_df = filtered_df[
        [
            "transaction_id",
            "invoice_id",
            "customer_name",
            "invoice_amount",
            "paid_amount",
            "difference",
            "reconciliation_status",
            "risk_level",
            "payment_method",
            "payment_date",
            "recommended_action",
        ]
    ].copy()

    # Format amounts with INR currency
    display_df["invoice_amount"] = display_df["invoice_amount"].apply(format_inr)
    display_df["paid_amount"] = display_df["paid_amount"].apply(format_inr)
    display_df["difference"] = display_df["difference"].apply(format_inr)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "transaction_id": st.column_config.TextColumn("Txn ID", width="medium"),
            "invoice_id": st.column_config.TextColumn("Invoice ID", width="medium"),
            "customer_name": st.column_config.TextColumn("Customer", width="large"),
            "invoice_amount": st.column_config.TextColumn("Invoiced", width="small"),
            "paid_amount": st.column_config.TextColumn("Paid", width="small"),
            "difference": st.column_config.TextColumn("Difference", width="small"),
            "reconciliation_status": st.column_config.TextColumn("Status", width="medium"),
            "risk_level": st.column_config.TextColumn("Risk", width="small"),
            "payment_method": st.column_config.TextColumn("Method", width="medium"),
            "payment_date": st.column_config.TextColumn("Date", width="small"),
            "recommended_action": st.column_config.TextColumn("Recommended Action", width="large"),
        },
    )

    st.markdown("---")
    st.markdown("### 🔬 Inspect Single Transaction Discrepancy")
    selected_txn_id = st.selectbox(
        "Select a Transaction to Inspect AI Diagnosis & Draft Action:",
        filtered_df["transaction_id"].unique(),
    )

    if selected_txn_id:
        selected_row = filtered_df[filtered_df["transaction_id"] == selected_txn_id].iloc[0]
        st.markdown(explain_single_transaction(selected_row))
        st.markdown("**✉️ Generated Merchant Recovery / Confirmation Email:**")
        st.code(generate_customer_email(selected_row), language="markdown")


# -------------------------------------------------------------
# TAB 3: AI FINANCE ASSISTANT
# -------------------------------------------------------------
with tab_assistant:
    st.markdown("### 🤖 PayMatch AI Finance Assistant")
    st.markdown(
        "Ask questions about discrepancies, financial risk, Razorpay fees, duplicate transactions, or draft resolution emails."
    )

    # Quick Prompt Buttons
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    quick_query = None

    with q_col1:
        if st.button("🚨 What is our biggest risk?", use_container_width=True):
            quick_query = "What is our biggest financial risk?"
    with q_col2:
        if st.button("❌ Missing Payments Audit", use_container_width=True):
            quick_query = "Show me missing payments and unpaid customers"
    with q_col3:
        if st.button("💳 Razorpay MDR Fee Analysis", use_container_width=True):
            quick_query = "How should we handle Razorpay MDR fee deductions?"
    with q_col4:
        if st.button("🔄 Duplicate Charges Audit", use_container_width=True):
            quick_query = "Explain duplicate transactions and chargeback risks"

    # Display chat history
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_query = st.chat_input("Ask PayMatch AI Finance Assistant...")
    final_query = quick_query or user_query

    if final_query:
        st.session_state["chat_history"].append({"role": "user", "content": final_query})
        with st.chat_message("user"):
            st.markdown(final_query)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing ledger data..."):
                response_text = answer_finance_query(
                    query=final_query,
                    df=df,
                    metrics=metrics,
                    api_key=api_key_input,
                )
                st.markdown(response_text)
                st.session_state["chat_history"].append({"role": "assistant", "content": response_text})


# -------------------------------------------------------------
# TAB 4: FINANCIAL ANALYTICS & DEEP INSIGHTS
# -------------------------------------------------------------
with tab_insights:
    st.markdown("### 📈 Deep Financial Analytics & Risk Patterns")

    ins_col1, ins_col2 = st.columns(2)
    with ins_col1:
        st.plotly_chart(create_timeline_chart(df), use_container_width=True)
    with ins_col2:
        # Top Discrepancies by Customer
        flagged_cust = (
            df[df["reconciliation_status"] != STATUS_MATCHED]
            .groupby("customer_name")["difference"]
            .apply(lambda x: x.abs().sum())
            .reset_index(name="total_discrepancy")
            .sort_values(by="total_discrepancy", ascending=False)
            .head(8)
        )
        if not flagged_cust.empty:
            import plotly.express as px
            fig_cust = px.bar(
                flagged_cust,
                x="total_discrepancy",
                y="customer_name",
                orientation="h",
                title="<b>Top Variance Exposure by Customer (₹)</b>",
                color="total_discrepancy",
                color_continuous_scale="Reds",
                labels={"total_discrepancy": "Discrepancy (₹)", "customer_name": "Customer"},
            )
            fig_cust.update_layout(height=340, margin=dict(t=50, b=30, l=20, r=20))
            st.plotly_chart(fig_cust, use_container_width=True)
        else:
            st.info("No customer discrepancies found.")

    st.markdown("---")
    st.markdown("### 📋 Root Cause Distribution Breakdown")
    root_cause_counts = df["reconciliation_status"].value_counts().reset_index()
    root_cause_counts.columns = ["Status", "Count"]
    root_cause_counts["Percentage"] = (root_cause_counts["Count"] / len(df) * 100).round(1).astype(str) + "%"
    st.table(root_cause_counts)


# -------------------------------------------------------------
# TAB 5: EXPORT & REPORTS
# -------------------------------------------------------------
with tab_export:
    st.markdown("### 📥 Export Reconciliation Audit Reports")
    st.markdown("Download enriched reconciliation files for compliance, ERP import, or executive stakeholder presentation.")

    exp_col1, exp_col2 = st.columns(2)

    with exp_col1:
        st.markdown("#### 📊 Enriched Reconciliation CSV")
        st.write("Contains full transaction dataset enriched with flags, difference calculations, risk tiers, and AI action items.")
        
        # Prepare CSV bytes
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue().encode("utf-8")

        st.download_button(
            label="⬇️ Download Reconciliation CSV Report",
            data=csv_data,
            file_name=f"PayMatch_AI_Reconciliation_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True,
        )

    with exp_col2:
        st.markdown("#### 📑 Executive Summary Markdown Report")
        st.write("Formatted audit report with high-level KPI summaries, health ratings, and top priority action items.")
        
        exec_summary = generate_executive_summary(metrics, get_priority_queue(df))
        
        st.download_button(
            label="⬇️ Download Executive Summary Report (.md)",
            data=exec_summary.encode("utf-8"),
            file_name=f"PayMatch_AI_Executive_Summary_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.markdown("---")
    st.markdown("#### 👁️ Live Preview of Executive Report")
    st.markdown(exec_summary)
