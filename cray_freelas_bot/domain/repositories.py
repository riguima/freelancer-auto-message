from abc import ABC, abstractmethod
from typing import Union

from cray_freelas_bot.domain.bot import Bot
from cray_freelas_bot.domain.message_sent import MessageSent


class IRepository(ABC):
    @abstractmethod
    def create(self, data: Union[Bot, MessageSent]) -> Union[Bot, MessageSent]:
        raise NotImplementedError()

    @abstractmethod
    def all(self) -> list[Union[Bot, MessageSent]]:
        raise NotImplementedError()

    def delete(self, id: int) -> None:
        raise NotImplementedError()
