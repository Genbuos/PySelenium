from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import json

class WebAutomation:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-search-engine-choice-screen")
        
        download_path = os.getcwd()
        prefs = {
            "download.default_directory": download_path,}
        chrome_options.add_experimental_option("prefs", prefs)


        service = Service(ChromeDriverManager().install())

        self.driver = webdriver.Chrome(options=chrome_options, service=service)

    def login(self, username, password):
        self.driver.get("https://demoqa.com/login")

        # Important elements are located using WebDriverWait to ensure they are visible before interacting with them
        username_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'userName')))
        password_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'password')))
        press_login = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'login')))

        
        username_field.send_keys(username)
        password_field.send_keys(password)
        press_login.click()

    
    def complete_textbox(self, fullname, email, current_address, permanent_address):
        elements = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div/div[1]/span/div')))
        elements.click()

        text_box = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="item-0"]/a')))
        self.driver.execute_script("arguments[0].click();", text_box)  # Click "Text Box" using JavaScript

        # Locate the form fields
        full_name_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'userName')))
        email_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="userEmail"]')))
        current_address_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="currentAddress"]')))
        permanent_address_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="permanentAddress"]')))
        submit_button = self.driver.find_element(By.XPATH, '//*[@id="submit"]')

        # Fill out the form fields and submit the form
        full_name_field.send_keys(fullname)
        email_field.send_keys(email)
        current_address_field.send_keys(current_address)
        permanent_address_field.send_keys(permanent_address)
        self.driver.execute_script("arguments[0].click();", submit_button)  # Click "Submit" using JavaScript

        def get_all_xpaths(self):
            """Extract all XPaths and element info from the page"""
            script = """
            function getElementXPath(element) {
                if (element.id !== '')
                    return "//*[@id='" + element.id + "']";
                if (element === document.body)
                    return "//" + element.tagName.toLowerCase();
                
                var ix = 0;
                var siblings = element.parentNode.childNodes;
                for (var i = 0; i < siblings.length; i++) {
                    var sibling = siblings[i];
                    if (sibling === element)
                        return getElementXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
                    if (sibling.nodeType === 1 && sibling.tagName.toLowerCase() === element.tagName.toLowerCase())
                        ix++;
                }
            }
            
            var elements = [];
            document.querySelectorAll('*').forEach(function(el) {
                elements.push({
                    tag: el.tagName,
                    id: el.id || 'N/A',
                    class: el.className || 'N/A',
                    xpath: getElementXPath(el),
                    text: (el.innerText || '').substring(0, 50),
                    clickable: el.onclick !== null || el.tagName.match(/button|a|input/i)
                });
            });
            return elements;
            """
            
            elements = self.driver.execute_script(script)
            return elements

    def get_interactive_elements(self):
        """Get only clickable/interactive elements (buttons, links, inputs)"""
        script = """
        function getElementXPath(element) {
            if (element.id !== '')
                return "//*[@id='" + element.id + "']";
            if (element === document.body)
                return "//" + element.tagName.toLowerCase();
            
            var ix = 0;
            var siblings = element.parentNode.childNodes;
            for (var i = 0; i < siblings.length; i++) {
                var sibling = siblings[i];
                if (sibling === element)
                    return getElementXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
                if (sibling.nodeType === 1 && sibling.tagName.toLowerCase() === element.tagName.toLowerCase())
                    ix++;
            }
        }
        
        var interactive = [];
        document.querySelectorAll('button, a, input, select, textarea, [onclick]').forEach(function(el) {
            interactive.push({
                tag: el.tagName,
                id: el.id || 'N/A',
                text: (el.innerText || el.value || el.placeholder || '').substring(0, 50),
                xpath: getElementXPath(el)
            });
        });
        return interactive;
        """
        
        return self.driver.execute_script(script)

    def save_xpaths_to_file(self, filename="xpaths.json", interactive_only=False):
        """Save extracted XPaths to a JSON file"""
        if interactive_only:
            elements = self.get_interactive_elements()
        else:
            elements = self.get_all_xpaths()
        
        with open(filename, "w") as f:
            json.dump(elements, f, indent=2)
        
        print(f"Saved {len(elements)} elements to {filename}")
        return elements

    def check_box_list(self):
        # Locate the Check box list element and click it
        check_box_list = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="item-1"]/a')))
        self.driver.execute_script("arguments[0].click();", check_box_list)  # Click "Check Box List" using JavaScript

        check_box = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'rc-tree-checkbox')))
        self.driver.execute_script("arguments[0].click();", check_box)

    def radio_button_list(self): 
        # locate the next item in the list and click it
        radio_button_list = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="item-2"]/a')))
        self.driver.execute_script("arguments[0].click();", radio_button_list)

        # locate the radio button and click it
        radio_button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'yesRadio')))
        self.driver.execute_script("arguments[0].click();", radio_button)

    # TODO [SCRUM-20]: add logic to export data from web tables into a xls file 
    def web_tables(self):
        web_tables = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="item-3"]/a')))
        self.driver.execute_script("arguments[0].click();", web_tables)


    def download(self):
        # Locate the Download item and click it
        download = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="item-7"]/a')))
        self.driver.execute_script("arguments[0].click();", download)

        #click the button
        download_button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'downloadButton')))
        self.driver.execute_script("arguments[0].click();", download_button)

    def close(self):
        self.driver.quit()

web_automation = WebAutomation()



if __name__ == "__main__":
    # data for functions
    web_automation.login("pyman", "Pymaster123!")
    web_automation.save_xpaths_to_file("all_xpaths.json", interactive_only=False)
    # Extract and save only interactive elements
    web_automation.save_xpaths_to_file("interactive_elements.json", interactive_only=True)
    web_automation.complete_textbox("PyMan Smith", "pyman@example.com", "123 Main St, New York, NY 10001", "456 Oak Ave, Los Angeles, CA 90210")
    web_automation.check_box_list()
    web_automation.radio_button_list()
    web_automation.web_tables()
    web_automation.download()
    web_automation.close()
