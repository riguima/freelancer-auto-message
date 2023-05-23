from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
from slugify import slugify

from cray_freelas_bot.domain.browser import IBrowser
from cray_freelas_bot.domain.models import Project
from cray_freelas_bot.common.driver import find_element, find_elements, click
from cray_freelas_bot.exceptions.nine_nine_freelas import (
    UnreleasedProjectError
)


class NineNineBrowser(IBrowser):

    def __init__(self, driver: Chrome) -> None:
        self.driver = driver

    def make_login(self, username: str, password: str) -> bool:
        self.driver.get('https://www.99freelas.com.br/login')
        find_element(self.driver, '#email').send_keys(username)
        find_element(self.driver, '#senha').send_keys(password)
        for i in range(60):
            if self.is_logged():
                return True
            sleep(1)
        return False

    def is_logged(self) -> bool:
        try:
            find_element(self.driver, '.user-name')
        except TimeoutException:
            return False
        return True

    def get_account_name(self) -> str:
        self.driver.get('https://www.99freelas.com.br/dashboard')
        return find_element(self.driver, '.user-name').text

    def get_all_categories(self) -> list[str]:
        self.driver.get('https://www.99freelas.com.br/projects')
        return [p.text for p in find_elements(
            self.driver, '.categorias-list-container .item-text'
        )]

    def get_projects(self, category: str = 'Todas as categorias', page: int = 1) -> list[Project]:
        if category not in self.get_all_categories():
            raise ValueError('Invalid category.')
        fixed_category = category.replace('&', 'e')
        self.driver.get(
            f'https://www.99freelas.com.br/projects?order=mais-recentes&categoria={slugify(fixed_category)}&page={page}'
        )
        urls = [
            link.get_attribute('href') for link in
            find_elements(self.driver, '.title a')
        ]
        return [self.get_project(url) for url in urls]

    def get_project(self, url: str) -> Project:
        self.driver.get(url)
        try:
            return Project(
                client_name=find_element(self.driver, '.info-usuario-nome .name').text,
                name=find_element(self.driver, '.nomeProjeto').text,
                category=find_element(self.driver, 'td').text,
                url=url,
            )
        except TimeoutException:
            if self.driver.find_elements(By.CSS_SELECTOR, '.fail'):
                raise ValueError('O projeto não existe')
            raise UnreleasedProjectError()

    def send_message(self, project_url: str, message: str) -> None:
        self.driver.get(project_url)
        self.driver.get(
            find_element(self.driver, '.txt-duvidas a').get_attribute('href')
        )
        find_element(self.driver, '#mensagem-pergunta').send_keys(message)
        click(self.driver, '#btnEnviarPergunta')

    def get_last_message(self) -> str:
        self.driver.get('https://www.99freelas.com.br/messages/inbox')
        return find_elements(
            self.driver, '.message-text:not(.empty)'
        )[-1].text
