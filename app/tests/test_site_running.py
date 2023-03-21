import requests

def test_app_running():
    r = requests.get("https://vermontvt.com") 
    assert r.status_code == 200