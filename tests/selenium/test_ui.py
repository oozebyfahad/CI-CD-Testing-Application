import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

APP_URL = "http://host.docker.internal:5000"  # or http://app-container:5000 if using docker network

class TestWebAppUI(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_page_load_timeout(20)

    def tearDown(self):
        self.driver.quit()

    def test_homepage_title(self):
        """Test 1: Homepage loads and title is correct."""
        self.driver.get(APP_URL)
        self.assertIn("My Sample App", self.driver.title)

    def test_add_record_flow(self):
        """Test 2: User can add a new record via form and see it in the list."""
        self.driver.get(APP_URL)

        name_input = self.driver.find_element(By.NAME, "name")
        detail_input = self.driver.find_element(By.NAME, "detail")
        submit_btn = self.driver.find_element(By.ID, "submit-btn")

        name_input.send_keys("Test User")
        detail_input.send_keys("This is a CI/CD test record")
        submit_btn.click()

        time.sleep(2)  # small wait for DB write + reload

        rows = self.driver.find_elements(By.CSS_SELECTOR, ".record-row")
        texts = [r.text for r in rows]
        self.assertTrue(any("Test User" in t for t in texts))


if __name__ == "__main__":
    unittest.main()
