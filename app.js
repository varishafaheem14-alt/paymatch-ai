/**
 * PayMatch AI — Production Frontend Application Logic
 * Track 4: AI Finance Controller - Razorpay Internship Hackathon
 */

// Embedded Realistic Indian Demo Transactions Dataset (45 Txns)
const DEFAULT_DEMO_DATA = [
  { transaction_id: "TXN-1001", invoice_id: "INV-2026-001", customer_name: "Aarav Sharma", invoice_amount: 5000.00, paid_amount: 5000.00, payment_date: "2026-08-01", payment_method: "Razorpay UPI", status: "SUCCESS" },
  { transaction_id: "TXN-1002", invoice_id: "INV-2026-002", customer_name: "Pooja Patel", invoice_amount: 12500.00, paid_amount: 12500.00, payment_date: "2026-08-02", payment_method: "Credit Card", status: "SUCCESS" },
  { transaction_id: "TXN-1003", invoice_id: "INV-2026-003", customer_name: "Rohan Mehta", invoice_amount: 7800.00, paid_amount: 7644.00, payment_date: "2026-08-02", payment_method: "Razorpay Cards", status: "SUCCESS" },
  { transaction_id: "TXN-1004", invoice_id: "INV-2026-004", customer_name: "Zomato Delivery Fleet", invoice_amount: 45000.00, paid_amount: 45000.00, payment_date: "2026-08-03", payment_method: "Netbanking", status: "SUCCESS" },
  { transaction_id: "TXN-1005", invoice_id: "INV-2026-005", customer_name: "Ananya Iyer", invoice_amount: 3200.00, paid_amount: 0.00, payment_date: "2026-08-03", payment_method: "None", status: "PENDING" },
  { transaction_id: "TXN-1006", invoice_id: "INV-2026-006", customer_name: "Vikramaditya Rao", invoice_amount: 18000.00, paid_amount: 18000.00, payment_date: "2026-08-04", payment_method: "Razorpay UPI", status: "SUCCESS" },
  { transaction_id: "TXN-1007", invoice_id: "INV-2026-007", customer_name: "Sneha Kulkarni", invoice_amount: 9500.00, paid_amount: 9000.00, payment_date: "2026-08-04", payment_method: "Bank Transfer", status: "SUCCESS" },
  { transaction_id: "TXN-1008", invoice_id: "INV-2026-008", customer_name: "Kiran Verma", invoice_amount: 15000.00, paid_amount: 15000.00, payment_date: "2026-08-05", payment_method: "Credit Card", status: "SUCCESS" },
  { transaction_id: "TXN-1009", invoice_id: "INV-2026-009", customer_name: "Freshworks India Ltd", invoice_amount: 62000.00, paid_amount: 60760.00, payment_date: "2026-08-05", payment_method: "Razorpay Gateway", status: "SUCCESS" },
  { transaction_id: "TXN-1010", invoice_id: "INV-2026-010", customer_name: "Deepak Joshi", invoice_amount: 4200.00, paid_amount: 4200.00, payment_date: "2026-08-06", payment_method: "Razorpay UPI", status: "SUCCESS" },
  { transaction_id: "TXN-1011", invoice_id: "INV-2026-011", customer_name: "Swiggy Cloud Kitchens", invoice_amount: 84000.00, paid_amount: 84000.00, payment_date: "2026-08-06", payment_method: "Netbanking", status: "SUCCESS" },
  { transaction_id: "TXN-1012", invoice_id: "INV-2026-012", customer_name: "Neha Reddy", invoice_amount: 24000.00, paid_amount: 0.00, payment_date: "2026-08-07", payment_method: "None", status: "FAILED" },
  { transaction_id: "TXN-1013", invoice_id: "INV-2026-013", customer_name: "Aditya Chopra", invoice_amount: 6500.00, paid_amount: 6500.00, payment_date: "2026-08-07", payment_method: "Debit Card", status: "SUCCESS" },
  { transaction_id: "TXN-1014", invoice_id: "INV-2026-014", customer_name: "Priyanka Sengupta", invoice_amount: 11200.00, paid_amount: 10500.00, payment_date: "2026-08-08", payment_method: "Bank Transfer", status: "SUCCESS" },
  { transaction_id: "TXN-1015", invoice_id: "INV-2026-015", customer_name: "Rahul Nair", invoice_amount: 8900.00, paid_amount: 8900.00, payment_date: "2026-08-08", payment_method: "Razorpay UPI", status: "SUCCESS" },
  { transaction_id: "TXN-1016", invoice_id: "INV-2026-016", customer_name: "Urban Company Services", invoice_amount: 53000.00, paid_amount: 53000.00, payment_date: "2026-08-09", payment_method: "Netbanking", status: "SUCCESS" },
  { transaction_id: "TXN-1017", invoice_id: "INV-2026-017", customer_name: "Meera Deshmukh", invoice_amount: 7500.00, paid_amount: 7500.00, payment_date: "2026-08-09", payment_method: "Razorpay UPI", status: "SUCCESS" },
  { transaction_id: "TXN-1018", invoice_id: "INV-2026-018", customer_name: "Kavita Krishnan", invoice_amount: 16400.00, paid_amount: 16072.00, payment_date: "2026-08-10", payment_method: "Razorpay Cards", status: "SUCCESS" },
  { transaction_id: "TXN-1019", invoice_id: "INV-2026-019", customer_name: "Amitabh Saxena", invoice_amount: 35000.00, paid_amount: 0.00, payment_date: "2026-08-10", payment_method: "None", status: "PENDING" },
  { transaction_id: "TXN-1020", invoice_id: "INV-2026-020", customer_name: "Harish Menon", invoice_amount: 9800.00, paid_amount: 9800.00, payment_date: "2026-08-11", payment_method: "Credit Card", status: "SUCCESS" },
  { transaction_id: "TXN-1021", invoice_id: "INV-2026-021", customer_name: "Blinkit Commerce Pvt", invoice_amount: 72000.00, paid_amount: 72000.00, payment_date: "2026-08-11", payment_method: "Netbanking", status: "SUCCESS" },
  { transaction_id: "TXN-1022", invoice_id: "INV-2026-022", customer_name: "Siddharth Malhotra", invoice_amount: 14500.00, paid_amount: 14000.00, payment_date: "2026-08-12", payment_method: "Razorpay UPI", status: "SUCCESS" },
  { transaction_id: "TXN-1023", invoice_id: "INV-2026-023", customer_name: "Tanvi Bansal", invoice_amount: 5600.00, paid_amount: 5600.00, payment_date: "2026-08-12", payment_method: "Debit Card", status: "SUCCESS" },
  { transaction_id: "TXN-1024", invoice_id: "INV-2026-024", customer_name: "Rajesh Khanna", invoice_amount: 28000.00, paid_amount: 28000.00, payment_date: "2026-08-13", payment_method: "Credit Card", status: "SUCCESS" },
  { transaction_id: "TXN-1025", invoice_id: "INV-2026-025", customer_name: "Divya Nambiar", invoice_amount: 8200.00, paid_amount: 0.00, payment_date: "2026-08-13", payment_method: "None", status: "PENDING" },
  { transaction_id: "TXN-1026", invoice_id: "INV-2026-026", customer_name: "Infosys Enterprise Unit", invoice_amount: 120000.00, paid_amount: 120000.00, payment_date: "2026-08-14", payment_method: "Netbanking", status: "SUCCESS" },
  { transaction_id: "TXN-1027", invoice_id: "INV-2026-027", customer_name: "Gaurav Bhattacharya", invoice_amount: 4900.00, paid_amount: 4900.00, payment_date: "2026-08-14", payment_method: "Razorpay UPI", status: "SUCCESS" },
  { transaction_id: "TXN-1028", invoice_id: "INV-2026-028", customer_name: "Payal Mukherjee", invoice_amount: 19500.00, paid_amount: 19110.00, payment_date: "2026-08-15", payment_method: "Razorpay Cards", status: "SUCCESS" },
  { transaction_id: "TXN-1029", invoice_id: "INV-2026-029", customer_name: "Nikhil Agarwal", invoice_amount: 6700.00, paid_amount: 6700.00, payment_date: "2026-08-15", payment_method: "Razorpay UPI", status: "SUCCESS" },
  { transaction_id: "TXN-1030", invoice_id: "INV-2026-030", customer_name: "Zepto Hyperlocal", invoice_amount: 96000.00, paid_amount: 96000.00, payment_date: "2026-08-16", payment_method: "Netbanking", status: "SUCCESS" },
  { transaction_id: "TXN-1010", invoice_id: "INV-2026-010", customer_name: "Deepak Joshi", invoice_amount: 4200.00, paid_amount: 4200.00, payment_date: "2026-08-06", payment_method: "Razorpay UPI", status: "SUCCESS" },
  { transaction_id: "TXN-1031", invoice_id: "INV-2026-031", customer_name: "Sunil Shetty", invoice_amount: 13500.00, paid_amount: 10000.00, payment_date: "2026-08-17", payment_method: "Bank Transfer", status: "SUCCESS" },
  { transaction_id: "TXN-1032", invoice_id: "INV-2026-032", customer_name: "Ritu Srivastava", invoice_amount: 3100.00, paid_amount: 3100.00, payment_date: "2026-08-17", payment_method: "Razorpay UPI", status: "SUCCESS" },
  { transaction_id: "TXN-1033", invoice_id: "INV-2026-033", customer_name: "Manish Kaushik", invoice_amount: 22000.00, paid_amount: 22000.00, payment_date: "2026-08-18", payment_method: "Credit Card", status: "SUCCESS" },
  { transaction_id: "TXN-1034", invoice_id: "INV-2026-034", customer_name: "Archana Dixit", invoice_amount: 17500.00, paid_amount: 0.00, payment_date: "2026-08-18", payment_method: "None", status: "PENDING" },
  { transaction_id: "TXN-1035", invoice_id: "INV-2026-035", customer_name: "Cred Club Solutions", invoice_amount: 150000.00, paid_amount: 150000.00, payment_date: "2026-08-19", payment_method: "Netbanking", status: "SUCCESS" },
  { transaction_id: "TXN-1036", invoice_id: "INV-2026-036", customer_name: "Arjun Kapoor", invoice_amount: 8800.00, paid_amount: 8800.00, payment_date: "2026-08-19", payment_method: "Razorpay UPI", status: "SUCCESS" },
  { transaction_id: "TXN-1037", invoice_id: "INV-2026-037", customer_name: "Shweta Tiwari", invoice_amount: 10500.00, paid_amount: 10290.00, payment_date: "2026-08-20", payment_method: "Razorpay Cards", status: "SUCCESS" },
  { transaction_id: "TXN-1038", invoice_id: "INV-2026-038", customer_name: "Vivek Oberoi", invoice_amount: 27000.00, paid_amount: 25000.00, payment_date: "2026-08-20", payment_method: "Bank Transfer", status: "SUCCESS" },
  { transaction_id: "TXN-1039", invoice_id: "INV-2026-039", customer_name: "Simran Kaur", invoice_amount: 6400.00, paid_amount: 6400.00, payment_date: "2026-08-21", payment_method: "Razorpay UPI", status: "SUCCESS" },
  { transaction_id: "TXN-1040", invoice_id: "INV-2026-040", customer_name: "Razorpay X Corp", invoice_amount: 210000.00, paid_amount: 210000.00, payment_date: "2026-08-21", payment_method: "Netbanking", status: "SUCCESS" },
  { transaction_id: "TXN-1020", invoice_id: "INV-2026-020", customer_name: "Harish Menon", invoice_amount: 9800.00, paid_amount: 9800.00, payment_date: "2026-08-11", payment_method: "Credit Card", status: "SUCCESS" },
  { transaction_id: "TXN-1041", invoice_id: "INV-2026-041", customer_name: "Kunal Shah", invoice_amount: 50000.00, paid_amount: 50000.00, payment_date: "2026-08-22", payment_method: "Netbanking", status: "PENDING" },
  { transaction_id: "TXN-1042", invoice_id: "INV-2026-042", customer_name: "Varun Dhawan", invoice_amount: 11800.00, paid_amount: 10000.00, payment_date: "2026-08-22", payment_method: "Razorpay UPI", status: "SUCCESS" },
  { transaction_id: "TXN-1043", invoice_id: "INV-2026-043", customer_name: "Kriti Sanon", invoice_amount: 9200.00, paid_amount: 9200.00, payment_date: "2026-08-23", payment_method: "Credit Card", status: "SUCCESS" },
  { transaction_id: "TXN-1044", invoice_id: "INV-2026-044", customer_name: "Alia Bhatt", invoice_amount: 33000.00, paid_amount: 0.00, payment_date: "2026-08-23", payment_method: "None", status: "FAILED" },
  { transaction_id: "TXN-1045", invoice_id: "INV-2026-045", customer_name: "PhonePe Merchant Hub", invoice_amount: 185000.00, paid_amount: 185000.00, payment_date: "2026-08-24", payment_method: "Netbanking", status: "SUCCESS" }
];

