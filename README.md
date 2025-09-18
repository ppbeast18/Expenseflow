Personal Expense Classification Dashboard

📌 Overview
This project is a Personal Finance Dashboard built with Flask and Firebase Authentication.
It allows users to upload their bank transaction data, automatically classifies transactions using an SVM model, and presents clear visual insights into their financial flow.

✨ Features
  .🔐 User Authentication → Secure login/signup with Firebase
  .📂 Transaction Upload → Upload bank statements for analysis
  .🤖 Machine Learning Model → Classifies transactions into categories using SVM
  .📊 Interactive Dashboard →
      .Shows Total Amount, Debit Total, and Credit Total
      .Pie Chart (Debit Distribution) → Top 15 debit transactions + "Others"
      .Pie Chart (Credit Distribution) → Top 15 credit transactions + "Others"
      .Pie Chart (Categorized Transactions) → ML-predicted spending categories
      .📑 PDF Report Generation → Exports total debit, credit, and categorized insights into a PDF

🛠️ Tech Stack
Backend: Flask
Authentication: Firebase
Machine Learning: Scikit-learn (Support Vector Machine)
Visualization: Chart.js / Matplotlib (for pie charts)
Export: ReportLab / FPDF for PDF generation

🚀 How It Works
  .User signs up / logs in via Firebase.
  .Upload a bank statement (CSV/Excel).
  .The SVM model processes and classifies each transaction.
  .Dashboard displays:
      .Total, debit, and credit amounts
      .Top 15 debit & credit transactions with “Others” grouped
      .Categorized spending distribution
      .User can download a PDF summary report.

🔮 Future Improvements

  .📩 Automated Data Fetching → Fetch bank statements directly from user emails (Gmail/Outlook API) after user consent, similar to how U.S. apps handle e-statements.
  .📊 Add line/bar charts for monthly spending trends.
  .💰 Enable budget tracking & smart alerts for overspending.
  .👥 Provide multi-user expense comparisons (family/group tracking).
  .🤖 Expand ML model with deep learning for more accurate transaction categorization.
