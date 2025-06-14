import time
import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from forwarder import extract_sms

def wait_for_login(driver, timeout=180):
    print("[*] Waiting for manual login...")
    start = time.time()
    while time.time() - start < timeout:
        time.sleep(2)
        if "Logout" in driver.page_source:
            print("[✅] Login successful!")
            return True
    print("[❌] Login timeout!")
    return False

def main():
    print("[*] Launching Chrome browser...")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get(config.LOGIN_URL)

    if not wait_for_login(driver):
        driver.quit()
        return

    print("[*] Starting SMS monitoring...")
    while True:
        try:
            extract_sms(driver)
            time.sleep(2)
        except Exception as e:
            print(f"[ERR] {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