// App Global State
let currentDataset = [];
let currentMetrics = {};
let currentHealth = {};
let activeDatasetName = "Sample Demo Dataset (45 transactions)";

// INR Currency Formatter
function formatINR(amount) {
  if (amount === null || amount === undefined || isNaN(amount)) return "₹0.00";
  const isNegative = amount < 0;
  const absAmount = Math.abs(amount);
  const parts = absAmount.toFixed(2).split(".");
  let intPart = parts[0];
  const decPart = parts[1];

  let formattedInt = "";
  if (intPart.length <= 3) {
    formattedInt = intPart;
  } else {
    const lastThree = intPart.substring(intPart.length - 3);
    const remaining = intPart.substring(0, intPart.length - 3);
    const groups = [];
    let rem = remaining;
    while (rem.length > 2) {
      groups.unshift(rem.substring(rem.length - 2));
      rem = rem.substring(0, rem.length - 2);
    }
    if (rem.length > 0) groups.unshift(rem);
    groups.push(lastThree);
    formattedInt = groups.join(",");
  }
  return `${isNegative ? "-" : ""}₹${formattedInt}.${decPart}`;
}

// Deterministic Multi-Rule Reconciliation Engine
function reconcileTransactions(rawRecords) {
  const records = JSON.parse(JSON.stringify(rawRecords));
  
  // Track duplicates
  const txnCounts = {};
  const invPaidCounts = {};

  records.forEach(r => {
    const txnId = (r.transaction_id || "").trim();
    const invId = (r.invoice_id || "").trim();
    const paid = parseFloat(r.paid_amount || 0);

    if (txnId && txnId !== "N/A") {
      txnCounts[txnId] = (txnCounts[txnId] || 0) + 1;
    }
    if (paid > 0 && invId) {
      invPaidCounts[invId] = (invPaidCounts[invId] || 0) + 1;
    }
  });

  records.forEach((r, idx) => {
    const invAmt = parseFloat(r.invoice_amount || 0);
    const paidAmt = parseFloat(r.paid_amount || 0);
    const diff = Math.round((invAmt - paidAmt) * 100) / 100;
    const varPct = invAmt > 0 ? Math.round((diff / invAmt) * 10000) / 100 : 0.0;
    const rawStatus = (r.status || "").toUpperCase();
    const txnId = (r.transaction_id || "").trim();
    const invId = (r.invoice_id || "").trim();

    r.invoice_amount = invAmt;
    r.paid_amount = paidAmt;
    r.difference = diff;
    r.variance_pct = varPct;

    const isDup = (txnCounts[txnId] > 1) || (paidAmt > 0 && invPaidCounts[invId] > 1);

    if (isDup) {
      r.reconciliation_status = "DUPLICATE";
      r.ai_reason = `Duplicate record detected for Transaction ID ${txnId}. Multiple identical charges or settlement logs recorded.`;
      r.recommended_action = "Flag for audit. Check bank gateway settlement logs and initiate refund if double-charged.";
      r.risk_level = paidAmt > 10000 ? "High Risk" : "Medium Risk";
    } else if (paidAmt === 0 || ["FAILED", "UNPAID", "CANCELLED"].includes(rawStatus)) {
      r.reconciliation_status = "MISSING PAYMENT";
      r.ai_reason = `No payment received for invoice ${invId} (Uncollected amount: ${formatINR(invAmt)}).`;
      r.recommended_action = "Trigger automated payment reminder email/SMS to customer with direct payment link.";
      r.risk_level = invAmt > 15000 ? "High Risk" : "Medium Risk";
    } else if (["PENDING", "PROCESSING", "INITIATED", "ON_HOLD", "IN_TRANSIT"].includes(rawStatus)) {
      r.reconciliation_status = "PENDING";
      r.ai_reason = `Payment of ${formatINR(paidAmt)} is currently in gateway processing / bank settlement transit.`;
      r.recommended_action = "Monitor gateway webhook. Allow T+2 settlement window before escalating.";
      r.risk_level = "Low Risk";
    } else if (Math.abs(diff) < 0.01) {
      r.reconciliation_status = "MATCHED";
      r.ai_reason = "Invoice amount matches received settlement perfectly (100% Match).";
      r.recommended_action = "Reconciled successfully. Auto-archive to general ledger.";
      r.risk_level = "Resolved / None";
    } else {
      r.reconciliation_status = "MISMATCH";
      if (varPct >= 1.7 && varPct <= 2.5) {
        r.ai_reason = `Discrepancy of ${formatINR(diff)} (${varPct}%). Matches standard 2% Razorpay Payment Gateway MDR transaction fee.`;
        r.recommended_action = "Post variance to 'Payment Gateway Fees & Processing Expenses' ledger account.";
        r.risk_level = "Low Risk";
      } else if (varPct >= 17.0 && varPct <= 19.0) {
        r.ai_reason = `Discrepancy of ${formatINR(diff)} (${varPct}%). Matches standard 18% GST tax deduction.`;
        r.recommended_action = "Verify customer TDS/GST certificate and reconcile against tax credit ledger.";
        r.risk_level = "Medium Risk";
      } else if (diff > 0) {
        r.ai_reason = `Short payment of ${formatINR(diff)} detected against total invoice of ${formatINR(invAmt)}.`;
        r.recommended_action = `Generate partial payment receipt and request remaining balance of ${formatINR(diff)}.`;
        r.risk_level = diff > 5000 ? "High Risk" : "Medium Risk";
      } else {
        r.ai_reason = `Overpayment of ${formatINR(Math.abs(diff))} received (Total paid: ${formatINR(paidAmt)} vs Invoiced: ${formatINR(invAmt)}).`;
        r.recommended_action = "Credit balance to customer advance wallet or issue surplus refund.";
        r.risk_level = "Low Risk";
      }
    }
  });

  // Calculate Metrics
  const totalTxns = records.length;
  let totalInvoiced = 0;
  let totalPaid = 0;
  let matchedCount = 0;
  let matchedAmount = 0;
  let mismatchCount = 0;
  let mismatchDiff = 0;
  let missingCount = 0;
  let missingAmount = 0;
  let duplicateCount = 0;
  let duplicateAmount = 0;
  let pendingCount = 0;

  records.forEach(r => {
    totalInvoiced += r.invoice_amount;
    totalPaid += r.paid_amount;

    if (r.reconciliation_status === "MATCHED") {
      matchedCount++;
      matchedAmount += r.paid_amount;
    } else if (r.reconciliation_status === "MISMATCH") {
      mismatchCount++;
      mismatchDiff += Math.abs(r.difference);
    } else if (r.reconciliation_status === "MISSING PAYMENT") {
      missingCount++;
      missingAmount += r.invoice_amount;
    } else if (r.reconciliation_status === "DUPLICATE") {
      duplicateCount++;
      duplicateAmount += r.paid_amount;
    } else if (r.reconciliation_status === "PENDING") {
      pendingCount++;
    }
  });

  const reconciliationRate = totalTxns > 0 ? (matchedCount / totalTxns) * 100 : 0;
  const totalMismatchAmount = missingAmount + mismatchDiff;

  const metrics = {
    total_transactions: totalTxns,
    total_invoiced_amount: totalInvoiced,
    total_paid_amount: totalPaid,
    matched_count: matchedCount,
    matched_amount: matchedAmount,
    mismatch_count: mismatchCount,
    mismatch_diff: mismatchDiff,
    missing_count: missingCount,
    missing_amount: missingAmount,
    duplicate_count: duplicateCount,
    duplicate_amount: duplicateAmount,
    pending_count: pendingCount,
    reconciliation_rate: reconciliationRate,
    total_mismatch_amount: totalMismatchAmount
  };

  let healthStatus = "Excellent";
  let healthColor = "#10B981";
  let healthDesc = "Your financial ledger is exceptionally healthy. Most settlements match invoiced amounts seamlessly.";

  if (reconciliationRate < 70) {
    healthStatus = "Critical Audit Required";
    healthColor = "#EF4444";
    healthDesc = "High discrepancy rate detected. Significant capital is stuck in missing invoices or unverified duplicate charges.";
  } else if (reconciliationRate < 90) {
    healthStatus = "Moderate Attention Needed";
    healthColor = "#F59E0B";
    healthDesc = "Moderate variance detected. Several payments have uncollected balances or gateway fee deductions requiring ledger posting.";
  }

  const health = {
    health_status: healthStatus,
    health_color: healthColor,
    health_message: healthDesc,
    risk_amount_formatted: formatINR(totalMismatchAmount)
  };

  return { transactions: records, metrics, health };
}

