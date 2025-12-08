from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from Base import Base

class YoutubeChannelId(Base):
    __tablename__ = 'YoutubeChannelId'

    name: Mapped[str] = mapped_column(String(255), primary_key=True)
    channelId: Mapped[str] = mapped_column(Text)
