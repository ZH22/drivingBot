
def getTable(showBrowser=False):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException

    # CONSTANTS ==============================
    bookingLink_xpath = "/html/body/table/tbody/tr/td/table/tbody/tr[15]/td[3]/a"

    # ========================================

    ser = Service("./drivers/chromedriver")
    
    opt = webdriver.ChromeOptions()
    if(not showBrowser):
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        opt.add_argument('--no-sandbox')
        opt.add_argument('--disable-gpu')
        opt.add_argument("--headless")
        opt.add_argument('--window-size=1920x1080')
        opt.add_argument(f'user-agent={user_agent}')

    browser = webdriver.Chrome(service=ser, options=opt)
    browser.get('https://info.bbdc.sg/members-login/')

    print("Logging In")
    # try: 
    # Login

    USERNAME = <USERNAME>
    PASSWORD = <PASSWORD>
    browser.find_element(By.ID, "txtNRIC").send_keys(USERNAME)
    browser.find_element(By.ID, "txtPassword").send_keys(PASSWORD)
    browser.find_element(By.ID, "loginbtn").click()

    wait = WebDriverWait(browser, 30)

    # Wait until the warning page shows
    wait.until(
        EC.title_is("Form is not secure")
    )
    
    browser.find_element(By.ID, "proceed-button").click()

    # Wait until booking page loads
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'leftFrame')))
    print("Booking Page Loaded")

    # Click on practical booking
    browser.find_element(By.XPATH, bookingLink_xpath).click()

    browser.switch_to.default_content()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'mainFrame')))

    browser.find_element(By.XPATH, "/html/body/table/tbody/tr[3]/td[1]/input").click()

    # TIMING SELECTOR
    allMonths = browser.find_elements(By.XPATH, '//*[@id="checkMonth"]')

    for month in allMonths:
        month.click()

    # browser.find_element(By.XPATH, '//*[@id="checkSes"]').click()
    # browser.find_element(By.XPATH, '//*[@id="checkDay"]').click()
    browser.find_element(By.NAME , 'allSes').click()
    browser.find_element(By.NAME , 'allDay').click()
    browser.find_element(By.NAME , 'btnSearch').click()

    print("Selected Options")
    try: 
        WebDriverWait(browser, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
        alert_obj = browser.switch_to.alert
        alert_obj.accept()
    except TimeoutException:
        print("no alert")

    browser.switch_to.default_content()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'mainFrame')))

    # Save HTML file for processing
    tablePageSource = browser.page_source
    browser.quit()
    return tablePageSource

if __name__ == "__main__":
    import datetime
    pageSource = getTable()

    with open("./temp/temp.html", "w") as f:
        f.write(pageSource)

    with open("./temp/lastMod.txt", "w") as f:
        e = datetime.datetime.now()
        f.write(f"{e}")