// Generate Customer Outreach Email
function generateCustomerEmail(r) {
  const customer = r.customer_name || "Customer";
  const invId = r.invoice_id || "N/A";
  const invAmt = formatINR(r.invoice_amount || 0);
  const paidAmt = formatINR(r.paid_amount || 0);
  const diffAmt = formatINR(r.difference || 0);

  if (r.reconciliation_status === "MISSING PAYMENT") {
    return `Subject: Friendly Reminder: Outstanding Invoice ${invId} Payment

Dear ${customer},

We hope you are doing well.

Our automated finance controller indicates that Invoice ${invId} for ${invAmt} remains unpaid.

To ensure uninterrupted services, please complete the payment at your earliest convenience using our instant Razorpay link:
👉 https://rzp.io/l/demo-${invId}

If you have already initiated the transfer, please reply with the payment reference ID so we can reconcile your account immediately.

Warm regards,
Finance Operations Team
PayMatch AI Controller`;
  } else if (r.reconciliation_status === "MISMATCH" && r.difference > 0) {
    return `Subject: Update on Invoice ${invId}: Balance of ${diffAmt} Remaining

Dear ${customer},

Thank you for your recent payment of ${paidAmt} towards Invoice ${invId} (Total: ${invAmt}).

Our records show a remaining balance of ${diffAmt}. Please verify if this was an installment payment or if any deduction was applied.

You can clear the outstanding balance here:
👉 https://rzp.io/l/demo-bal-${invId}

Thank you for your partnership.

Warm regards,
Finance Operations Team
PayMatch AI Controller`;
  } else if (r.reconciliation_status === "DUPLICATE") {
    return `Subject: Notice: Duplicate Charge Detected for Invoice ${invId}

Dear ${customer},

Our automated finance controller detected a possible duplicate transaction for Invoice ${invId}.

We are currently verifying the bank settlement. If a double-charge occurred, a full refund of the duplicate amount will be processed back to your original payment method within 3-5 business days.

No action is required from your end. We apologize for any inconvenience.

Warm regards,
Finance Operations Team
PayMatch AI Controller`;
  } else {
    return `Subject: Receipt & Confirmation for Invoice ${invId}

Dear ${customer},

Thank you for your payment of ${paidAmt} for Invoice ${invId}.
Your transaction has been successfully reconciled.

Warm regards,
Finance Operations Team
PayMatch AI Controller`;
  }
}

