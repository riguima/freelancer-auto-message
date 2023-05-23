from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def create_driver(visible: bool = False) -> Chrome:
    options = Options()
    if not visible:
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
    return Chrome(
        options=options, service=Service(ChromeDriverManager().install())
    )


def click(driver: Chrome, selector: str, **kwargs) -> None:
    driver.execute_script(
        'arguments[0].click();',
        find_element(kwargs.get('element', driver), selector),
    )


def find_element(driver: Chrome, selector: str, wait: int = 20):
    return WebDriverWait(driver, wait).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )


def find_elements(driver: Chrome, selector: str, wait: int = 20):
    return WebDriverWait(driver, wait).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )
