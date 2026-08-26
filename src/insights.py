"""
Analytics, Visualizations, and Risk Insights for PayMatch AI.
Builds interactive Plotly charts and financial risk queues.
"""

from typing import Dict, Any
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from .utils import format_inr


# Fintech Theme Colors
COLOR_MATCHED = "#10B981"    # Emerald Green
COLOR_MISMATCH = "#F59E0B"   # Amber Orange
COLOR_MISSING = "#EF4444"    # Coral Red
COLOR_DUPLICATE = "#8B5CF6"  # Purple
COLOR_PENDING = "#3B82F6"    # Razorpay Blue
COLOR_BG = "#FFFFFF"
FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif"


def create_status_donut_chart(metrics: Dict[str, Any]) -> go.Figure:
    """Create a sleek fintech donut chart showing reconciliation breakdown."""
    labels = ["Matched", "Mismatch", "Missing Payment", "Duplicate", "Pending"]
    values = [
        metrics.get("matched_count", 0),
        metrics.get("mismatch_count", 0),
        metrics.get("missing_count", 0),
        metrics.get("duplicate_count", 0),
        metrics.get("pending_count", 0),
    ]
    colors = [COLOR_MATCHED, COLOR_MISMATCH, COLOR_MISSING, COLOR_DUPLICATE, COLOR_PENDING]

    # Filter out 0 count items for clean presentation
    clean_labels = [l for l, v in zip(labels, values) if v > 0]
    clean_values = [v for v in values if v > 0]
    clean_colors = [c for c, v in zip(colors, values) if v > 0]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=clean_labels,
                values=clean_values,
                hole=0.62,
                marker=dict(colors=clean_colors, line=dict(color="#FFFFFF", width=2)),
                textinfo="percent+label",
                textposition="outside",
                hoverinfo="label+value+percent",
            )
        ]
    )

    rec_rate = metrics.get("reconciliation_rate", 0.0)

    fig.update_layout(
        title=dict(
            text="<b>Reconciliation Status Distribution</b>",
            font=dict(size=16, family=FONT_FAMILY, color="#1E293B"),
            x=0.05,
        ),
        annotations=[
            dict(
                text=f"<b>{rec_rate:.1f}%</b><br><span style='font-size:12px;color:#64748B;'>Matched</span>",
                x=0.5,
                y=0.5,
                font=dict(size=22, family=FONT_FAMILY, color="#0F172A"),
                showarrow=False,
            )
        ],
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(t=50, b=40, l=20, r=20),
        height=340,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def create_method_bar_chart(df: pd.DataFrame) -> go.Figure:
    """Create a breakdown of reconciliation status by payment method."""
    if df is None or df.empty or "payment_method" not in df.columns:
        return go.Figure()

    grouped = (
        df.groupby(["payment_method", "reconciliation_status"])
        .size()
        .reset_index(name="count")
    )

    color_map = {
        "MATCHED": COLOR_MATCHED,
        "MISMATCH": COLOR_MISMATCH,
        "MISSING PAYMENT": COLOR_MISSING,
        "DUPLICATE": COLOR_DUPLICATE,
        "PENDING": COLOR_PENDING,
    }

    fig = px.bar(
        grouped,
        x="payment_method",
        y="count",
        color="reconciliation_status",
        color_discrete_map=color_map,
        title="<b>Payment Channel Performance & Discrepancies</b>",
        barmode="stack",
        labels={"payment_method": "Payment Method", "count": "Transactions", "reconciliation_status": "Status"},
    )

    fig.update_layout(
        font=dict(family=FONT_FAMILY),
        margin=dict(t=50, b=30, l=20, r=20),
        height=340,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
    )
    return fig


def create_timeline_chart(df: pd.DataFrame) -> go.Figure:
    """Create a timeline chart comparing invoiced vs settled amounts over time."""
    if df is None or df.empty or "payment_date" not in df.columns:
        return go.Figure()

    temp_df = df.copy()
    temp_df["payment_date"] = pd.to_datetime(temp_df["payment_date"], errors="coerce")
    temp_df = temp_df.dropna(subset=["payment_date"]).sort_values("payment_date")

    if temp_df.empty:
        return go.Figure()

    daily = (
        temp_df.groupby(temp_df["payment_date"].dt.strftime("%Y-%m-%d"))
        .agg(
            total_invoiced=("invoice_amount", "sum"),
            total_paid=("paid_amount", "sum"),
        )
        .reset_index()
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=daily["payment_date"],
            y=daily["total_invoiced"],
            name="Invoiced Amount",
            mode="lines+markers",
            line=dict(color="#3B82F6", width=3),
            marker=dict(size=6),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=daily["payment_date"],
            y=daily["total_paid"],
            name="Settled / Received",
            mode="lines+markers",
            line=dict(color="#10B981", width=3, dash="dot"),
            marker=dict(size=6),
        )
    )

    fig.update_layout(
        title="<b>Daily Settlement vs Billed Timeline</b>",
        font=dict(family=FONT_FAMILY),
        margin=dict(t=50, b=30, l=20, r=20),
        height=340,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, title="Date"),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title="Amount (₹)"),
    )
    return fig


def get_priority_queue(df: pd.DataFrame) -> pd.DataFrame:
    """Extract top flagged high-risk items that require immediate finance team action."""
    if df is None or df.empty:
        return pd.DataFrame()

    flagged = df[df["reconciliation_status"] != "MATCHED"].copy()
    if flagged.empty:
        return pd.DataFrame()

    # Sort by risk level and discrepancy magnitude
    flagged["sort_weight"] = flagged["risk_level"].map({"High Risk": 3, "Medium Risk": 2, "Low Risk": 1}).fillna(0)
    flagged["abs_diff"] = flagged["difference"].abs()
    
    # Priority sort
    priority_df = flagged.sort_values(by=["sort_weight", "abs_diff", "invoice_amount"], ascending=[False, False, False])
    return priority_df
