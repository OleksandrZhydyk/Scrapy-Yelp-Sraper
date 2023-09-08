from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SelenAuto:

    def __init__(self, driver_name: str, path_to_driver: str):
        self._driver_name = driver_name.capitalize()
        self.path_to_driver = path_to_driver
        self.driver = self.get_driver()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def _get_options(self):
        option_obj = getattr(webdriver, f"{self._driver_name}Options")()
        option_obj.add_argument("--window-size=1920,1080")
        option_obj.add_argument("--disable-extensions")
        option_obj.add_argument("--disable-dev-shm-usage")
        option_obj.add_argument("--disable-gpu")
        option_obj.add_argument("--no-sandbox")
        option_obj.add_argument("--headless")
        return option_obj

    def _get_driver(self):
        if hasattr(webdriver, self._driver_name):
            return getattr(webdriver, self._driver_name)
        raise AttributeError("Incorrect webdriver")

    def _get_service(self):
        return getattr(webdriver, f"{self._driver_name}Service")

    def get_driver(self):
        driver = self._get_driver()
        service = self._get_service()
        options = self._get_options()
        return driver(service=service(self.path_to_driver), options=options)

    def driver_get_page(self, page_url: str):
        return self.driver.get(page_url)

    def scroll_to_element(self, strategy: str, locator: str):
        js_code = "arguments[0].scrollIntoView();"
        element = self.driver.find_element(strategy, locator)
        self.driver.execute_script(js_code, element)

    def wait_until_element_presence(self, strategy: str, locator: str, timeout: int):
        waiter = WebDriverWait(self.driver, timeout)
        waiter.until(EC.presence_of_element_located((strategy, locator)))

    def get_page(self):
        return self.driver.page_source
