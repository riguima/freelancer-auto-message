from functools import cache

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from slugify import slugify

from cray_freelas_bot.common.driver import (
    click,
    create_driver,
    find_element,
    find_elements,
)
from cray_freelas_bot.domain.browser import IBrowser
from cray_freelas_bot.domain.models import Message, Project
from cray_freelas_bot.exceptions.project import (
    CategoryError,
    LoginError,
    ProjectError,
    SendMessageError,
)


class NineNineBrowser(IBrowser):
    """
    Implementação de IBrowser para o site 99Freelas, os métodos são os mesmos da interface, então o modo de uso será identico
    """

    def __init__(self, user_data_dir: str, visible: bool = True) -> None:
        """
        Parameters:
            user_data_dir: Caminho para pasta onde serão salvos os dados do navegador
            visible: Para mostrar ou não o navegador, por padrão é True, ou seja, mostra o navegador
        """
        self.driver = create_driver(user_data_dir, visible=visible)

    def make_login(self, username: str, password: str) -> None:
        self.driver.delete_all_cookies()
        self.driver.get('https://www.99freelas.com.br/login')
        find_element(self.driver, '#email').send_keys(username)
        find_element(self.driver, '#senha').send_keys(password)
        while True:
            if not self.is_logged():
                errors_messages = self.driver.find_elements(
                    By.CSS_SELECTOR, '.general-error-msg'
                )
                if errors_messages and errors_messages[0].get_attribute(
                    'style'
                ):
                    raise LoginError('Email ou senha inválidos')
            else:
                break

    def is_logged(self) -> bool:
        self.driver.get('https://www.99freelas.com.br/login')
        try:
            find_element(self.driver, '.user-name')
        except TimeoutException:
            return False
        return True

    def get_account_name(self) -> str:
        self.driver.get('https://www.99freelas.com.br/dashboard')
        return find_element(self.driver, '.user-name').text

    @cache
    def get_all_categories(self) -> list[str]:
        self.driver.get('https://www.99freelas.com.br/projects')
        return [
            p.text
            for p in find_elements(
                self.driver, '.categorias-list-container .item-text'
            )
        ]

    def get_projects_urls(
        self, category: str = 'Todas as categorias', page: int = 1
    ) -> list[str]:
        if category not in self.get_all_categories():
            raise CategoryError(
                'Categoria inválida, utilize uma das seguintes: '
                f'{self.get_all_categories()}'
            )
        category = category.replace('&', 'e')
        self.driver.get(
            f'https://www.99freelas.com.br/projects?order=mais-recentes'
            f'&categoria={slugify(category)}&page={page}'
        )
        return [
            link.get_attribute('href')
            for link in find_elements(self.driver, '.title a')
        ]

    def get_project(self, url: str) -> Project:
        self.driver.get(url)
        try:
            return Project(
                client_name=find_element(
                    self.driver, '.info-usuario-nome .name'
                ).text,
                name=find_element(self.driver, '.nomeProjeto').text,
                category=find_element(self.driver, 'td').text,
                url=url,
            )
        except TimeoutException:
            if self.driver.find_elements(By.CSS_SELECTOR, '.fail'):
                raise ProjectError('O projeto não existe')
            raise ProjectError(
                'Projeto ainda não está disponivel para mandar mensagens'
            )

    def send_message(self, project_url: str, message: str) -> Message:
        self.driver.get(project_url)
        self.driver.get(
            find_element(self.driver, '.txt-duvidas a').get_attribute('href')
        )
        try:
            find_element(self.driver, '#mensagem-pergunta').send_keys(message)
        except TimeoutException:
            raise SendMessageError('Projeto não disponivel para envio de mensagens')
        click(self.driver, '#btnEnviarPergunta')
        return Message(project=self.get_project(project_url), text=message)
