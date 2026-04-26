import requests

BASE_URL = 'http://127.0.0.1:5000'

def test_api():
    session = requests.Session()
    # Log in as admin using JSON
    login_data = {'username': 'admin', 'password': 'admin123', 'role': 'company'}
    r = session.post(f"{BASE_URL}/login", json=login_data)
    if r.status_code != 200:
        print(f"Login failed: {r.status_code}")
        print(r.text)
        return

    # Fetch applications
    r = session.get(f"{BASE_URL}/api/applications")
    if r.status_code == 200:
        apps = r.json()
        print(f"Fetched {len(apps)} applications")
        # Print the first few to check structure
        for app in apps[:3]:
            print(app)
    else:
        print(f"API failed with status {r.status_code}")
        print(r.text)

if __name__ == "__main__":
    test_api()
