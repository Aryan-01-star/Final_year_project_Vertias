import pandas as pd
import sqlite3
import os
import sys
import random

# Add backend to path to import database helpers if needed
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'backend', 'veritas.db')
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'credit_risk_dataset.csv')

NAMES = [
    "Rajesh Kumar", "Ananya Sharma", "Vikram Singh", "Priya Verma", 
    "Suresh Raina", "Meera Nair", "Arjun Kapoor", "Ishita Iyer",
    "Rohan Gupta", "Sana Khan", "Aditya Rao", "Kavya Menon",
    "Manish Pandey", "Deepika Padukone", "Ranveer Singh", "Alia Bhatt",
    "Virat Kohli", "MS Dhoni", "Sachin Tendulkar", "Sunil Chhetri"
]

RISK_LABELS = {
    0: ("Minimal Risk", "emerald"),
    1: ("High Risk", "red")
}

def seed():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found.")
        return

    print(f"Reading dataset from {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH).sample(100) # Seed 100 rows
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Clearing existing applications...")
    cursor.execute("DELETE FROM applications")
    
    print("Inserting 100 sample records...")
    for _, row in df.iterrows():
        app_id = f"VNB-{os.urandom(2).hex().upper()}"
        customer_name = random.choice(NAMES)
        
        # Determine status and label based on loan_status
        is_default = int(row['loan_status'])
        status = 'Rejected' if is_default == 1 else 'Approved'
        # Probability of default simulation for score
        if is_default == 1:
            score = random.randint(300, 500)
            label = "High Risk"
            priority = "Critical"
        else:
            score = random.randint(700, 950)
            label = "Low Risk" if score < 850 else "Minimal Risk"
            priority = "Normal"
            
        cursor.execute('''
        INSERT INTO applications (
            application_id, customer_name, income, debt, credit_score, 
            loan_amount, duration, risk_score, risk_label, status, priority,
            age, emp_length, home_ownership, loan_intent, loan_grade, int_rate
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            app_id,
            customer_name,
            row['person_income'],
            row['person_income'] * 0.3, # simulated debt
            random.randint(600, 850), # simulated credit score
            row['loan_amnt'],
            random.choice([12, 24, 36, 48, 60]),
            score,
            label,
            status,
            priority,
            row['person_age'],
            row['person_emp_length'],
            row['person_home_ownership'],
            row['loan_intent'],
            row['loan_grade'],
            row['loan_int_rate']
        ))
        
    conn.commit()
    conn.close()
    print("Seeding complete.")

if __name__ == "__main__":
    seed()
