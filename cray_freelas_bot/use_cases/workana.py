from functools import cache
from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from cray_freelas_bot.common.driver import click, find_element, find_elements
from cray_freelas_bot.domain.browser import IBrowser
from cray_freelas_bot.domain.models import Message, Project
from cray_freelas_bot.exceptions.project import (
    CategoryError,
    LoginError,
    ProjectError,
)


class WorkanaBrowser(IBrowser):
    """
    Implementação de IBrowser para o site Workana, os métodos são os mesmos da interface, então o modo de uso será identico
    """


    def __str__(self) -> str:
        return 'workana'

    def make_login(self, username: str, password: str) -> None:
        self.driver.get('https://www.workana.com/login')
        find_element(self.driver, 'input[name=email]').send_keys(username)
        find_element(self.driver, 'input[name=password]').send_keys(password)
        click(self.driver, 'button[type=submit]')
        if not self.is_logged():
            raise LoginError('Email ou senha inválidos')

    def is_logged(self) -> bool:
        url = 'https://www.workana.com/login'
        if self.driver.current_url != url:
            self.driver.get(url)
        try:
            find_element(self.driver, '.user-info')
        except TimeoutException:
            return False
        return True

    def get_account_name(self) -> str:
        self.driver.get('https://www.workana.com/dashboard')
        return find_element(
            self.driver,
            '.user-name span',
        ).get_attribute('textContent')

    @cache
    def get_all_categories(self) -> list[str]:
        self.driver.get('https://www.workana.com/jobs?language=pt')
        return [
            p.get_attribute('textContent')
            for p in find_elements(self.driver, 'span.is-disabled')
        ]

    def get_projects_urls(
        self, category: str = 'Todas as categorias', page: int = 1
    ) -> list[str]:
        if category not in self.get_all_categories():
            raise CategoryError(
                'Categoria inválida, utilize uma das seguintes: '
                f'{self.get_all_categories()}'
            )
        self.driver.get('https://www.workana.com/jobs?language=pt')
        click(self.driver, '#category-')
        checkbox = find_elements(
            self.driver,
            '.search-category input[type=checkbox]',
        )[self.get_all_categories().index(category)]
        self.driver.execute_script('arguments[0].click();', checkbox)
        self.driver.get(self.driver.current_url + f'?page={page}')
        sleep(5)
        return [
            link.get_attribute('href')
            for link in find_elements(self.driver, '.project-title a')
        ]

    def get_project(self, url: str) -> Project:
        self.driver.get(url)
        try:
            return Project(
                client_name=find_element(
                    self.driver, '.user-name span'
                ).get_attribute('textContent'),
                name=find_element(self.driver, '#productName .title').text,
                category=find_elements(self.driver, 'b')[1].get_attribute(
                    'textContent'
                ),
                url=url,
            )
        except TimeoutException:
            if self.driver.find_elements(By.CSS_SELECTOR, '.error-section'):
                raise ProjectError('O projeto não existe')

    def send_message(self, project_url: str, message: str) -> Message:
        self.driver.get(project_url)
        click(self.driver, '#message_button')
        find_element(
            self.driver,
            'textarea[name="message[content]"]',
        ).send_keys(message)
        button = find_elements(self.driver, 'input[type=submit]')[-1]
        self.driver.execute_script('arguments[0].click();', button)
        project = self.get_project(project_url)
        return Message(
            project=project,
            text=self.format_message(message, project),
        )
