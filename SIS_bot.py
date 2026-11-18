from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoAlertPresentException,
    TimeoutException,
    WebDriverException,
)
from getpass import getpass
from multiprocessing import Process
import datetime
import time

# JHU SIS Registration Bot made with Selenium
# Runs NUM_WORKERS independent browser sessions that all try to register
# at the same moment.

NUM_WORKERS = 3
START_STAGGER = 3.0  # seconds between launching each worker process
REGISTRATION_STAGGER_MS = 7  # per-worker offset of the register click: worker N fires N ms after worker 0
TIGHT_POLL_WINDOW = 180  # seconds before registration when polling switches to continuous (no sleep)


def log(worker_id, message):
    print(f"[worker {worker_id}] {message}", flush=True)


def login_sis(driver, wait, username, password, authentication, worker_id=0):
    driver.get("https://sis.jhu.edu/sswf/")
    wait.until(EC.element_to_be_clickable((By.ID, "linkSignIn"))).click()

    user_elem = wait.until(EC.element_to_be_clickable((By.ID, "i0116")))
    user_elem.clear()
    user_elem.send_keys(username)
    user_elem.send_keys(Keys.RETURN)

    pass_elem = wait.until(EC.element_to_be_clickable((By.ID, "i0118")))
    pass_elem.clear()
    pass_elem.send_keys(password)
    pass_elem.send_keys(Keys.RETURN)

    if authentication:
        fa_elem = wait.until(EC.element_to_be_clickable((By.ID, "idTxtBx_SAOTCC_OTC")))
        fa_elem.clear()
        fa_elem.send_keys(authentication)
        # Stagger the submit: worker 0 immediately, worker 1 after 0.5s, worker 2 after 1.0s
        time.sleep(worker_id * 0.5)
        fa_elem.send_keys(Keys.RETURN)


def accept_alert_if_present(driver):
    try:
        driver.switch_to.alert.accept()
    except NoAlertPresentException:
        pass


def handle_waitlist(driver, wait, worker_id, timeout=60):
    """After clicking register, say 'yes' to the waitlist prompt if it shows up."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        accept_alert_if_present(driver)
        if driver.find_elements(By.ID, "ctl00_contentPlaceHolder_lblWaitlist"):
            wait.until(
                EC.element_to_be_clickable((By.ID, "ctl00_contentPlaceHolder_rbWaitlistYes"))
            ).click()
            wait.until(
                EC.element_to_be_clickable((By.ID, "ctl00_contentPlaceHolder_cmdContinue"))
            ).click()
            log(worker_id, "Waitlist confirmed")
            return
        time.sleep(0.05)
    log(worker_id, "No waitlist prompt appeared (registered, or the page changed)")


def run_worker(worker_id, username, password, authentication, registration_time):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)  # each worker gets its own browser/profile
    wait = WebDriverWait(driver, 30)

    try:
        login_sis(driver, wait, username, password, authentication, worker_id)
        wait.until(lambda d: d.find_element(By.ID, "img-jhu-shield-only"))
        log(worker_id, "Logged in")

        driver.get("https://sis.jhu.edu/sswf/SSS/EnrollmentCart/SSS_EnrollmentCart.aspx")
        wait.until(EC.element_to_be_clickable((By.ID, "SelectAllCheckBox"))).click()
        register_button = wait.until(
            EC.element_to_be_clickable((By.ID, "ctl00_contentPlaceHolder_ibEnroll"))
        )
        log(worker_id, "Cart ready, waiting for registration time")

        # Each worker fires slightly after the previous one: worker 0 at 0 ms, worker 1 at 1 ms, ...
        target_time = registration_time + datetime.timedelta(
            milliseconds=worker_id * REGISTRATION_STAGGER_MS
        )

        # Wait loop: only worker 0 prints the countdown so output isn't garbled.
        last_housekeeping = 0.0
        while True:
            now = datetime.datetime.now()
            remaining = (target_time - now).total_seconds()
            if remaining <= 0:
                break

            # Display and alert checks involve slow I/O (console redraw, a round trip
            # to chromedriver), so run them at most twice a second. That keeps the
            # time check itself running as fast as possible.
            mono = time.monotonic()
            if mono - last_housekeeping >= 0.5:
                last_housekeeping = mono
                if worker_id == 0:
                    print(
                        "\033[H\033[J"
                        f"Waiting...\nCurrent Time: {now.strftime('%B-%d-%Y %H:%M:%S')}"
                        f"\nWaiting until: {registration_time.strftime('%B-%d-%Y %H:%M:%S')}",
                        end="\r",
                        flush=True,
                    )
                accept_alert_if_present(driver)

            # Coarse sleep when far away; no sleep at all within the tight window
            if remaining > TIGHT_POLL_WINDOW:
                time.sleep(0.5)

        register_button.click()
        log(worker_id, "Registering")
        handle_waitlist(driver, wait, worker_id)

    except (TimeoutException, WebDriverException) as e:
        log(worker_id, f"Error: {type(e).__name__}: {str(e).splitlines()[0] if str(e) else ''}")


def main():
    username = input("your jhu username <jhed@jh.edu>: ")
    password = getpass("your jhu password (password will not appear on screen): ")
    registration_date = input("the date of your registration in (MM/DD/YYYY) format: ")
    authentication = input(
        "the 2FA code in your authenticator app for SIS "
        "(skip if you're using a different 2-FA method by hitting enter): "
    )

    month, day, year = (int(p) for p in registration_date.split("/"))
    # 7:00 AM registration time in your computer's local clock
    registration_time = datetime.datetime(year, month, day, 7, 0, 0)

    # Everything above happens once; from here we split into concurrent processes.
    workers = [
        Process(
            target=run_worker,
            args=(i, username, password, authentication, registration_time),
        )
        for i in range(NUM_WORKERS)
    ]
    for i, w in enumerate(workers):
        if i > 0:
            time.sleep(START_STAGGER)  # worker 1 starts 3s after worker 0, worker 2 after 6s
        w.start()
    for w in workers:
        w.join()


if __name__ == "__main__":  # required for multiprocessing on Windows/macOS
    main()
