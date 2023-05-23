from abc import ABC, abstractmethod

from cray_freelas_bot.domain.models import Message, Project


class IBrowser(ABC):
    @abstractmethod
    def make_login(self, username: str, password: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_account_name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def send_message(self, project_url: str, message: str) -> Message:
        raise NotImplementedError()

    @abstractmethod
    def get_all_categories(self) -> list[str]:
        raise NotImplementedError()

    @abstractmethod
    def get_projects(self, category: str, page: int) -> list[Project]:
        raise NotImplementedError()
