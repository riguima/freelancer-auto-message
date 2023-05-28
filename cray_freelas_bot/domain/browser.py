from abc import ABC, abstractmethod
from functools import cache

from cray_freelas_bot.domain.models import Message, Project


class IBrowser(ABC):
    """
    Interface para implementação de novos bots para outras plataformas, as classes que implementam essa interface devem conter os mesmos métodos
    """

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
