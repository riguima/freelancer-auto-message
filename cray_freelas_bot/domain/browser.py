from abc import ABC, abstractmethod
from datetime import datetime
from functools import cache

from cray_freelas_bot.common.driver import create_driver
from cray_freelas_bot.common.project import get_greeting_according_time
from cray_freelas_bot.domain.models import Message, Project


class IBrowser(ABC):
    """
    Interface para implementação de novos bots para outras plataformas, as classes que implementam essa interface devem conter os mesmos métodos
    """

    def __init__(
        self, user_data_dir: str = '.default_user_data', visible: bool = False
    ) -> None:
        """
        Parameters:
            user_data_dir: Caminho para pasta onde serão salvos os dados do navegador
            visible: Para mostrar ou não o navegador, por padrão é True, ou seja, mostra o navegador
        """
        self.driver = create_driver(
            user_data_dir=user_data_dir,
            visible=visible,
        )

    @abstractmethod
    def make_login(self, username: str, password: str) -> None:
        """
        Para fazer o login com o bot
        parameters:
            username: email ou nome para primeiro campo de login
            password: senha para logar
        examples:
            >>> from cray_freelas_bot.use_cases.nine_nine_freelas import nineninebrowser
            >>> from cray_freelas_bot.common.driver import create_driver
            >>>
            >>> driver = create_driver()
            >>> browser = nineninebrowser(driver)
            >>> browser.make_login('richard', '12345678')
        """
        raise NotImplementedError()

    @abstractmethod
    def is_logged(self) -> bool:
        """
        Verifica se o browser já está logado na plataforma de freelancer
        Returns:
            Retorna um booleano que responde True se está logado e False se não está logado
        """
        raise NotImplementedError()

    @abstractmethod
    def get_account_name(self) -> str:
        """
        Para obter o nome da conta, precisa para envio de mensagem ao cliente
        Returns:
            Retorna o nome da conta
        Examples:
            >>> from cray_freelas_bot.use_cases.nine_nine_freelas import NineNineBrowser
            >>> from cray_freelas_bot.common.driver import create_driver
            >>>
            >>> driver = create_driver()
            >>> browser = NineNineBrowser(driver)
            >>> browser.get_account_name()
            Richard
        """
        raise NotImplementedError()

    @abstractmethod
    def send_message(self, project_url: str, message: str) -> Message:
        """
        Para enviar a mensagem para o cliente
        Parameters:
            project_url: Url do projeto para qual ele vai fazer o envio da mensagem
            message: String que será a mensagem que vai ser enviada ao cliente
        Returns:
            Retorna uma instância da classe Message, para obter informações sobre o envio
        Examples:
            >>> from cray_freelas_bot.use_cases.nine_nine_freelas import NineNineBrowser
            >>> from cray_freelas_bot.common.driver import create_driver
            >>>
            >>> driver = create_driver()
            >>> browser = NineNineBrowser(driver)
            >>> browser.send_message('exampleurl1.com.br', 'Olá, tudo bem')
        """
        raise NotImplementedError()

    @abstractmethod
    @cache
    def get_all_categories(self) -> list[str]:
        """
        Para obter todas as categorias disponiveis do site de freelancer, útil para fazer validação e filtros
        Returns:
            Retorna a lista de todas as categorias disponiveis do site de freelancer
        Examples:
            >>> from cray_freelas_bot.use_cases.nine_nine_freelas import NineNineBrowser
            >>> from cray_freelas_bot.common.driver import create_driver
            >>>
            >>> driver = create_driver()
            >>> browser = NineNineBrowser(driver)
            >>> browser.get_all_categories()
            ['Web, Mobile & Software', 'Engenharia', 'Marketing']
        """
        raise NotImplementedError()

    @abstractmethod
    def get_projects_urls(self, category: str, page: int = 1) -> list[str]:
        """
        Para obter as urls dos projetos de uma determinada categoria e de uma determinada página
        Parameters:
            category: Uma string dizendo de qual categoria deve retornar as urls
            page: Argumento opcional, de qual página do site de freelancers que deve retornar as urls, por padrão ele pega urls da primeira página
        Returns:
            Retorna uma lista de strings que são urls dos projetos de uma determinada página e de uma determinada categoria
        Examples:
            >>> from cray_freelas_bot.use_cases.nine_nine_freelas import NineNineBrowser
            >>> from cray_freelas_bot.common.driver import create_driver
            >>>
            >>> driver = create_driver()
            >>> browser = NineNineBrowser(driver)
            >>> # Retorna os projetos da página 5
            >>> browser.get_projects_urls(category='Web, Mobile & Software', page=5)
            ['exampleurl1.com.br', 'exampleurl2.com.br', 'exampleurl3.com.br']
        """
        raise NotImplementedError()

    def get_project(self, url: str) -> Project:
        """
        Retorna uma instância da classe Project, que é referente ao projeto da url passada como parâmetro
        Parameters:
            url: Uma string que é a url do projeto
        Returns:
            Uma instância da classe Project referente ao projeto da url passada como parâmetro
        """
        raise NotImplementedError()

    def format_message(self, message: str, project: Project) -> str:
        greeting = get_greeting_according_time(datetime.now().time())
        message = message.replace('{saudação}', greeting)
        message = message.replace('{nome do cliente}', project.client_name)
        message = message.replace('{nome do projeto}', project.name)
        message = message.replace('{categoria}', project.category)
        message = message.replace('{nome da conta}', self.get_account_name())
        return message
