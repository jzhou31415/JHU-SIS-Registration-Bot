from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from getpass import getpass
import time
import datetime

#JHU SIS Registration Bot made with Selenium

def login_sis(driver, username, password):
    driver.get("https://sis.jhu.edu/sswf/")
    signInButton = wait.until(EC.element_to_be_clickable((By.ID, "linkSignIn")))
    signInButton.click()
    user_elem = wait.until(EC.element_to_be_clickable((By.ID, "i0116"))) 
    user_elem.clear()
    user_elem.send_keys(username)
    submit_btn = driver.find_element(By.ID, "idSIButton9") 
    submit_btn.click()
    pass_elem = wait.until(EC.element_to_be_clickable((By.ID, "i0118"))) 
    pass_elem.clear()
    pass_elem.send_keys(password)
    pass_elem.send_keys(Keys.RETURN)    

username = input("your jhu username <jhed@jh.edu>: ")
password = getpass("your jhu password (password will not appear on screen): ")

#7:00.00 AM Registration Time, set your timezone to EST with Naval Clock
registration_time = datetime.datetime.combine(datetime.date.today(), datetime.time(hour=7,minute=0, second=0, microsecond=15))
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)
login_sis(driver, username, password)
wait.until(lambda d : d.find_element(By.ID, "img-jhu-shield-only"))
driver.get("https://sis.jhu.edu/sswf/SSS/EnrollmentCart/SSS_EnrollmentCart.aspx?MyIndex=88199")
select_all = wait.until(EC.element_to_be_clickable((By.ID, "SelectAllCheckBox")))
select_all.click()
register_button = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_contentPlaceHolder_ibEnroll")))
while True:
    curr_time = datetime.datetime.now()
    time = "Waiting... " + curr_time.strftime('%H:%M:%S')
    print(time, end="\r")
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass
    if curr_time >= registration_time:
        print("Executing")
        register_button.click()
        while True:
            if (driver.find_element(By.ID, "ctl00_contentPlaceHolder_lblWaitlist")):
                yes = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_contentPlaceHolder_rbWaitlistYes")))
                yes.click()
                cont = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_contentPlaceHolder_cmdContinue")))
                cont.click()
                break



