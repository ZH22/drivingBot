from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# CONSTANTS ==============================
bookingLink_xpath = "/html/body/table/tbody/tr/td/table/tbody/tr[15]/td[3]/a"

# ========================================

ser = Service("./drivers/chromedriver")
browser = webdriver.Chrome(service=ser)
browser.get('https://info.bbdc.sg/members-login/')

# try: 
# Login
USERNAME = <USERNAME>
PASSWORD = <PASSWORD>
browser.find_element(By.ID, "txtNRIC").send_keys(USERNAME)
browser.find_element(By.ID, "txtPassword").send_keys(PASSWORD)
browser.find_element(By.ID, "loginbtn").click()

# Wait until the warning page shows
elem = WebDriverWait(browser, 30).until(
    EC.title_is("Form is not secure")
)

browser.find_element(By.ID, "proceed-button").click()

# Wait until booking page loads

elem = WebDriverWait(browser, 30).until(
    EC.presence_of_element_located((By.XPATH, bookingLink_xpath))
)
print("booking page loaded")

browser.find_element_by_xpath(bookingLink_xpath).click()
print("clicked")  

print('Title: %s' % browser.title)
# browser.quit()