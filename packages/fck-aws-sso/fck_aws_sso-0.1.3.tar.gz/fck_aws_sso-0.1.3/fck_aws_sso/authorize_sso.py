from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

def build_driver(headless=True):
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    user_data_dir = Path.home() / ".cache" / "fck_aws_sso" / "user_data"
    options.add_argument(f"user-data-dir={user_data_dir}")
    if headless:
        options.add_argument("headless")
    return webdriver.Chrome(service=service, options=options)

def authorize_sso(url, code, headless=True):
    driver = build_driver(headless)
    url_with_code = f"{url}?user_code={code}"
    driver.get(url_with_code)
    print("opening the page")

    try:
        print("waiting for the page to load")
        submit_button = WebDriverWait(driver, 1000).until(
            EC.element_to_be_clickable((By.ID, "cli_verification_btn"))
        )
        print("clicking on the verification button")
        submit_button.click()

        print("waiting for the login page to load")
        login_button = WebDriverWait(driver, 1000).until(
            EC.element_to_be_clickable((By.ID, "cli_login_button"))
        )
        print("clicking on the allow button")
        login_button.click()

        print("waiting for confirmation page to load")
        WebDriverWait(driver, 1000).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "You may now close this browser.")
        )


    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()