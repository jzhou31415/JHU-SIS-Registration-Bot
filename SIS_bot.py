from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from getpass import getpass
import time
import datetime

#JHU SIS Registration Bot made with Selenium

def login_sis(driver, username, password, authentication):
    driver.get("https://sis.jhu.edu/sswf/")
    signInButton = wait.until(EC.element_to_be_clickable((By.ID, "linkSignIn")))
    signInButton.click()
    user_elem = wait.until(EC.element_to_be_clickable((By.ID, "i0116"))) 
    user_elem.clear()
    user_elem.send_keys(username)
    user_elem.send_keys(Keys.RETURN)
    pass_elem = wait.until(EC.element_to_be_clickable((By.ID, "i0118"))) 
    pass_elem.clear()
    pass_elem.send_keys(password)
    pass_elem.send_keys(Keys.RETURN)
    fa_elem = wait.until(EC.element_to_be_clickable((By.ID, "idTxtBx_SAOTCC_OTC")))
    fa_elem.clear()
    fa_elem.send_keys(authentication)
    fa_elem.send_keys(Keys.RETURN)

username = input("your jhu username <jhed@jh.edu>: ")
password = getpass("your jhu password (password will not appear on screen): ")
registration_date = input("the date of your registration in (MM/DD/YYYY) format: ")
authentication = input("the 2FA code in your authenticator app for SIS: ")
list = registration_date.split("/")

# 7:00.00 AM Registration Time, set your timezone to EST with Naval Clock
#registration_time = datetime.datetime.combine(datetime.date.today(), datetime.time(hour=7,minute=0, second=0, microsecond=15))
registration_time = datetime.datetime(int(list[2]), int(list[0]), int(list[1]), hour = 7, minute = 0, second = 0, microsecond = 15)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)
login_sis(driver, username, password, authentication)
wait.until(lambda d : d.find_element(By.ID, "img-jhu-shield-only"))
driver.get("https://sis.jhu.edu/sswf/SSS/EnrollmentCart/SSS_EnrollmentCart.aspx?MyIndex=88199")
select_all = wait.until(EC.element_to_be_clickable((By.ID, "SelectAllCheckBox")))
select_all.click()
register_button = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_contentPlaceHolder_ibEnroll")))
while True:
    curr_time = datetime.datetime.now()
    time = "Waiting... \nCurrent Time: " + curr_time.strftime('%B-%d-%Y %H:%M:%S') + "\nWaiting until: " + registration_time.strftime('%B-%d-%Y %H:%M:%S')
    print("\033[H\033[J", end="")
    print(time, end="\r")
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass
    if curr_time >= registration_time:
        print("Registering")
        register_button.click()
        while True:
            if (driver.find_element(By.ID, "ctl00_contentPlaceHolder_lblWaitlist")):
                yes = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_contentPlaceHolder_rbWaitlistYes")))
                yes.click()
                cont = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_contentPlaceHolder_cmdContinue")))
                cont.click()
                break