// Generate Executive Report Markdown
function generateExecutiveReport(metrics, transactions) {
  const nowStr = new Date().toLocaleString("en-IN", { dateStyle: "long", timeStyle: "short" });
  const flagged = transactions.filter(t => t.reconciliation_status !== "MATCHED").slice(0, 5);

  let md = `# 📑 PayMatch AI — Executive Finance Reconciliation Report
**Generated On:** ${nowStr}
**Reconciliation Status:** Audit Completed

---

## 1. Key Performance Indicators (KPIs)
* **Total Transactions Processed:** ${metrics.total_transactions}
* **Total Invoiced Value:** ${formatINR(metrics.total_invoiced_amount)}
* **Total Received Amount:** ${formatINR(metrics.total_paid_amount)}
* **Overall Reconciliation Rate:** ${metrics.reconciliation_rate.toFixed(1)}%
* **Total Financial Risk / Discrepancy:** ${formatINR(metrics.total_mismatch_amount)}

---

## 2. Reconciliation Status Breakdown
* **✅ Perfectly Matched:** ${metrics.matched_count} transactions (${formatINR(metrics.matched_amount)})
* **⚠️ Amount Mismatches:** ${metrics.mismatch_count} transactions (${formatINR(metrics.mismatch_diff)} variance)
* **❌ Missing Payments:** ${metrics.missing_count} transactions (${formatINR(metrics.missing_amount)} uncollected)
* **🔄 Duplicate Transactions:** ${metrics.duplicate_count} transactions
* **⏳ Pending Settlements:** ${metrics.pending_count} transactions

---

## 3. High-Priority Action Items
`;

  flagged.forEach(item => {
    md += `### [${item.reconciliation_status}] ${item.invoice_id} - ${item.customer_name}
* **Transaction ID:** \`${item.transaction_id}\`
* **Invoiced:** ${formatINR(item.invoice_amount)} | **Paid:** ${formatINR(item.paid_amount)} | **Variance:** ${formatINR(item.difference)}
* **AI Root Cause:** ${item.ai_reason}
* **Recommended Next Action:** ${item.recommended_action}

`;
  });

  md += `---
*Report generated automatically by PayMatch AI Finance Controller (Track 4 - Razorpay Hackathon)*`;
  return md;
}

