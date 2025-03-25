# flake8: noqa: E501
import os
import dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

dotenv.load_dotenv()
USERNAME = os.getenv("DEMOQA_USERNAME")
PASSWORD = os.getenv("DEMOQA_PASSWORD")


class WebAutomation:
    """
    Class for automating web tasks.
    """

    def __init__(self) -> None:
        """
        Initialize the WebAutomation class.
        """
        # Set up Chrome WebDriver
        self._chrome_options = Options()
        self._chrome_options.add_argument(
            "--disable-search-engine-choice-screen")

        # Create absolute path for downloads directory
        self._download_path = os.path.join(
            os.path.abspath(os.getcwd()), "downloads")
        # Create directory if it doesn't exist
        os.makedirs(self._download_path, exist_ok=True)
        # Normalize the path (converts forward slashes to backslashes on Windows)
        self._download_path = os.path.normpath(self._download_path)

        self._prefs = {
            "download.default_directory": self._download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "safebrowsing.disable_download_protection": False,
            "download.open_pdf_in_system_reader": False,
        }
        self._chrome_options.add_experimental_option('prefs', self._prefs)

        self._service = Service("chromedriver-win64\chromedriver.exe")
        self._driver = webdriver.Chrome(
            options=self._chrome_options, service=self._service)

        # Load the webpage
        self._driver.get("https://demoqa.com/login")

    def login(self, username: str, password: str) -> None:
        """
        Login to the website.

        Arguments:
            username -- The username to use for login.
            password -- The password to use for login.
        """
        # Locate username, password fields and login button
        self.username_field = WebDriverWait(self._driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'userName')))
        self.password_field = WebDriverWait(self._driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'password')))
        self.login_button = self._driver.find_element(By.ID, 'login')

        # Fill in username and password
        self.username_field.send_keys(username)
        self.password_field.send_keys(password)
        self._driver.execute_script("arguments[0].click();", self.login_button)

    def fill_form(self, fullname: str, email: str, current_address: str,
                  permanent_address: str) -> None:
        """
        Fill in a form.
        """
        # Locate the Elements dropdown and Text Box option
        elements_dropdown = WebDriverWait(self._driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div[1]/div/div/div[1]/span/div')))  # noqa E501
        elements_dropdown.click()

        text_box_option = WebDriverWait(self._driver, 10).until(
            EC. visibility_of_element_located((By.ID, 'item-0')))
        text_box_option.click()

        # Locate the form fields and submit button
        fullname_field = WebDriverWait(self._driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'userName')))
        email_field = WebDriverWait(self._driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'userEmail')))
        current_address_field = WebDriverWait(self._driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'currentAddress')))
        permanent_address_field = WebDriverWait(self._driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'permanentAddress')))
        submit_button = self._driver.find_element(By.ID, 'submit')

        # Fill in the form fields
        fullname_field.send_keys(fullname)
        email_field.send_keys(email)
        current_address_field.send_keys(current_address)
        permanent_address_field.send_keys(permanent_address)

        # Submit the form
        submit_button.click()

    def download(self) -> None:
        """
        Download a file.
        """
        # Locate the Upload and Download sections and the Download button
        upload_section = WebDriverWait(self._driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'item-7')))
        self._driver.execute_script("arguments[0].click();", upload_section)
        download_button = self._driver.find_element(By.ID, 'downloadButton')
        self._driver.execute_script("arguments[0].click();", download_button)

    def close(self) -> None:
        """
        Close the browser.
        """
        self._driver.quit()


if __name__ == "__main__":
    automation = WebAutomation()
    automation.login(USERNAME, PASSWORD)
    automation.fill_form("John Doe", "johndoe@example.com",
                         "123 Main St, City, Country",
                         "456 Elm St, City, Country")
    automation.download()
    automation.close()
