from sqlalchemy import CHAR, ForeignKeyConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Users import Users
from RssFlowLibrary import RssFlowLibrary
from Base import Base

class UserRssFlow(Base):
    __tablename__ = 'UserRssFlow'
    __table_args__ = (
        ForeignKeyConstraint(['rssFlowLibrairyId'], ['RssFlowLibrary.rssFlowLibraryId'], ondelete='CASCADE', name='userrssflow_ibfk_1'),
        ForeignKeyConstraint(['userId'], ['Users.userId'], ondelete='CASCADE', name='userrssflow_ibfk_2'),
        Index('rssFlowLibrairyId', 'rssFlowLibrairyId'),
        Index('userId', 'userId')
    )

    customRssFlowId: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    rssFlowLibrairyId: Mapped[str] = mapped_column(CHAR(36))
    userId: Mapped[str] = mapped_column(CHAR(36))

    RssFlowLibrary_: Mapped['RssFlowLibrary'] = relationship('RssFlowLibrary', back_populates='UserRssFlow')
    Users_: Mapped['Users'] = relationship('Users', back_populates='UserRssFlow')