// UI Render Functions
function updateUI() {
  document.getElementById("active-dataset-name").textContent = activeDatasetName;

  // Health Card
  const healthCard = document.getElementById("health-card");
  healthCard.style.borderLeftColor = currentHealth.health_color;
  document.getElementById("health-status-title").textContent = currentHealth.health_status;
  document.getElementById("health-status-desc").textContent = currentHealth.health_message;
  document.getElementById("total-risk-val").textContent = currentHealth.risk_amount_formatted;

  // Primary KPIs
  document.getElementById("kpi-total-txns").textContent = currentMetrics.total_transactions;
  document.getElementById("kpi-total-invoiced").textContent = formatINR(currentMetrics.total_invoiced_amount);
  document.getElementById("kpi-total-settled").textContent = formatINR(currentMetrics.total_paid_amount);
  
  const recRateEl = document.getElementById("kpi-reconciliation-rate");
  recRateEl.textContent = `${currentMetrics.reconciliation_rate.toFixed(1)}%`;
  recRateEl.className = `kpi-value ${currentMetrics.reconciliation_rate >= 80 ? "text-green" : currentMetrics.reconciliation_rate >= 60 ? "text-amber" : "text-red"}`;

  // Mini Status KPIs
  document.getElementById("kpi-matched-count").textContent = currentMetrics.matched_count;
  document.getElementById("kpi-matched-amt").textContent = formatINR(currentMetrics.matched_amount);
  document.getElementById("kpi-mismatch-count").textContent = currentMetrics.mismatch_count;
  document.getElementById("kpi-mismatch-diff").textContent = `Diff: ${formatINR(currentMetrics.mismatch_diff)}`;
  document.getElementById("kpi-missing-count").textContent = currentMetrics.missing_count;
  document.getElementById("kpi-missing-amt").textContent = `Unpaid: ${formatINR(currentMetrics.missing_amount)}`;
  document.getElementById("kpi-duplicate-count").textContent = currentMetrics.duplicate_count;

  renderCharts();
  renderPriorityQueue();
  populateChannelFilter();
  renderTable();
  populateInspector();
  renderAnalytics();
  renderReportPreview();
}

// Plotly Charts Rendering
function renderCharts() {
  // 1. Donut Status Chart
  const statusLabels = ["Matched", "Mismatch", "Missing Payment", "Duplicate", "Pending"];
  const statusValues = [
    currentMetrics.matched_count,
    currentMetrics.mismatch_count,
    currentMetrics.missing_count,
    currentMetrics.duplicate_count,
    currentMetrics.pending_count
  ];
  const statusColors = ["#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#3B82F6"];

  const donutData = [{
    labels: statusLabels.filter((_, i) => statusValues[i] > 0),
    values: statusValues.filter(v => v > 0),
    type: "pie",
    hole: 0.62,
    marker: { colors: statusColors.filter((_, i) => statusValues[i] > 0) },
    textinfo: "percent+label",
    textposition: "outside",
    hoverinfo: "label+value+percent"
  }];

  const donutLayout = {
    title: { text: "<b>Reconciliation Status Distribution</b>", font: { size: 14, color: "#0F172A" }, x: 0.05 },
    annotations: [{
      text: `<b>${currentMetrics.reconciliation_rate.toFixed(1)}%</b><br><span style="font-size:11px;color:#64748B;">Matched</span>`,
      x: 0.5, y: 0.5, font: { size: 18, color: "#0F172A" }, showarrow: false
    }],
    showlegend: true,
    legend: { orientation: "h", y: -0.2, x: 0.5, xanchor: "center" },
    margin: { t: 40, b: 40, l: 20, r: 20 },
    height: 330,
    paper_bgcolor: "rgba(0,0,0,0)"
  };

  Plotly.newPlot("chart-status-donut", donutData, donutLayout, { responsive: true, displayModeBar: false });

  // 2. Channel Performance Bar Chart
  const channels = {};
  currentDataset.forEach(r => {
    const ch = r.payment_method || "Unknown";
    if (!channels[ch]) channels[ch] = { MATCHED: 0, MISMATCH: 0, "MISSING PAYMENT": 0, DUPLICATE: 0, PENDING: 0 };
    channels[ch][r.reconciliation_status] = (channels[ch][r.reconciliation_status] || 0) + 1;
  });

  const chNames = Object.keys(channels);
  const barData = [
    { x: chNames, y: chNames.map(c => channels[c].MATCHED), name: "Matched", type: "bar", marker: { color: "#10B981" } },
    { x: chNames, y: chNames.map(c => channels[c].MISMATCH), name: "Mismatch", type: "bar", marker: { color: "#F59E0B" } },
    { x: chNames, y: chNames.map(c => channels[c]["MISSING PAYMENT"]), name: "Missing", type: "bar", marker: { color: "#EF4444" } },
    { x: chNames, y: chNames.map(c => channels[c].DUPLICATE), name: "Duplicate", type: "bar", marker: { color: "#8B5CF6" } },
    { x: chNames, y: chNames.map(c => channels[c].PENDING), name: "Pending", type: "bar", marker: { color: "#3B82F6" } }
  ];

  const barLayout = {
    title: { text: "<b>Payment Channel Performance & Discrepancies</b>", font: { size: 14, color: "#0F172A" }, x: 0.05 },
    barmode: "stack",
    legend: { orientation: "h", y: -0.25, x: 0.5, xanchor: "center" },
    margin: { t: 40, b: 40, l: 30, r: 20 },
    height: 330,
    paper_bgcolor: "rgba(0,0,0,0)",
    yaxis: { gridcolor: "#F1F5F9" }
  };

  Plotly.newPlot("chart-channel-bar", barData, barLayout, { responsive: true, displayModeBar: false });
}

