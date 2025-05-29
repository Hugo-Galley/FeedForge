from typing import List

from sqlalchemy import CHAR, ForeignKeyConstraint, Index, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RssFlowLibrary(Base):
    __tablename__ = 'RssFlowLibrary'

    rssFlowLibraryId: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    flowName: Mapped[str] = mapped_column(String(255))
    flowLink: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(255))

    CustomRssFlow: Mapped[List['CustomRssFlow']] = relationship('CustomRssFlow', back_populates='RssFlowLibrary_')


class Users(Base):
    __tablename__ = 'Users'

    userId: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    passwd: Mapped[str] = mapped_column(Text)
    profilPicture: Mapped[str] = mapped_column(Text)

    CustomRssFlow: Mapped[List['CustomRssFlow']] = relationship('CustomRssFlow', back_populates='Users_')


class YoutubeChannelId(Base):
    __tablename__ = 'YoutubeChannelId'

    name: Mapped[str] = mapped_column(String(255), primary_key=True)
    channelId: Mapped[str] = mapped_column(Text)


class CustomRssFlow(Base):
    __tablename__ = 'CustomRssFlow'
    __table_args__ = (
        ForeignKeyConstraint(['rssFlowLibraryId'], ['RssFlowLibrary.rssFlowLibraryId'], ondelete='CASCADE', name='customrssflow_ibfk_1'),
        ForeignKeyConstraint(['userId'], ['Users.userId'], ondelete='CASCADE', name='customrssflow_ibfk_2'),
        Index('rssFlowLibraryId', 'rssFlowLibraryId'),
        Index('userId', 'userId')
    )

    customRssFlowId: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    articleTitle: Mapped[str] = mapped_column(Text)
    articlePublicationDate: Mapped[str] = mapped_column(Text)
    articleLink: Mapped[str] = mapped_column(Text)
    articleDescription: Mapped[str] = mapped_column(Text)
    articleLanguage: Mapped[str] = mapped_column(String(30))
    rssFlowLibraryId: Mapped[str] = mapped_column(CHAR(36))
    userId: Mapped[str] = mapped_column(CHAR(36))

    RssFlowLibrary_: Mapped['RssFlowLibrary'] = relationship('RssFlowLibrary', back_populates='CustomRssFlow')
    Users_: Mapped['Users'] = relationship('Users', back_populates='CustomRssFlow')
