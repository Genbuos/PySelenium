import tkinter as tk
from tkinter import ttk, messagebox
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AutomationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Selenium Automation GUI")
        self.root.geometry("800x600")
        
        self.driver = None
        self.elements_data = []

        # Config button
        config_btn = tk.Button(root, text="Configure Automation", command=self.open_config)
        config_btn.pack(pady=10)
        
        # Start session button (FIRST - navigate to site)
        start_btn = tk.Button(root, text="Scrape Current Page Elements", command=self.start_session)
        start_btn.pack(pady=10)

        
        
        # Load button (load from JSON)
        load_btn = tk.Button(root, text="Load Elements from File", command=self.load_elements)
        load_btn.pack(pady=5)
        
        # Treeview to display elements
        self.tree = ttk.Treeview(root, columns=("Tag", "ID", "Text", "XPath"), height=15)
        self.tree.column("#0", width=50)
        self.tree.column("Tag", width=60)
        self.tree.column("ID", width=150)
        self.tree.column("Text", width=200)
        self.tree.column("XPath", width=300)
        
        self.tree.heading("#0", text="Index")
        self.tree.heading("Tag", text="Tag")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Text", text="Text")
        self.tree.heading("XPath", text="XPath")
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Click button
        click_btn = tk.Button(root, text="Click Selected Element", command=self.click_element)
        click_btn.pack(pady=5)
        
        # Close browser button
        close_btn = tk.Button(root, text="Close Browser", command=self.close_browser)
        close_btn.pack(pady=5)
        
        # Run automation button
        run_auto_btn = tk.Button(root, text="Run Full Automation", command=self.run_automation)
        run_auto_btn.pack(pady=10)
    
    def start_session(self):
        """Scrape elements from the current page (browser must be running)"""
        if not self.driver:
            messagebox.showwarning("Warning", "No active browser session. Run automation first or open a browser manually.")
            return
        
        try:
            # Scrape elements from current page
            self.scrape_elements()
            messagebox.showinfo("Success", "Elements scraped and loaded into table!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scrape elements: {str(e)}")
    
    def scrape_elements(self):
        """Extract elements from current page and save to JSON"""
        try:
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
            
            self.elements_data = self.driver.execute_script(script)
            
            # Save to file
            with open("interactive_elements.json", "w") as f:
                json.dump(self.elements_data, f, indent=2)
            
            # Display in treeview
            self.display_elements()
            messagebox.showinfo("Success", f"Scraped and saved {len(self.elements_data)} elements")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scrape elements: {str(e)}")
    
    def display_elements(self):
        """Display elements in treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add elements
        for i, element in enumerate(self.elements_data):
            self.tree.insert("", "end", text=str(i), values=(
                element.get("tag", ""),
                element.get("id", "N/A"),
                element.get("text", ""),
                element.get("xpath", "")
            ))
    
    def load_elements(self):
        """Load elements from JSON file"""
        try:
            with open("interactive_elements.json", "r") as f:
                self.elements_data = json.load(f)
            
            self.display_elements()
            messagebox.showinfo("Success", f"Loaded {len(self.elements_data)} elements")
        except FileNotFoundError:
            messagebox.showerror("Error", "interactive_elements.json not found. Click 'Start Session & Scrape Elements' first")
    
    def click_element(self):
        """Click the selected element in the browser"""
        if not self.driver:
            messagebox.showwarning("Warning", "No browser session. Click 'Start Session' first")
            return
        
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an element first")
            return
        
        try:
            index = int(self.tree.item(selected[0])['text'])
            element = self.elements_data[index]
            xpath = element.get("xpath")
            
            elem = self.driver.find_element("xpath", xpath)
            elem.click()
            messagebox.showinfo("Success", f"Clicked: {element.get('text', 'Element')}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not click element: {str(e)}")
    
    def close_browser(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            messagebox.showinfo("Info", "Browser closed")
    
    def open_config(self):
        """Open configuration window"""
        config_window = tk.Toplevel(self.root)
        config_window.title("Automation Configuration")
        config_window.geometry("500x600")
        
        # Load existing config if available
        try:
            with open("automation_config.json", "r") as f:
                config_data = json.load(f)
        except FileNotFoundError:
            config_data = {
                "login": {"username": "pyman", "password": "Pymaster123!"},
                "textbox": {
                    "fullname": "PyMan Smith",
                    "email": "pyman@example.com",
                    "current_address": "123 Main St, New York, NY 10001",
                    "permanent_address": "456 Oak Ave, Los Angeles, CA 90210"
                }
            }
        
        # Create scrollable frame
        canvas = tk.Canvas(config_window)
        scrollbar = ttk.Scrollbar(config_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Login Section
        ttk.Label(scrollable_frame, text="Login Credentials", font=("Arial", 12, "bold")).pack(pady=10)
        
        ttk.Label(scrollable_frame, text="Username:").pack()
        username_var = tk.StringVar(value=config_data["login"]["username"])
        ttk.Entry(scrollable_frame, textvariable=username_var, width=40).pack()
        
        ttk.Label(scrollable_frame, text="Password:").pack()
        password_var = tk.StringVar(value=config_data["login"]["password"])
        ttk.Entry(scrollable_frame, textvariable=password_var, show="*", width=40).pack()
        
        # TextBox Section
        ttk.Label(scrollable_frame, text="TextBox Form Data", font=("Arial", 12, "bold")).pack(pady=10)
        
        ttk.Label(scrollable_frame, text="Full Name:").pack()
        fullname_var = tk.StringVar(value=config_data["textbox"]["fullname"])
        ttk.Entry(scrollable_frame, textvariable=fullname_var, width=40).pack()
        
        ttk.Label(scrollable_frame, text="Email:").pack()
        email_var = tk.StringVar(value=config_data["textbox"]["email"])
        ttk.Entry(scrollable_frame, textvariable=email_var, width=40).pack()
        
        ttk.Label(scrollable_frame, text="Current Address:").pack()
        current_addr_var = tk.StringVar(value=config_data["textbox"]["current_address"])
        ttk.Entry(scrollable_frame, textvariable=current_addr_var, width=40).pack()
        
        ttk.Label(scrollable_frame, text="Permanent Address:").pack()
        permanent_addr_var = tk.StringVar(value=config_data["textbox"]["permanent_address"])
        ttk.Entry(scrollable_frame, textvariable=permanent_addr_var, width=40).pack()
        
        # Save button
        def save_config():
            new_config = {
                "login": {
                    "username": username_var.get(),
                    "password": password_var.get()
                },
                "textbox": {
                    "fullname": fullname_var.get(),
                    "email": email_var.get(),
                    "current_address": current_addr_var.get(),
                    "permanent_address": permanent_addr_var.get()
                }
            }
            
            with open("automation_config.json", "w") as f:
                json.dump(new_config, f, indent=2)
            
            messagebox.showinfo("Success", "Configuration saved to automation_config.json")
            config_window.destroy()
        
        ttk.Button(scrollable_frame, text="Save Configuration", command=save_config).pack(pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def run_automation(self):
        """Run the full automation workflow using saved config"""
        try:
            # Load config
            with open("automation_config.json", "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "Config file not found. Click 'Configure Automation' first")
            return
        
        try:
            # Import WebAutomation from main.py
            from main import WebAutomation
            
            # Create automation instance
            automation = WebAutomation()
            
            # Run the workflow
            messagebox.showinfo("Starting", "Automation workflow starting...")
            
            automation.login(
                config["login"]["username"], 
                config["login"]["password"]
            )
            messagebox.showinfo("Step 1", "Login complete")
            
            automation.complete_textbox(
                config["textbox"]["fullname"],
                config["textbox"]["email"],
                config["textbox"]["current_address"],
                config["textbox"]["permanent_address"]
            )
            messagebox.showinfo("Step 2", "TextBox complete")
            
            automation.check_box_list()
            messagebox.showinfo("Step 3", "CheckBox complete")
            
            automation.radio_button_list()
            messagebox.showinfo("Step 4", "RadioButton complete")
            
            automation.web_tables()
            messagebox.showinfo("Step 5", "WebTables complete")
            
            automation.download()
            messagebox.showinfo("Step 6", "Download complete")
            
            automation.close()
            messagebox.showinfo("Success", "Automation workflow completed!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Automation failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = AutomationGUI(root)
    root.mainloop()
