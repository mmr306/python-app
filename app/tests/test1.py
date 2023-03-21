from selenium import webdriver
from time import sleep
 
def test_lambdatest_todo_app():
    chrome_driver = webdriver.Chrome()
    
    chrome_driver.get('https://vermontvt.com/')

    title = "Dash"
    sleep(2)
    assert title == chrome_driver.title
    
    sleep(2)
    chrome_driver.close()