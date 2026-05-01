from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


chrome_options = Options()
chrome_options.add_argument("--disable-search-engine-choice-screen")

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(options=chrome_options, service=service)
driver.get("https://demoqa.com/login")

# Important elements are located using WebDriverWait to ensure they are visible before interacting with them
username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'userName')))
password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'password')))
press_login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'login')))

 
username_field.send_keys("Pyman")
password_field.send_keys("pymaster123!")
press_login.click()
driver.implicitly_wait(5)  # Wait for the page to load after clicking login

if WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'name'))).text == "Invalid username or password!":
    press_new_account = driver.find_element(By.ID, 'newUser')
    driver.execute_script("arguments[0].click();", press_new_account)  # Click "New User" using JavaScript

input("Press Enter to close the browser...")

driver.quit()