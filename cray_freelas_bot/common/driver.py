from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def create_driver(visible: bool = False) -> Chrome:
    """
    Cria um driver do Google Chrome do selenium
    Parameters:
        visible: Opção para mostrar ou não o navegador, por padrão é False, ou seja, não visivel
    Returns:
        Retorna uma instância do driver Chrome do selenium
    """
    options = Options()
    if not visible:
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
    return Chrome(
        options=options, service=Service(ChromeDriverManager().install())
    )


def click(driver: Chrome, selector: str, element=None) -> None:
    """
    Clica em um elemento da página
    Parameters:
        driver: Driver do Chrome do selenium
        selector: Seletor css que identifica o elemento que será clicado
        element: Argumento opcional, define a partir de qual elemento ele deve fazer a busca do elemento especificado em selector
    Examples:
        >>> from cray_freelas_bot.common.driver import (
                create_driver,
                click,
                find_element,
            )
        >>>
        >>> driver = create_driver()
        >>> click(driver, 'button[type=submit]')
        >>>
        >>> form = find_element(driver, 'form')
        >>> # Vai clicar no primeiro elemento button com type submit que está dentro do form
        >>> click(driver, 'button[type=submit]', element=form)
    """
    if element is None:
        element = driver
    driver.execute_script(
        'arguments[0].click();',
        find_element(element, selector),
    )


def find_element(element, selector: str, wait: int = 20):
    """
    Procura por um elemento na página, caso não encontre gera uma exceção
    Parameters:
        element: A partir de qual elemento ele deve fazer a busca do elemento especificado em selector
        selector: Seletor css que identifica o elemento que será buscado
        wait: Argumento opcional, quantidade de tempo em segundos que ele deve esperar para encontrar o elemento, caso ultrapasse esse tempo ele vai retornar um erro do tipo selenium.common.exceptions.TimeoutException, por padrão ele espera por 20 segundos
    Returns:
        Retorna o primeiro elemento com seletor especificado
    Examples:
        >>> from cray_freelas_bot.common.driver import (
                create_driver,
                find_element,
            )
        >>>
        >>> driver = create_driver()
        >>> # Procura pelo primeiro elemento com tag a dentro de uma div
        >>> link = find_element(driver, 'div a')
        >>>
        >>> form = find_element(driver, 'form')
        >>> # Procura o primeiro elemento com tag a, dentro de uma div que está dentro de um form
        >>> # Ele espera por 10 segundos pelo elemento
        >>> link = find_element(form, 'div a', wait=10)
    """
    return WebDriverWait(element, wait).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )


def find_elements(element, selector: str, wait: int = 20):
    """
    O mesmo que find_element, mas procura por todos os elementos correspondentes ao seletor
    Parameters:
        element: A partir de qual elemento ele deve fazer a busca dos elementos especificado em selector
        selector: Seletor css que identifica os elementos que serão buscados
        wait: Argumento opcional, quantidade de tempo em segundos que ele deve esperar para encontrar os elementos, caso ultrapasse esse tempo ele vai retornar um erro do tipo selenium.common.exceptions.TimeoutException, por padrão ele espera por 20 segundos
    Returns:
        Retorna todos os elementos que correspondem ao seletor especificado
    Examples:
        >>> from cray_freelas_bot.common.driver import (
                create_driver,
                find_element,
                find_elements,
            )
        >>>
        >>> driver = create_driver()
        >>> # Procura por todas as div da página
        >>> divs = find_elements(driver, 'div')
        >>>
        >>> form = find_element(driver, 'form')
        >>> # Procura por todas as divs que estão dentro de form
        >>> # Ele espera por 10 segundos pelo elemento
        >>> divs = find_elements(form, 'div', wait=10)
    """
    return WebDriverWait(element, wait).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )
