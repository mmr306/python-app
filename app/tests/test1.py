from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def test_lambdatest_todo_app():
    #chrome_driver = webdriver.Chrome()
    chrome_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    chrome_driver.get('https://vermontvt.com/')

    title = "Dash"
    sleep(2)
    assert title == chrome_driver.title
    
    sleep(2)
    chrome_driver.close()