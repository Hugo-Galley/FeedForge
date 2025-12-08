from typing import List

from sqlalchemy import CHAR, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Base import Base
from UserRssFlow import UserRssFlow

class Users(Base):
    __tablename__ = 'Users'

    userId: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(Text)

    UserRssFlow: Mapped[List['UserRssFlow']] = relationship('UserRssFlow', back_populates='Users_')
