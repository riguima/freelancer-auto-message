from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from cray_freelas_bot.database import db

Base = declarative_base()


class BotModel(Base):
    __tablename__ = 'bots'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    report_folder: Mapped[str] = mapped_column()
    category: Mapped[str] = mapped_column()
    message: Mapped[str] = mapped_column()
    user_data_dir: Mapped[str] = mapped_column()
    browser_module: Mapped[str] = mapped_column()


Base.metadata.create_all(db)