// Priority Queue List
function renderPriorityQueue() {
  const container = document.getElementById("priority-items-container");
  container.innerHTML = "";

  const flagged = currentDataset
    .filter(r => r.reconciliation_status !== "MATCHED")
    .sort((a, b) => Math.abs(b.difference) - Math.abs(a.difference))
    .slice(0, 4);

  if (flagged.length === 0) {
    container.innerHTML = `<div style="color:#10B981;padding:12px;font-weight:600;"><i class="fa-solid fa-circle-check"></i> All transactions are 100% matched! Zero risk items detected.</div>`;
    return;
  }

  flagged.forEach(item => {
    const el = document.createElement("div");
    el.className = "priority-item";
    const statusBadge = `<span class="badge-${item.reconciliation_status === "MISMATCH" ? "mismatch" : item.reconciliation_status === "DUPLICATE" ? "duplicate" : "missing"}">${item.reconciliation_status}</span>`;
    
    el.innerHTML = `
      <div class="priority-summary">
        <span>[${item.risk_level}] <b>${item.invoice_id}</b> — ${item.customer_name} | Variance: <b>${formatINR(item.difference)}</b></span>
        ${statusBadge}
      </div>
      <div class="priority-body">
        <p><b>🤖 AI Root Cause:</b> ${item.ai_reason}</p>
        <p style="margin-top:4px;"><b>💡 Action:</b> ${item.recommended_action}</p>
        <div style="margin-top:10px;">
          <small><b>✉️ 1-Click Resolution Outreach Template:</b></small>
          <pre style="background:#F8FAFC;padding:10px;border-radius:6px;font-size:11px;margin-top:4px;white-space:pre-wrap;border:1px solid #E2E8F0;">${generateCustomerEmail(item)}</pre>
        </div>
      </div>
    `;
    container.appendChild(el);
  });
}

// Populate Channels Dropdown
function populateChannelFilter() {
  const select = document.getElementById("filter-channel-select");
  const currentVal = select.value;
  select.innerHTML = `<option value="ALL">ALL Channels</option>`;

  const channels = Array.from(new Set(currentDataset.map(r => r.payment_method).filter(Boolean))).sort();
  channels.forEach(ch => {
    const opt = document.createElement("option");
    opt.value = ch;
    opt.textContent = ch;
    select.appendChild(opt);
  });

  if (channels.includes(currentVal)) select.value = currentVal;
}

// Render Transactions Table
function renderTable() {
  const statusFilter = document.getElementById("filter-status-select").value;
  const channelFilter = document.getElementById("filter-channel-select").value;
  const searchTerm = (document.getElementById("search-txns-input").value || "").toLowerCase().trim();

  let filtered = currentDataset.filter(r => {
    if (statusFilter !== "ALL" && r.reconciliation_status !== statusFilter) return false;
    if (channelFilter !== "ALL" && r.payment_method !== channelFilter) return false;
    if (searchTerm) {
      const matchTxn = (r.transaction_id || "").toLowerCase().includes(searchTerm);
      const matchInv = (r.invoice_id || "").toLowerCase().includes(searchTerm);
      const matchCust = (r.customer_name || "").toLowerCase().includes(searchTerm);
      if (!matchTxn && !matchInv && !matchCust) return false;
    }
    return true;
  });

  document.getElementById("table-record-count").textContent = `Showing ${filtered.length} of ${currentDataset.length} transactions`;

  const tbody = document.getElementById("transactions-table-body");
  tbody.innerHTML = "";

  filtered.forEach(r => {
    const tr = document.createElement("tr");
    let badgeClass = "badge-matched";
    if (r.reconciliation_status === "MISMATCH") badgeClass = "badge-mismatch";
    else if (r.reconciliation_status === "MISSING PAYMENT") badgeClass = "badge-missing";
    else if (r.reconciliation_status === "DUPLICATE") badgeClass = "badge-duplicate";
    else if (r.reconciliation_status === "PENDING") badgeClass = "badge-pending";

    tr.innerHTML = `
      <td><code>${r.transaction_id || "N/A"}</code></td>
      <td><code>${r.invoice_id || "N/A"}</code></td>
      <td><b>${r.customer_name || "N/A"}</b></td>
      <td>${formatINR(r.invoice_amount)}</td>
      <td>${formatINR(r.paid_amount)}</td>
      <td style="font-weight:600;color:${r.difference > 0 ? '#EF4444' : '#10B981'}">${formatINR(r.difference)}</td>
      <td><span class="${badgeClass}">${r.reconciliation_status}</span></td>
      <td><small>${r.risk_level}</small></td>
      <td>${r.payment_method || "N/A"}</td>
      <td>${r.payment_date || "N/A"}</td>
      <td style="max-width:240px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="${r.recommended_action}">${r.recommended_action}</td>
    `;
    tbody.appendChild(tr);
  });
}

// Single Transaction Inspector Dropdown
function populateInspector() {
  const select = document.getElementById("inspector-txn-select");
  select.innerHTML = "";

  currentDataset.forEach(r => {
    const opt = document.createElement("option");
    opt.value = r.transaction_id;
    opt.textContent = `${r.transaction_id} — ${r.customer_name} (${r.invoice_id}) [${r.reconciliation_status}]`;
    select.appendChild(opt);
  });

  if (currentDataset.length > 0) {
    inspectTransaction(currentDataset[0].transaction_id);
  }
}

function inspectTransaction(txnId) {
  const item = currentDataset.find(r => r.transaction_id === txnId);
  const container = document.getElementById("inspector-details-box");
  if (!item) {
    container.innerHTML = `<p class="text-muted">Select a transaction above to inspect details.</p>`;
    return;
  }

  container.innerHTML = `
    <h4 style="margin-bottom:8px;">🔍 Discrepancy Breakdown for <code>${item.transaction_id}</code></h4>
    <p><b>Customer:</b> ${item.customer_name} (Invoice: <code>${item.invoice_id}</code>) | <b>Payment Channel:</b> ${item.payment_method} | <b>Status:</b> ${item.reconciliation_status}</p>
    <p><b>Invoiced:</b> ${formatINR(item.invoice_amount)} | <b>Paid:</b> ${formatINR(item.paid_amount)} | <b>Variance:</b> <span style="color:#EF4444;font-weight:700;">${formatINR(item.difference)}</span></p>
    <p style="margin-top:8px;"><b>🤖 Root Cause Analysis:</b> ${item.ai_reason}</p>
    <p style="margin-top:4px;"><b>💡 Controller Recommended Action:</b> ${item.recommended_action}</p>
    <div style="margin-top:12px;">
      <b>✉️ Generated Merchant Recovery / Confirmation Email:</b>
      <pre style="background:#FFFFFF;padding:12px;border-radius:6px;border:1px solid #E2E8F0;font-size:12px;margin-top:6px;white-space:pre-wrap;">${generateCustomerEmail(item)}</pre>
    </div>
  `;
}

