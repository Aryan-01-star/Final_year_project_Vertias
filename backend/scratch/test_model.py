import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model.joblib')
ENCODER_PATH = os.path.join(BASE_DIR, 'encoders.joblib')
FEATURES_PATH = os.path.join(BASE_DIR, 'features.joblib')

model = joblib.load(MODEL_PATH)
encoders = joblib.load(ENCODER_PATH)
feature_names = joblib.load(FEATURES_PATH)

def test_predict(income, loan_amnt, credit_score, age=30, emp_length=5):
    # Derive grade
    if credit_score >= 750: grade = 'A'
    elif credit_score >= 700: grade = 'B'
    elif credit_score >= 650: grade = 'C'
    elif credit_score >= 600: grade = 'D'
    elif credit_score >= 550: grade = 'E'
    else: grade = 'F'
    
    features = {
        'person_age': age,
        'person_income': income,
        'person_home_ownership': 'RENT',
        'person_emp_length': emp_length,
        'loan_intent': 'PERSONAL',
        'loan_grade': grade,
        'loan_amnt': loan_amnt,
        'loan_int_rate': 11.0,
        'loan_percent_income': loan_amnt / income if income > 0 else 0,
        'cb_person_default_on_file': 'N',
        'cb_person_cred_hist_length': 2
    }
    
    input_df = pd.DataFrame([features])
    for col, le in encoders.items():
        if col in input_df.columns:
            input_df[col] = le.transform(input_df[col])
            
    input_df = input_df[feature_names]
    prob = model.predict_proba(input_df)[0][1]
    score = int((1 - prob) * 1000)
    return score, prob

def test_int_rate(int_rate):
    features = {
        'person_age': 30,
        'person_income': 1200000,
        'person_home_ownership': 'RENT',
        'person_emp_length': 10,
        'loan_intent': 'PERSONAL',
        'loan_grade': 'A',
        'loan_amnt': 100000,
        'loan_int_rate': int_rate,
        'loan_percent_income': 100000 / 1200000,
        'cb_person_default_on_file': 'N',
        'cb_person_cred_hist_length': 2
    }
    input_df = pd.DataFrame([features])
    for col, le in encoders.items():
        if col in input_df.columns:
            input_df[col] = le.transform(input_df[col])
    input_df = input_df[feature_names]
    prob = model.predict_proba(input_df)[0][1]
    return int((1 - prob) * 1000), prob

def test_home(home):
    features = {
        'person_age': 30,
        'person_income': 1200000,
        'person_home_ownership': home,
        'person_emp_length': 10,
        'loan_intent': 'PERSONAL',
        'loan_grade': 'A',
        'loan_amnt': 100000,
        'loan_int_rate': 11.0,
        'loan_percent_income': 100000 / 1200000,
        'cb_person_default_on_file': 'N',
        'cb_person_cred_hist_length': 2
    }
    input_df = pd.DataFrame([features])
    for col, le in encoders.items():
        if col in input_df.columns:
            input_df[col] = le.transform(input_df[col])
    input_df = input_df[feature_names]
    prob = model.predict_proba(input_df)[0][1]
    return int((1 - prob) * 1000), prob

print("\nHome Ownership Impact:")
for h in ['RENT', 'OWN', 'MORTGAGE']:
    print(f"{h}: {test_home(h)}")
