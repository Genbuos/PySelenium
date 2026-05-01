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
password_field.send_keys("Pymaster123!")
press_login.click()
driver.implicitly_wait(5)  # Wait for the page to load after clicking login

# Check for the error message and click "New User" if the login fails

# if WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'name'))).text == "Invalid username or password!":
#     press_new_account = driver.find_element(By.ID, 'newUser')
#     driver.execute_script("arguments[0].click();", press_new_account)  # Click "New User" using JavaScript

#     # Fill out the form for creating a new user
#     first_name_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'firstname')))
#     last_name_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'lastname')))
#     username_field_new = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'userName')))
#     password_field_new = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'password')))
#     click_register = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'register')))


#     first_name_field.send_keys("Py")
#     last_name_field.send_keys("Man")
#     username_field_new.send_keys("Pyman")
#     password_field_new.send_keys("Pymaster123!")


# locate the elements dropdown and text box

elements = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div/div[1]/span/div')))
elements.click()

text_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="item-0"]/a')))
driver.execute_script("arguments[0].click();", text_box)  # Click "Text Box" using JavaScript

# Locate the form fields
full_name_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'userName')))
email_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="userEmail"]')))
current_address_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="currentAddress"]')))
permanent_address_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="permanentAddress"]')))
submit_button = driver.find_element(By.XPATH, '//*[@id="submit"]')

# Fill out the form fields
full_name_field.send_keys("PyMan Smith")
email_field.send_keys("pyman@example.com")
current_address_field.send_keys("123 Main St, New York, NY 10001")
permanent_address_field.send_keys("456 Oak Ave, Los Angeles, CA 90210")
driver.execute_script("arguments[0].click();", submit_button)  # Click "Submit" using JavaScript

input("Press Enter to close the browser...")

driver.quit()