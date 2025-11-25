from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


WEBSITE_URL = "http://127.0.0.1:5000"

#

def test1_handler(driver):
    if handle_javascript_alert(driver):
        print("❌ - Teste de XSS")
    else:
        print("✅ - Teste de XSS")


def test2_handler(driver):
    try:
        resultado = driver.find_element(By.TAG_NAME, "h1")
    except:
        print("✅ - Teste de SQLi")
        return
    
    welcome_message = resultado.text
    if "Bem-vindo" in welcome_message:
        print("❌ - Teste de SQLi")
    else:
        print("✅ - Teste de SQLi")


TEST_FORM_DATA = [
    # Test 1 - XSS
    {
        "name": "<script>alert('hackeado')</script>",
        "email": "aluno@teste.com",
        "password": "senha123",
        "handler": test1_handler
    },
    
    # Test 2 - SQLi
    {
        "name": "Fellipe",
        "email": "' OR 1=1; --",
        "password": "1234",
        "handler": test2_handler
    }
]

#

def handle_javascript_alert(driver, timeout=1):
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

    handle_validation(driver)


def main():
    driver = get_driver()

    try:
        # Teste 1 e 2 - XSS (Cross Site Script) e SQLi (SQL Injection)
        for data in TEST_FORM_DATA:
            test_form(
                driver, 
                data["name"], 
                data["email"], 
                data["password"], 
                data["handler"]
            )
        
        # Teste 3 - IDOR (Insecure Direct Object References)
        driver.get(f'{WEBSITE_URL}/profile/1')
        
        time.sleep(2)

        try:
            driver.find_element(By.TAG_NAME, "h1")
            print("❌ - Teste de IDOR")
        except:
            print("✅ - Teste de IDOR")

    except Exception as e:
        print(e)

    finally:
        # 4. Fechamento
        driver.quit()


if __name__ == "__main__":
    main()
