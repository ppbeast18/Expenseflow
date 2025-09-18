# Personal Expense Classification Dashboard

## 📌 Overview

This project is a Personal Finance Dashboard built with **Flask** and **Firebase Authentication**.  
It allows users to upload their bank transaction data, automatically classifies transactions using an SVM model, and presents clear visual insights into their financial flow.

---

## ✨ Features

- 🔐 **User Authentication:** Secure login/signup with Firebase
- 📂 **Transaction Upload:** Upload bank statements (CSV/Excel) for analysis
- 🤖 **Machine Learning Model:** Automatically classifies transactions into categories using SVM
- 📊 **Interactive Dashboard:**
    - Shows Total Amount, Debit Total, and Credit Total
    - **Pie Chart (Debit Distribution):** Top 15 debit transactions + "Others"
    - **Pie Chart (Credit Distribution):** Top 15 credit transactions + "Others"
    - **Pie Chart (Categorized Transactions):** ML-predicted spending categories
- 📑 **PDF Report Generation:** Exports total debit, credit, and categorized insights into a PDF

---

## 🛠️ Tech Stack

- **Backend:** Flask
- **Authentication:** Firebase
- **Machine Learning:** Scikit-learn (Support Vector Machine)
- **Visualization:** Chart.js / Matplotlib (for pie charts)
- **Export:** ReportLab / FPDF for PDF generation

---

## 🚀 How It Works

1. User signs up / logs in via Firebase.
2. User uploads a bank statement (CSV or Excel).
3. The SVM model processes and classifies each transaction.
4. Dashboard displays:
    - Total, debit, and credit amounts
    - Top 15 debit & credit transactions (with "Others" grouping)
    - Categorized spending distribution
    - User can download a PDF summary report.

---

## 🔮 Future Improvements

- 📩 **Automated Data Fetching:** Fetch statements from user emails (Gmail/Outlook API) after user consent.
- 📊 **Additional Visualizations:** Add line/bar charts for monthly spending trends.
- 💰 **Budget Tracking & Alerts:** Enable budget monitoring and smart alerts.
- 👥 **Multi-user Expense Comparisons:** Allow family/group expense tracking.
- 🤖 **Advanced ML Models:** Expand ML with deep learning for more accurate transaction categorization.

---

*For setup instructions and code samples, refer to the repository files and documentation.*
