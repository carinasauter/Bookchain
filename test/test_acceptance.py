from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from flask_testing import LiveServerTestCase
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument('-headless')
firefox = Firefox(firefox_options=options)


def test_login():
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(chrome_options=options)
	driver.get('http://localhost:8081/login')
	userfield = driver.find_element_by_id("username")
	userfield.send_keys("carina")
	passwordfield = driver.find_element_by_id("password")
	passwordfield.send_keys("abc")
	elem = driver.find_element_by_id("loginButton").click()
	assert "Dashboard" in driver.page_source

# def test_signup():
#     options = webdriver.ChromeOptions()
#     options.add_argument('headless')
#     driver = webdriver.Chrome(chrome_options=options)
   
#     driver.get('http://localhost:8081/hello')
#     assert "Hello" in driver.page_source

# def test_result():
#     options = webdriver.ChromeOptions()
#     options.add_argument('headless')
#     driver = webdriver.Chrome(chrome_options=options)
#     driver.get('http://localhost:8081/result?first_number=4&second_number=10&submit_button=Submit')
#     assert "40" in driver.page_source

# def test2():
#     options = webdriver.ChromeOptions()
#     options.add_argument('headless')
#     driver = webdriver.Chrome(chrome_options=options)
#     driver.get('http://localhost:8080/multiplication')
#     element = driver.find_element_by_name("first_number")
#     element.send_keys("5")

#     element = driver.find_element_by_name("second_number")
#     element.send_keys("10")
#     driver.find_element_by_id("submit").click()
#     assert "50" in driver.page_source


