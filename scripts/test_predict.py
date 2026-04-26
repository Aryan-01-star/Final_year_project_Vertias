import requests
import json
import pandas as pd

# Start the server if not already running (assuming it's on 5000)
URL = "http://127.0.0.1:5000/predict"

# Test data based on a known 'Default' case (loan_status=1)
# person_age: 22, person_income: 59000, person_home_ownership: RENT, person_emp_length: 123.0, 
# loan_intent: PERSONAL, loan_grade: D, loan_amnt: 35000, loan_int_rate: 16.02, loan_status: 1
test_case_default = {
    "customer_name": "Test Default User",
    "income": 59000,
    "debt": 15000,
    "credit_score": 580,
    "loan_amount": 35000,
    "duration": 24,
    "age": 22,
    "emp_length": 5.0 # Reduced from 123 to be 'realistic'
}

# Test data based on a known 'Non-Default' case (loan_status=0)
# 21,9600,OWN,5.0,EDUCATION,B,1000,11.14,0
test_case_safe = {
    "customer_name": "Test Safe User",
    "income": 96000, # Increased for better ratio
    "debt": 2000,
    "credit_score": 820,
    "loan_amount": 5000,
    "duration": 12,
    "age": 25,
    "emp_length": 4.0
}

def test_prediction(case, label):
    print(f"Testing {label} case...")
    try:
        # We need to simulate the session/login if it's @login_required
        # But app.py has a demo bypass, so any credentials might work if we send them in headers or session?
        # Actually, let's just use a session object.
        session = requests.Session()
        # Login first
        session.post("http://127.0.0.1:5000/login", json={"username": "admin", "password": "admin123", "role": "company"})
        
        response = session.post(URL, json=case)
        if response.status_code == 200:
            result = response.json()
            print(f"Result: Score={result['score']}, Label={result['risk_label']}, Recommendation={result['recommendation']}")
            return result
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    test_prediction(test_case_default, "DEFAULT")
    test_prediction(test_case_safe, "SAFE")
