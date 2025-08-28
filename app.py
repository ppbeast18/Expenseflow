from flask import Flask,render_template,request,redirect,url_for,send_file
import os
import pdfplumber,joblib
import pandas as pd
import re
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'model')

model = joblib.load(os.path.join(MODEL_DIR, 'model.pkl'))
vectorizer = joblib.load(os.path.join(MODEL_DIR, 'vectorizer.pkl'))

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    return render_template("index.html")  # show actual homepage after login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    uploaded_file = request.files['bankfile']

    if uploaded_file.filename.endswith('.pdf'):
        path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(path)

        # Process PDF with pdfplumber
        transactions = []

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue
                lines = text.split("\n")

                for i in range(len(lines)):
                    line = lines[i]
                    if "DEBIT ₹" in line or "CREDIT ₹" in line:
                        direction = "DEBIT" if "DEBIT ₹" in line else "CREDIT"
                        amount_match = re.search(r"₹([\d,]+)", line)
                        amount = amount_match.group(1).replace(",", "") if amount_match else ""
                        name = line
                        name = re.sub(r"(DEBIT|CREDIT) ₹[\d,]+", "", name)
                        name = re.sub(r"(Paid to|Payment to|Received from)", "", name).strip()

                        date, time, utr = "", "", ""
                        for j in range(i - 3, i):
                            if re.match(r"\b[A-Za-z]{3} \d{2}, \d{4}", lines[j]):
                                date = lines[j]
                            elif re.match(r"\d{2}:\d{2} (am|pm)", lines[j]):
                                time_match = re.search(r"\d{2}:\d{2} (am|pm)", lines[j])
                                if time_match:
                                    time = time_match.group(0)

                        for j in range(i+1, min(i+6, len(lines))):
                            if "UTR No." in lines[j]:
                                utr = lines[j].replace("UTR No.", "").strip()

                        transactions.append({
                            "Date": date,
                            "Time": time,
                            "Name": name,
                            "Type": direction,
                            "Amount": amount,
                            "UTR No.": utr
                        })

        df = pd.DataFrame(transactions)
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df['date'] = df['Name'].str.extract(r'^([A-Za-z]{3} \d{1,2}, \d{4})')
        df['Name'] = df['Name'].str.replace(r'^([A-Za-z]{3} \d{1,2}, \d{4})\s*', '', regex=True)
        df.rename(columns={'Date': 'serial number'}, inplace=True)

        # output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'final.csv')
        # df = pd.read_csv(output_path)
        df = df.rename(columns={"serial number": "S.No", "date": "Date", "UTR No.": "UTR No"})
        desired = df[["S.No", "Date", "Name", "Amount", "Type", "Time", "UTR No"]]

        desired.loc[:, 'combined'] = desired['Name'].fillna('')

        # Predict categories
        X_desired = vectorizer.transform(desired['combined'])
        probs = model.predict_proba(X_desired)
        max_probs = probs.max(axis=1)
        predicted_indices = probs.argmax(axis=1)
        threshold = 0.7
        predicted_labels = []
        for prob, idx in zip(max_probs, predicted_indices):
            if prob < threshold:
                predicted_labels.append('contacts')
            else:
                predicted_labels.append(model.classes_[idx])
        desired.loc[:, 'Predicted_Category'] = predicted_labels

        debits_only = desired[desired['Type'].str.lower() == 'debit']
        credits_only = desired[desired['Type'].str.lower() == 'credit']
        total_sum = sum(desired['Amount'])

        total_debit_sum = debits_only['Amount'].sum()
        total_credit_sum = credits_only['Amount'].sum()
        total_sum = desired['Amount'].sum()


        category_grouped = desired.groupby('Predicted_Category')['Amount'].sum().reset_index()
        category_grouped = category_grouped.sort_values(by='Amount', ascending=False)

        grouped_debits = debits_only.groupby('Name')['Amount'].sum().reset_index().sort_values(by='Amount', ascending=False)
        grouped_credits = credits_only.groupby('Name')['Amount'].sum().reset_index().sort_values(by='Amount', ascending=False)

        top_debits = grouped_debits.head(15)
        top_credits = grouped_credits.head(15)

# Convert to dicts or lists for passing to template
        debit_names = top_debits['Name'].tolist()
        debit_amounts = top_debits['Amount'].tolist()
        credit_names = top_credits['Name'].tolist()
        credit_amounts = top_credits['Amount'].tolist()
        category_names = category_grouped['Predicted_Category'].tolist()
        category_amounts = category_grouped['Amount'].tolist()


        # debits_html = debits_only.to_html(classes='table table-bordered', index=False)
        # credits_html = credits_only.to_html(classes='table table-bordered', index=False)

        return render_template(
            'visualization.html',
            # debits_table=debits_html,
            # credits_table=credits_html,
            total_debit=total_debit_sum,
            total_credit=total_credit_sum,
            total_sum = total_sum,
            debit_names=debit_names,
            debit_amounts=debit_amounts,
            credit_names=credit_names,
            credit_amounts=credit_amounts,
            category_names=category_names,
            category_amounts=category_amounts,
        )
        
        # df.to_csv(output_path, index=False)
        # return send_file(output_path, as_attachment=True) ---sending file back to user to download

    else:
        return "Please upload a valid PDF file."

if __name__ == '__main__':
    app.run(debug=True)
