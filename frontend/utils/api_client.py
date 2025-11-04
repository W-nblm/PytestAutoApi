import requests

API_BASE = "http://127.0.0.1:8000"

def post(endpoint, files=None, data=None, json=None):
    url = f"{API_BASE}{endpoint}"
    resp = requests.post(url, files=files, data=data, json=json)
    if resp.status_code == 200:
        return resp.json()
    else:
        return {"code": 1, "message": resp.text}
