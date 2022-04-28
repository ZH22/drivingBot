from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from db_helper import getAccount

def login(teleID):
    ser = Service("./drivers/chromedriver")
    
    opt = webdriver.ChromeOptions()

    browser = webdriver.Chrome(service=ser, options=opt)
    # browser.minimize_window()
    browser.get('https://info.bbdc.sg/members-login/')

    print("Logging In")
    USERNAME, PASSWORD = getAccount(teleID)

    # Cheng Xun's
    # USERNAME = <USERNAME>
    # PASSWORD = <PASSWORD>

    browser.find_element(By.ID, "txtNRIC").send_keys(USERNAME)
    browser.find_element(By.ID, "txtPassword").send_keys(PASSWORD)
    browser.find_element(By.ID, "loginbtn").click()

    wait = WebDriverWait(browser, 30)

    # Wait until the warning page shows
    wait.until(
        EC.title_is("Form is not secure")
    )
    
    browser.find_element(By.ID, "proceed-button").click()
    
    return browser, wait

def getPracPage(teleID, selectedMonth=[]):
    # CONSTANTS ==============================
    bookingLink_xpath = "/html/body/table/tbody/tr/td/table/tbody/tr[15]/td[3]/a"

    # ========================================

    # Login
    browser, wait = login(teleID)

    # Wait until booking page loads
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'leftFrame')))
    print("Booking Page Loaded")

    # Click on practical booking
    browser.find_element(By.XPATH, bookingLink_xpath).click()

    browser.switch_to.default_content()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'mainFrame')))

    browser.find_element(By.XPATH, "/html/body/table/tbody/tr[3]/td[1]/input").click()

    # TIMING SELECTOR======================================================================
    allMonths = browser.find_elements(By.XPATH, '//*[@id="checkMonth"]')
    
    # Select specific months (if not specified select all)
    currentMonth = 0
    for month in allMonths:
        currentMonth += 1
        if((currentMonth in selectedMonth) or (len(selectedMonth)==0)):
            month.click()

    browser.find_element(By.NAME , 'allSes').click()
    browser.find_element(By.NAME , 'allDay').click()
    browser.find_element(By.NAME , 'btnSearch').click()
    # ======================================================================================

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

# ==============================================================================================
# For getting to TPDS booking slots ============================================================
def reachedLimit(browser):
    from selenium.common.exceptions import NoSuchElementException
    try:
        browser.find_element(By.XPATH, '//*[@id="TblSpan"]/table/tbody/tr/td/table/tbody/tr[2]/td')
    except:
        return False
    return True


def getTPDS(teleID, modNum, selectedMonth=[]):
    # Booking Link XPATH
    TPDS_xpath = "/html/body/table/tbody/tr/td/table/tbody/tr[11]/td[3]/a"

    browser, wait = login(teleID)
    # Wait until booking page loads
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'leftFrame')))
    print("Booking Page Loaded")

    # Click on TDPS link
    browser.find_element(By.XPATH, TPDS_xpath).click()

    browser.switch_to.default_content()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'mainFrame')))
    
    # STOP IF LIMIT REACHED
    if(reachedLimit(browser)):
        print("TPDS Limit Reached")
        return 0

    
    # Click on button
    module_number_xpath = f"/html/body/table/tbody/tr/td[2]/form/table[1]/tbody/tr[3]/td/input[{str(modNum)}]"
    browser.find_element(By.XPATH, module_number_xpath).click()
    browser.find_element(By.NAME, 'btnSubmit').click()
    
    allMonths = browser.find_elements(By.XPATH, '//*[@id="checkMonth"]')
    
    # Select specific months (if not specified select all)
    currentMonth = 0
    for month in allMonths:
        currentMonth += 1
        if((currentMonth in selectedMonth) or (len(selectedMonth)==0)):
            month.click()

    browser.find_element(By.NAME , 'allSes').click()
    browser.find_element(By.NAME , 'allDay').click()
    browser.find_element(By.NAME , 'btnSearch').click()

    # Switch to mainframe
    browser.switch_to.default_content()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'mainFrame')))

    # Save HTML file for processing
    tablePageSource = browser.page_source
    browser.quit()
    return tablePageSource

def getFTT(teleID, selectedMonth=[]):
    # FTT X-Path
    FTT_XPATH = "/html/body/table/tbody/tr/td/table/tbody/tr[29]/td[3]/a"
    ACCEPT_XPATH = "/html/body/table/tbody/tr[7]/td/center/table/tbody/tr[6]/td[1]/input"

    browser, wait = login(teleID)
    # Wait until booking page loads
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'leftFrame')))
    print("Booking Page Loaded")

    # Click on FTT link
    browser.find_element(By.XPATH, FTT_XPATH).click()

    browser.switch_to.default_content()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'mainFrame')))

    # Click on FTT accept
    browser.find_element(By.XPATH, ACCEPT_XPATH).click()


    FTT_MOD_XPATH = "/html/body/table/tbody/tr/td[2]/form/table/tbody/tr[3]/td/input[2]"
    browser.find_element(By.XPATH, FTT_MOD_XPATH).click()

    # Click accept
    browser.find_element(By.NAME, 'btnSubmit').click()

    allMonths = browser.find_elements(By.XPATH, '//*[@id="checkMonth"]')
    
    # Select specific months (if not specified select all)
    currentMonth = 0
    for month in allMonths:
        currentMonth += 1
        if((currentMonth in selectedMonth) or (len(selectedMonth)==0)):
            month.click()

    browser.find_element(By.NAME , 'allSes').click()
    browser.find_element(By.NAME , 'allDay').click()
    browser.find_element(By.NAME , 'btnSearch').click()

    try: 
        WebDriverWait(browser, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
        alert_obj = browser.switch_to.alert
        alert_obj.accept()
    except TimeoutException:
        print("no alert")


    # Switch to mainframe
    browser.switch_to.default_content()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'mainFrame')))

    # Save HTML file for processing
    tablePageSource = browser.page_source
    browser.quit()
    return tablePageSource