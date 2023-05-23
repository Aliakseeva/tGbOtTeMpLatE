from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.core.db.models import Base


class User(Base):
    __tablename__ = "user"

    id_: Mapped[int] = mapped_column(primary_key=True)
    registered = mapped_column(DateTime(timezone=True),
                               server_default=func.now(),
                               nullable=False,
                               )
    role: Mapped[str]
    locale: Mapped[str]

    def __repr__(self):
        str_ = f'ID: {self.id_.__str__()}:\n'
        for k, v in self.__dict__.items():
            if not k.startswith('_') and not k.endswith('_'):
                str_ += f'{k}: {v}.\n'
        return str_