// Render Analytics Tab
function renderAnalytics() {
  // 1. Timeline Chart
  const daily = {};
  currentDataset.forEach(r => {
    const date = r.payment_date || "2026-08-01";
    if (!daily[date]) daily[date] = { invoiced: 0, paid: 0 };
    daily[date].invoiced += r.invoice_amount;
    daily[date].paid += r.paid_amount;
  });

  const dates = Object.keys(daily).sort();
  const timelineData = [
    { x: dates, y: dates.map(d => daily[d].invoiced), name: "Invoiced Amount", type: "scatter", mode: "lines+markers", line: { color: "#3B82F6", width: 3 } },
    { x: dates, y: dates.map(d => daily[d].paid), name: "Settled Amount", type: "scatter", mode: "lines+markers", line: { color: "#10B981", width: 3, dash: "dot" } }
  ];

  const timelineLayout = {
    title: { text: "<b>Daily Settlement vs Billed Timeline</b>", font: { size: 14, color: "#0F172A" }, x: 0.05 },
    legend: { orientation: "h", y: -0.25, x: 0.5, xanchor: "center" },
    margin: { t: 40, b: 40, l: 40, r: 20 },
    height: 330,
    paper_bgcolor: "rgba(0,0,0,0)",
    yaxis: { gridcolor: "#F1F5F9" }
  };

  Plotly.newPlot("chart-timeline", timelineData, timelineLayout, { responsive: true, displayModeBar: false });

  // 2. Customer Variance Bar Chart
  const custVar = {};
  currentDataset.filter(r => r.reconciliation_status !== "MATCHED").forEach(r => {
    custVar[r.customer_name] = (custVar[r.customer_name] || 0) + Math.abs(r.difference);
  });

  const sortedCusts = Object.entries(custVar).sort((a, b) => b[1] - a[1]).slice(0, 8);
  const custBarData = [{
    x: sortedCusts.map(c => c[1]),
    y: sortedCusts.map(c => c[0]),
    type: "bar",
    orientation: "h",
    marker: { color: "#EF4444" }
  }];

  const custBarLayout = {
    title: { text: "<b>Top Variance Exposure by Customer (₹)</b>", font: { size: 14, color: "#0F172A" }, x: 0.05 },
    margin: { t: 40, b: 30, l: 140, r: 20 },
    height: 330,
    paper_bgcolor: "rgba(0,0,0,0)",
    xaxis: { gridcolor: "#F1F5F9" }
  };

  Plotly.newPlot("chart-customer-variance", custBarData, custBarLayout, { responsive: true, displayModeBar: false });

  // Root Cause Distribution Table
  const statusCounts = {};
  currentDataset.forEach(r => {
    statusCounts[r.reconciliation_status] = (statusCounts[r.reconciliation_status] || 0) + 1;
  });

  const tbody = document.getElementById("root-cause-table-body");
  tbody.innerHTML = "";
  Object.entries(statusCounts).forEach(([status, count]) => {
    const pct = ((count / currentDataset.length) * 100).toFixed(1);
    const tr = document.createElement("tr");
    tr.innerHTML = `<td><b>${status}</b></td><td>${count}</td><td>${pct}%</td>`;
    tbody.appendChild(tr);
  });
}

// Live Preview in Export Tab
function renderReportPreview() {
  const container = document.getElementById("report-preview-content");
  container.textContent = generateExecutiveReport(currentMetrics, currentDataset);
}

