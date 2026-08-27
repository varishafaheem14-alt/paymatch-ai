"""
Vercel Serverless API Handler & Fallback Server for PayMatch AI.
Provides REST endpoints and serves static frontend assets when routed through serverless.
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler
import io
import pandas as pd

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

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


class handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        parsed_path = self.path.split("?")[0].strip()

        # 1. API Health Endpoint
        if parsed_path in ["/api/health", "/api/health/"]:
            self._set_headers(200, "application/json")
            self.wfile.write(
                json.dumps({"status": "ok", "app": "PayMatch AI", "version": "1.0.0"}).encode("utf-8")
            )
            return

        # 2. API Sample Data Endpoint
        elif parsed_path in ["/api/sample", "/api/sample/"]:
            sample_path = os.path.join(parent_dir, "sample_data", "sample_transactions.csv")
            if os.path.exists(sample_path):
                df = pd.read_csv(sample_path)
                clean_df, err = sanitize_and_validate_csv(df)
                if clean_df is not None:
                    rec_df, metrics = reconcile_transactions(clean_df)
                    health = analyze_portfolio_health(metrics, rec_df)
                    self._set_headers(200, "application/json")
                    response_data = {
                        "transactions": rec_df.to_dict(orient="records"),
                        "metrics": metrics,
                        "health": health,
                    }
                    self.wfile.write(json.dumps(response_data).encode("utf-8"))
                    return

            self._set_headers(404, "application/json")
            self.wfile.write(json.dumps({"error": "Sample data file not found"}).encode("utf-8"))
            return

        # 3. Static Style CSS
        elif parsed_path == "/style.css":
            css_path = os.path.join(parent_dir, "style.css")
            if os.path.exists(css_path):
                with open(css_path, "rb") as f:
                    content = f.read()
                self._set_headers(200, "text/css; charset=utf-8")
                self.wfile.write(content)
                return

        # 4. Static App JS
        elif parsed_path == "/app.js":
            js_path = os.path.join(parent_dir, "app.js")
            if os.path.exists(js_path):
                with open(js_path, "rb") as f:
                    content = f.read()
                self._set_headers(200, "application/javascript; charset=utf-8")
                self.wfile.write(content)
                return

        # 5. Root / SPA Fallback to index.html
        index_path = os.path.join(parent_dir, "index.html")
        if os.path.exists(index_path):
            with open(index_path, "rb") as f:
                content = f.read()
            self._set_headers(200, "text/html; charset=utf-8")
            self.wfile.write(content)
            return

        self._set_headers(404, "application/json")
        self.wfile.write(json.dumps({"error": "Resource not found"}).encode("utf-8"))

    def do_POST(self):
        parsed_path = self.path.split("?")[0].strip()
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""

        try:
            body = json.loads(post_data) if post_data else {}
        except Exception:
            body = {}

        if parsed_path in ["/api/reconcile", "/api/reconcile/"]:
            csv_content = body.get("csv_content", "")
            transactions_data = body.get("transactions", None)

            if csv_content:
                df = pd.read_csv(io.StringIO(csv_content))
            elif transactions_data:
                df = pd.DataFrame(transactions_data)
            else:
                self._set_headers(400, "application/json")
                self.wfile.write(json.dumps({"error": "Missing csv_content or transactions payload"}).encode("utf-8"))
                return

            clean_df, err = sanitize_and_validate_csv(df)
            if err:
                self._set_headers(400, "application/json")
                self.wfile.write(json.dumps({"error": err}).encode("utf-8"))
                return

            rec_df, metrics = reconcile_transactions(clean_df)
            health = analyze_portfolio_health(metrics, rec_df)

            self._set_headers(200, "application/json")
            self.wfile.write(
                json.dumps(
                    {
                        "transactions": rec_df.to_dict(orient="records"),
                        "metrics": metrics,
                        "health": health,
                    }
                ).encode("utf-8")
            )

        elif parsed_path in ["/api/query", "/api/query/"]:
            query = body.get("query", "")
            transactions_data = body.get("transactions", [])
            api_key = body.get("api_key", None)

            df = pd.DataFrame(transactions_data) if transactions_data else pd.DataFrame()
            metrics = body.get("metrics", {})

            answer = answer_finance_query(query=query, df=df, metrics=metrics, api_key=api_key)

            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({"answer": answer}).encode("utf-8"))

        else:
            self._set_headers(404, "application/json")
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))
