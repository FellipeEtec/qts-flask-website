from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


WEBSITE_URL = "http://127.0.0.1:5000"

TEST_FORM_DATA = [
    # Test 1
    {
        "name": "<script>alert('hackeado')</script>",
        "email": "aluno@teste.com",
        "password": "senha123",
        "handler": lambda: handle_javascript_alert()
    },
    
    # # Test 2
    # {
    #     "name": "",
    #     "email": "",
    #     "password": "",
    #     "handler": lambda x: print()
    # },
    
    # # Test 3
    # {
    #     "name": "",
    #     "email": "",
    #     "password": "",
    #     "handler": lambda x: print()
    # }
]


def handle_javascript_alert(driver, timeout=10):
    try:
        wait = WebDriverWait(driver, timeout)
        alert = wait.until(EC.alert_is_present())
        alert.accept() 
        return True

    except TimeoutException:
        return False
    except NoAlertPresentException:
        return False


def get_driver():
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


def test_form(driver, name_input, email_input, password_input, handle_validation):
    driver.get(WEBSITE_URL)

    name_field = driver.find_element(By.ID, "user-name")
    email_field = driver.find_element(By.ID, "user-email")
    pass_field = driver.find_element(By.ID, "user-password")
    login_button = driver.find_element(By.XPATH, "//button[text()='Entrar']")

    name_field.send_keys(name_input)
    email_field.send_keys(email_input)
    pass_field.send_keys(password_input)
    login_button.click()

    time.sleep(2)

    return handle_validation()


def main():
    driver = get_driver()

    try:
        for data in TEST_FORM_DATA:
            error = test_form(
                driver, 
                data["name"], 
                data["email"], 
                data["password"], 
                data["handler"]
            )

            if error:
                raise Exception(error)

    except Exception as e:
        print(f"Teste de Login: FALHA - {e}")

    finally:
        # 4. Fechamento
        driver.quit()


if __name__ == "__main__":
    main()
