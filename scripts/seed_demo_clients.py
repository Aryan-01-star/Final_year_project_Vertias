"""
Seed three demo client applications with clearly different credit risk profiles:

  priya  -> Minimal Risk (excellent credit)
  vikram -> Low Risk     (moderate credit)
  rajesh -> High Risk    (poor credit, defaulting)

The customer_name column matches the login username so each client only sees
their own application on the client dashboard. Re-running this script wipes the
previous demo rows for these usernames and re-inserts them.
"""

import json
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'backend', 'veritas.db')

DOC_KEYS = [
    ('proof_identity', 'Proof of Identity'),
    ('proof_income', 'Proof of Income'),
    ('proof_address', 'Address Proof'),
    ('bank_statements', 'Bank Statements'),
    ('tax_returns', 'Tax Returns'),
    ('employment_verification', 'Employment Verification'),
]


def _completed_documents_json():
    return json.dumps({
        key: {
            'label': label,
            'required': True,
            'status': 'uploaded',
            'filename': f'{key}.pdf',
        }
        for key, label in DOC_KEYS
    })

DEMO_CLIENTS = [
    {
        'application_id': 'VNB-DEMO01',
        'customer_name': 'priya',
        'income': 1_800_000,
        'debt': 150_000,
        'credit_score': 820,
        'loan_amount': 800_000,
        'duration': 36,
        'risk_score': 920,
        'risk_label': 'Minimal Risk',
        'status': 'Waiting',
        'priority': 'Normal',
        'age': 32,
        'emp_length': 9.0,
        'home_ownership': 'MORTGAGE',
        'loan_intent': 'HOMEIMPROVEMENT',
        'loan_grade': 'A',
        'int_rate': 8.5,
    },
    {
        'application_id': 'VNB-DEMO02',
        'customer_name': 'vikram',
        'income': 950_000,
        'debt': 320_000,
        'credit_score': 715,
        'loan_amount': 600_000,
        'duration': 48,
        'risk_score': 720,
        'risk_label': 'Low Risk',
        'status': 'Waiting',
        'priority': 'Normal',
        'age': 38,
        'emp_length': 6.0,
        'home_ownership': 'RENT',
        'loan_intent': 'PERSONAL',
        'loan_grade': 'C',
        'int_rate': 12.4,
    },
    {
        'application_id': 'VNB-DEMO03',
        'customer_name': 'rajesh',
        'income': 480_000,
        'debt': 410_000,
        'credit_score': 590,
        'loan_amount': 350_000,
        'duration': 60,
        'risk_score': 380,
        'risk_label': 'High Risk',
        'status': 'Waiting',
        'priority': 'Critical',
        'age': 47,
        'emp_length': 1.5,
        'home_ownership': 'RENT',
        'loan_intent': 'MEDICAL',
        'loan_grade': 'E',
        'int_rate': 16.8,
    },
]

INSERT_SQL = '''
INSERT INTO applications (
    application_id, customer_name, income, debt, credit_score,
    loan_amount, duration, risk_score, risk_label, status, priority,
    age, emp_length, home_ownership, loan_intent, loan_grade, int_rate
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
'''

CLIENT_APP_INSERT_SQL = '''
INSERT INTO client_applications (
    username, application_id, estimated_loan,
    doc_step_complete, iris_verified, final_review_ready,
    status, documents_json
) VALUES (?, ?, ?, 1, 1, 1, 'Submitted', ?)
'''


def seed():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}. Start the Flask app once to initialize it.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    usernames = [c['customer_name'] for c in DEMO_CLIENTS]
    placeholders = ','.join('?' for _ in usernames)
    cursor.execute(
        f"DELETE FROM applications WHERE customer_name IN ({placeholders})",
        usernames,
    )
    cursor.execute(
        f"DELETE FROM applications WHERE application_id IN ({placeholders})",
        [c['application_id'] for c in DEMO_CLIENTS],
    )
    cursor.execute(
        f"DELETE FROM client_applications WHERE username IN ({placeholders})",
        usernames,
    )

    documents_json = _completed_documents_json()

    for client in DEMO_CLIENTS:
        cursor.execute(INSERT_SQL, (
            client['application_id'], client['customer_name'], client['income'],
            client['debt'], client['credit_score'], client['loan_amount'],
            client['duration'], client['risk_score'], client['risk_label'],
            client['status'], client['priority'], client['age'],
            client['emp_length'], client['home_ownership'], client['loan_intent'],
            client['loan_grade'], client['int_rate'],
        ))
        cursor.execute(CLIENT_APP_INSERT_SQL, (
            client['customer_name'],
            client['application_id'],
            client['loan_amount'],
            documents_json,
        ))
        print(
            f"  + {client['customer_name']:7s} | credit {client['credit_score']} | "
            f"risk {client['risk_score']:3d} ({client['risk_label']}) | {client['status']}"
        )

    conn.commit()
    conn.close()
    print("\nDone. Login with priya/priya123, vikram/vikram123, or rajesh/rajesh123.")


if __name__ == "__main__":
    seed()
