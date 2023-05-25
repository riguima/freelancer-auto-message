from abc import ABC, abstractmethod

from cray_freelas_bot.domain.models import Message, Project


class IBrowser(ABC):
    """
    Interface para implementação de novos bots para outras plataformas, as classes que implementam essa interface devem conter os mesmos métodos
    Examples:
        >>> from cray_freelas_bot.domain.browser import IBrowser
        >>>
        >>> class FakeBrowser(IBrowser):
        >>>     def make_login(self, username: str, password: str) -> None:
        >>>         print('Fazendo login...')
        >>>
        >>>     def get_account_name(self) -> str:
        >>>         return 'Nome da conta'
        >>>
        >>>     def send_message(self, project_url: str, message: str) -> Message:
        >>>         print('Enviando mensagem')
        >>>         project = Project(
        >>>             name='Projeto 1',
        >>>             category='Web, Mobile & Software',
        >>>             url='exampleurl.com.br',
        >>>             client_name='Rogerio',
        >>>         )
        >>>         return Message(project=project, text='Ola')
        >>>
        >>>     def get_all_categories(self) -> list[str]:
        >>>         return ['Web, Mobile & Software', 'Engenharia']
        >>>
        >>>     def get_projects(self, category: str, page: int) -> list[Project]:
        >>>         projects = [
        >>>             Project(
        >>>                 name='Projeto 1',
        >>>                 category='Web, Mobile & Software',
        >>>                 url='exampleurl.com.br',
        >>>                 client_name='Rogerio',
        >>>             ),
        >>>             Project(
        >>>                 name='Projeto 2',
        >>>                 category='Engenharia',
        >>>                 url='exampleurl2.com.br',
        >>>                 client_name='Maria',
        >>>             ),
        >>>             Project(
        >>>                 name='Projeto 3',
        >>>                 category='Marketing',
        >>>                 url='exampleurl3.com.br',
        >>>                 client_name='Carlos',
        >>>             ),
        >>>         ]
        >>>         return projects
    """

    @abstractmethod
    def make_login(self, username: str, password: str) -> None:
        """
        para fazer o login com o bot
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
    def get_projects(self, category: str, page: int = 1) -> list[Project]:
        """
        Para obter todos os projetos de uma determinada categoria e de uma determinada página
        Parameters:
            category: Uma string dizendo de qual categoria deve retornar projetos
            page: Argumento opcional, de qual página do site de freelancers que deve retornar projetos, por padrão ele pega projetos da primeira página
        Returns:
            Retorna uma lista de instâncias da classe Project, que são os projetos retornados de determinada categoria e de determinada página
        Examples:
            >>> from cray_freelas_bot.use_cases.nine_nine_freelas import NineNineBrowser
            >>> from cray_freelas_bot.common.driver import create_driver
            >>>
            >>> driver = create_driver()
            >>> browser = NineNineBrowser(driver)
            >>> # Retorna os projetos da página 5
            >>> browser.get_projects(category='Web, Mobile & Software', page=5)
            [Project(name='Projeto 1', category='Web, Mobile & Software', url='exampleurl.com.br', client_name='Rogerio')]
        """
        raise NotImplementedError()
