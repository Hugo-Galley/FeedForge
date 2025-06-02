from typing import List, Optional

from sqlalchemy import CHAR, ForeignKeyConstraint, Index, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class RssFlowLibrary(Base):
    __tablename__ = 'RssFlowLibrary'

    rssFlowLibraryId: Mapped[str] = mapped_column(CHAR(36, 'utf8mb4_unicode_ci'), primary_key=True)
    flowName: Mapped[str] = mapped_column(String(255, 'utf8mb4_unicode_ci'))
    flowLink: Mapped[str] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    category: Mapped[str] = mapped_column(String(255, 'utf8mb4_unicode_ci'))
    logo: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    domains: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))

    CustomRssFlow: Mapped[List['CustomRssFlow']] = relationship('CustomRssFlow', back_populates='RssFlowLibrary_')


class Users(Base):
    __tablename__ = 'Users'

    userId: Mapped[str] = mapped_column(CHAR(36, 'utf8mb4_unicode_ci'), primary_key=True)
    username: Mapped[str] = mapped_column(String(255, 'utf8mb4_unicode_ci'))
    email: Mapped[str] = mapped_column(String(255, 'utf8mb4_unicode_ci'))
    passwd: Mapped[str] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    profilPicture: Mapped[str] = mapped_column(Text(collation='utf8mb4_unicode_ci'))

    CustomRssFlow: Mapped[List['CustomRssFlow']] = relationship('CustomRssFlow', back_populates='Users_')


class YoutubeChannelId(Base):
    __tablename__ = 'YoutubeChannelId'

    name: Mapped[str] = mapped_column(String(255, 'utf8mb4_unicode_ci'), primary_key=True)
    channelId: Mapped[str] = mapped_column(Text(collation='utf8mb4_unicode_ci'))


class CustomRssFlow(Base):
    __tablename__ = 'CustomRssFlow'
    __table_args__ = (
        ForeignKeyConstraint(['rssFlowLibraryId'], ['RssFlowLibrary.rssFlowLibraryId'], ondelete='CASCADE', name='customrssflow_ibfk_1'),
        ForeignKeyConstraint(['userId'], ['Users.userId'], ondelete='CASCADE', name='customrssflow_ibfk_2'),
        Index('rssFlowLibraryId', 'rssFlowLibraryId'),
        Index('userId', 'userId')
    )

    customRssFlowId: Mapped[str] = mapped_column(CHAR(36, 'utf8mb4_unicode_ci'), primary_key=True)
    articleTitle: Mapped[str] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    articlePublicationDate: Mapped[str] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    articleLink: Mapped[str] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    articleDescription: Mapped[str] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    articleLanguage: Mapped[str] = mapped_column(String(30, 'utf8mb4_unicode_ci'))
    rssFlowLibraryId: Mapped[str] = mapped_column(CHAR(36, 'utf8mb4_unicode_ci'))
    userId: Mapped[str] = mapped_column(CHAR(36, 'utf8mb4_unicode_ci'))

    RssFlowLibrary_: Mapped['RssFlowLibrary'] = relationship('RssFlowLibrary', back_populates='CustomRssFlow')
    Users_: Mapped['Users'] = relationship('Users', back_populates='CustomRssFlow')
