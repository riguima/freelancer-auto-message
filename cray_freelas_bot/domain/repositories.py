from abc import ABC, abstractmethod

from cray_freelas_bot.domain.bot import Bot


class IRepository(ABC):
    @abstractmethod
    def create(self, data: Bot) -> Bot:
        raise NotImplementedError()

    @abstractmethod
    def all(self) -> list[Bot]:
        raise NotImplementedError()

    def delete(self, id: int) -> None:
        raise NotImplementedError()