// CSV Ingestion Parser
function parseCSV(text) {
  const lines = text.trim().split("\n");
  if (lines.length < 2) return [];
  const headers = lines[0].split(",").map(h => h.trim().toLowerCase().replace(/[\r"]/g, ""));

  const results = [];
  for (let i = 1; i < lines.length; i++) {
    const row = lines[i].split(",").map(c => c.trim().replace(/[\r"]/g, ""));
    if (row.length === 0 || !row[0]) continue;
    const obj = {};
    headers.forEach((h, idx) => {
      obj[h] = row[idx] || "";
    });

    // Map common aliases
    const txnId = obj.transaction_id || obj.txn_id || obj.id || `TXN-AUTO-${i + 1000}`;
    const invId = obj.invoice_id || obj.inv_id || `INV-${i + 100}`;
    const cust = obj.customer_name || obj.customer || "Valued Customer";
    const invAmt = parseFloat(String(obj.invoice_amount || obj.amount || "0").replace(/[₹$,\s]/g, "")) || 0;
    const paidAmt = parseFloat(String(obj.paid_amount || obj.paid || "0").replace(/[₹$,\s]/g, "")) || 0;
    const pDate = obj.payment_date || obj.date || new Date().toISOString().split("T")[0];
    const pMethod = obj.payment_method || obj.method || "Gateway Settlement";
    const stat = obj.status || "SUCCESS";

    results.push({
      transaction_id: txnId,
      invoice_id: invId,
      customer_name: cust,
      invoice_amount: invAmt,
      paid_amount: paidAmt,
      payment_date: pDate,
      payment_method: pMethod,
      status: stat
    });
  }
  return results;
}

// Chat Assistant Handler
function handleChatQuery(query) {
  const container = document.getElementById("chat-messages-container");

  // User Bubble
  const userMsg = document.createElement("div");
  userMsg.className = "chat-message user";
  userMsg.innerHTML = `<div class="chat-avatar"><i class="fa-solid fa-user"></i></div><div class="chat-bubble">${query}</div>`;
  container.appendChild(userMsg);

  // Assistant Response Logic (Offline Fallback Guarantee)
  const q = query.toLowerCase();
  let answer = "";

  if (q.includes("risk") || q.includes("highest") || q.includes("biggest")) {
    const topItem = currentDataset.filter(r => r.reconciliation_status !== "MATCHED").sort((a,b) => b.invoice_amount - a.invoice_amount)[0];
    if (topItem) {
      answer = `🤖 **AI Finance Controller Insight:**\nThe highest single exposure in your ledger is **${topItem.invoice_id}** for customer **${topItem.customer_name}**.\n* **Invoiced Amount:** ${formatINR(topItem.invoice_amount)}\n* **Paid Amount:** ${formatINR(topItem.paid_amount)}\n* **Discrepancy:** ${formatINR(topItem.difference)}\n* **Status:** \`${topItem.reconciliation_status}\`\n* **Recommended Next Step:** ${topItem.recommended_action}`;
    } else {
      answer = `🤖 **AI Finance Controller:** All transactions are 100% matched! Zero risk items detected.`;
    }
  } else if (q.includes("missing") || q.includes("unpaid")) {
    const missing = currentDataset.filter(r => r.reconciliation_status === "MISSING PAYMENT");
    const totalMissing = missing.reduce((sum, r) => sum + r.invoice_amount, 0);
    answer = `🤖 **Missing Payments Audit:**\nWe found **${missing.length} missing payments** totaling **${formatINR(totalMissing)}** in outstanding uncollected revenue.\nTop unpaid customers: ${missing.slice(0, 4).map(m => m.customer_name).join(", ")}.\n👉 **Recommended Action:** Trigger automated batch payment reminder emails with direct Razorpay payment links.`;
  } else if (q.includes("duplicate") || q.includes("double")) {
    const dups = currentDataset.filter(r => r.reconciliation_status === "DUPLICATE");
    answer = `🤖 **Duplicate Detection Analysis:**\nIdentified **${dups.length} duplicate records**. Multiple charges or settlement logs were captured for identical transaction/invoice IDs.\n👉 **Recommended Action:** Cross-reference transaction IDs with bank gateway settlement logs and initiate automated customer refunds before chargeback dispute fees occur.`;
  } else if (q.includes("fee") || q.includes("mdr") || q.includes("razorpay") || q.includes("tax")) {
    answer = `🤖 **Payment Gateway & MDR Fee Diagnosis:**\nPayMatch AI automatically detected that several discrepancies correspond to standard **~2.0% Razorpay payment gateway MDR fees** and **18% GST withholdings**.\n* Rather than chasing customers for these small variances, these amounts should be auto-classified into your **'Payment Gateway Fees & Processing Expenses'** ledger.`;
  } else {
    answer = `🤖 **AI Finance Controller Assistant:**\nBased on our audit of **${currentMetrics.total_transactions} transactions**:\n* **Reconciliation Rate:** ${currentMetrics.reconciliation_rate.toFixed(1)}%\n* **Identified Discrepancies:** ${currentMetrics.mismatch_count} Mismatches, ${currentMetrics.missing_count} Missing Payments, ${currentMetrics.duplicate_count} Duplicates.\n* **Total Risk Exposure:** ${formatINR(currentMetrics.total_mismatch_amount)}\n\nYou can ask:\n- *"What is our biggest financial risk?"*\n- *"Show me missing payments"*\n- *"Explain duplicate transactions"*\n- *"How should we handle Razorpay MDR fees?"*`;
  }

  const botMsg = document.createElement("div");
  botMsg.className = "chat-message assistant";
  botMsg.innerHTML = `<div class="chat-avatar"><i class="fa-solid fa-robot"></i></div><div class="chat-bubble">${answer}</div>`;
  container.appendChild(botMsg);
  container.scrollTop = container.scrollHeight;
}

// Initialize Application
function initApp() {
  const result = reconcileTransactions(DEFAULT_DEMO_DATA);
  currentDataset = result.transactions;
  currentMetrics = result.metrics;
  currentHealth = result.health;
  updateUI();

  // Tab Navigation
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      const targetId = btn.getAttribute("data-tab");
      document.getElementById(targetId).classList.add("active");
      if (targetId === "tab-dashboard" || targetId === "tab-insights") {
        setTimeout(renderCharts, 50);
      }
    });
  });

  // Source Radio Switching
  document.querySelectorAll(".radio-label").forEach(label => {
    label.addEventListener("click", () => {
      document.querySelectorAll(".radio-label").forEach(l => l.classList.remove("active"));
      label.classList.add("active");
      const mode = label.getAttribute("data-mode");

      document.getElementById("single-upload-box").classList.toggle("hidden", mode !== "single");
      document.getElementById("dual-upload-box").classList.toggle("hidden", mode !== "dual");
      document.getElementById("demo-action-box").classList.toggle("hidden", mode !== "demo");

      if (mode === "demo") {
        activeDatasetName = "Sample Demo Dataset (45 transactions)";
        const res = reconcileTransactions(DEFAULT_DEMO_DATA);
        currentDataset = res.transactions;
        currentMetrics = res.metrics;
        currentHealth = res.health;
        updateUI();
      }
    });
  });

  // Reload Demo Button
  document.getElementById("btn-reload-demo").addEventListener("click", () => {
    activeDatasetName = "Sample Demo Dataset (45 transactions)";
    const res = reconcileTransactions(DEFAULT_DEMO_DATA);
    currentDataset = res.transactions;
    currentMetrics = res.metrics;
    currentHealth = res.health;
    updateUI();
  });

  // CSV Single File Upload
  document.getElementById("csv-file-input").addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (evt) => {
      const records = parseCSV(evt.target.result);
      if (records.length > 0) {
        activeDatasetName = file.name;
        const res = reconcileTransactions(records);
        currentDataset = res.transactions;
        currentMetrics = res.metrics;
        currentHealth = res.health;
        updateUI();
      } else {
        alert("Unable to parse CSV. Please check the expected column headers.");
      }
    };
    reader.readAsText(file);
  });

  // Filter and Search Events
  document.getElementById("filter-status-select").addEventListener("change", renderTable);
  document.getElementById("filter-channel-select").addEventListener("change", renderTable);
  document.getElementById("search-txns-input").addEventListener("input", renderTable);
  document.getElementById("inspector-txn-select").addEventListener("change", (e) => {
    inspectTransaction(e.target.value);
  });

  // Quick Prompt Buttons
  document.querySelectorAll(".quick-prompt-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const query = btn.getAttribute("data-query");
      handleChatQuery(query);
    });
  });

  // Chat Input
  document.getElementById("btn-send-chat").addEventListener("click", () => {
    const input = document.getElementById("chat-user-input");
    const query = input.value.trim();
    if (query) {
      handleChatQuery(query);
      input.value = "";
    }
  });

  document.getElementById("chat-user-input").addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      const query = e.target.value.trim();
      if (query) {
        handleChatQuery(query);
        e.target.value = "";
      }
    }
  });

  // CSV Download Button
  document.getElementById("btn-download-csv").addEventListener("click", () => {
    const headers = ["transaction_id", "invoice_id", "customer_name", "invoice_amount", "paid_amount", "difference", "reconciliation_status", "risk_level", "payment_method", "payment_date", "ai_reason", "recommended_action"];
    const rows = currentDataset.map(r => headers.map(h => `"${String(r[h] || '').replace(/"/g, '""')}"`).join(","));
    const csvContent = headers.join(",") + "\n" + rows.join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `PayMatch_AI_Reconciliation_${new Date().toISOString().slice(0,10)}.csv`;
    link.click();
  });

  // Markdown Download Button
  document.getElementById("btn-download-md").addEventListener("click", () => {
    const mdContent = generateExecutiveReport(currentMetrics, currentDataset);
    const blob = new Blob([mdContent], { type: "text/markdown;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `PayMatch_AI_Executive_Summary_${new Date().toISOString().slice(0,10)}.md`;
    link.click();
  });
}

// Run when DOM is ready
document.addEventListener("DOMContentLoaded", initApp);
