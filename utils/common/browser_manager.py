# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# def launch_browser(browser_name="chrome", options_list=None, implicit_wait=5):
#     """
#     Launch a Selenium browser with optional Chrome options and implicit wait.
#     """
#     if browser_name.lower() == "chrome":
#         chrome_options = webdriver.ChromeOptions()

#         # Apply Chrome options if given in config
#         if options_list:
#             for opt in options_list:
#                 chrome_options.add_argument(opt)

#         # Initialize Chrome driver properly
#         service = Service(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service, options=chrome_options)

#     else:
#         raise ValueError(f"Unsupported browser: {browser_name}")

#     driver.implicitly_wait(implicit_wait)
#     return driver


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def launch_browser(browser_name="chrome", chrome_options_list=None):
    options = webdriver.ChromeOptions()
    if chrome_options_list:
        for opt in chrome_options_list:
            options.add_argument(opt)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    return driver
