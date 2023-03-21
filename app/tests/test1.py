import requests

def test_lambdatest_todo_app():
    r = requests.get("https://vermontvt.com") 
    assert r.status_code == 200