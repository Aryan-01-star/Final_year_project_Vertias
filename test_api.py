import requests

BASE_URL = 'http://127.0.0.1:5000'

def test_api():
    session = requests.Session()
    # Log in as admin
    login_data = {'username': 'admin', 'password': 'admin123', 'role': 'company'}
    r = session.post(f"{BASE_URL}/login", data=login_data)
    if r.status_code != 200:
        print("Login failed")
        return

    # Fetch applications
    r = session.get(f"{BASE_URL}/api/applications")
    if r.status_code == 200:
        apps = r.json()
        print(f"Fetched {len(apps)} applications")
        for app in apps:
            print(f"ID: {app.get('application_id')}, Status: {app.get('status')}")
    else:
        print(f"API failed with status {r.status_code}")
        print(r.text)

if __name__ == "__main__":
    test_api()
