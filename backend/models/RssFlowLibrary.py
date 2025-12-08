from typing import List

from sqlalchemy import CHAR, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Base import Base
from UserRssFlow import UserRssFlow



class RssFlowLibrary(Base):
    __tablename__ = 'RssFlowLibrary'

    rssFlowLibraryId: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    flowName: Mapped[str] = mapped_column(String(255))
    flowLink: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(255))
    logo: Mapped[str] = mapped_column(Text)
    domains: Mapped[str] = mapped_column(Text)

    UserRssFlow: Mapped[List['UserRssFlow']] = relationship('UserRssFlow', back_populates='RssFlowLibrary_')

