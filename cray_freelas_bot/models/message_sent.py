from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from cray_freelas_bot.database import db


Base = declarative_base()


class MessageSentModel(Base):
    __tablename__ = 'messages_sent'
    id: Mapped[int] = mapped_column(primary_key=True)
    account_name: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()


Base.metadata.create_all(db)
