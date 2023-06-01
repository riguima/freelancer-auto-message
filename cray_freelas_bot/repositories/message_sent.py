from sqlalchemy import select

from cray_freelas_bot.domain.message_sent import MessageSent
from cray_freelas_bot.domain.repositories import IRepository
from cray_freelas_bot.models.message_sent import MessageSentModel
from cray_freelas_bot.database import Session


class MessageSentRepository(IRepository):
    def create(self, data: MessageSent) -> MessageSent:
        with Session() as session:
            model = MessageSentModel(url=data.url)
            session.add(model)
            session.commit()
            return self.to_dataclass(model)

    def all(self) -> list[MessageSent]:
        with Session() as session:
            query = select(MessageSentModel)
            models = session.execute(query).scalars().all()
            return [self.to_dataclass(m) for m in models]

    def delete(self, id: int) -> None:
        with Session() as session:
            model = session.get(MessageSentModel, id)
            if model:
                session.delete(model)
                session.commit()

    def to_dataclass(self, model: MessageSentModel) -> MessageSent:
        return MessageSent(
            id=model.id,
            url=model.url,
        )
