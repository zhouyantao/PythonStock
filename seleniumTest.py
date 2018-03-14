# __*__ code:utf-8 __*__

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.action_chains import ActionChains

browser=webdriver.Chrome()
browser.get('https://www.baidu.com')
input=browser.find_element_by_css_selector('#kw')
input.send_keys('selenium')
submit=browser.find_element_by_css_selector('#su')
actions=ActionChains(browser)
actions.move_to_element(submit)
actions.click(submit)
actions.perform()
#browser.quit()

