from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 1. Configuração
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # 2. Modo de Uso (Ação)
    driver.get("http://127.0.0.1:5000") # Site fictício

    # Encontra elementos (Locators)
    email_field = driver.find_element(By.ID, "user-email")
    pass_field = driver.find_element(By.ID, "user-password")
    login_button = driver.find_element(By.XPATH, "//button[text()='Entrar']")

    # Executa ações
    email_field.send_keys("aluno@teste.com")
    pass_field.send_keys("senha123")
    login_button.click()

    time.sleep(2) # Espera a página carregar (má prática, mas visual)

    # 3. Validação (Assert)
    welcome_message = driver.find_element(By.ID, "resultado").text
    assert "Bem-vindo" in welcome_message
    print("Teste de Login: SUCESSO")

except Exception as e:
    print(f"Teste de Login: FALHA - {e}")

finally:
    # 4. Fechamento
    driver.quit()
