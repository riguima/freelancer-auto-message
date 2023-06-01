from sqlalchemy import select

from cray_freelas_bot.database import Session
from cray_freelas_bot.domain.bot import Bot
from cray_freelas_bot.domain.repositories import IRepository
from cray_freelas_bot.models.bot import BotModel


class BotRepository(IRepository):
    def create(self, data: Bot) -> Bot:
        with Session() as session:
            model = BotModel(
                username=data.username,
                password=data.password,
                report_folder=data.report_folder,
                category=data.category,
                message=data.message,
                user_data_dir=data.user_data_dir,
                browser_module=data.browser_module,
            )
            session.add(model)
            session.commit()
            return self.to_dataclass(model)

    def all(self) -> list[Bot]:
        with Session() as session:
            query = select(BotModel)
            models = session.execute(query).scalars().all()
            return [self.to_dataclass(m) for m in models]

    def delete(self, id: int) -> None:
        with Session() as session:
            model = session.get(BotModel, id)
            if model:
                session.delete(model)
                session.commit()

    def to_dataclass(self, model: BotModel) -> Bot:
        return Bot(
            id=model.id,
            username=model.username,
            password=model.password,
            report_folder=model.report_folder,
            category=model.category,
            message=model.message,
            user_data_dir=model.user_data_dir,
            browser_module=model.browser_module,
        )
