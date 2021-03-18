from sqlalchemy import Column, Integer, String, Time, Sequence, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    UID = Column(Integer, primary_key=True)
    ChatID = Column(Integer)
    FeedTime = Column(Time)

    subscriptions = relationship("Psubscription", order_by=Feed.FID)

    def __repr__(self):
        return "<User(UID='%d', ChatID='%d')>" % (self.UID, self.ChatID)

class Feed(Base):
    __tablename__ = 'feeds'
    FID = Column(Integer, Sequence('feed_id_seq'), primary_key=True)
    URL = Column(String, unique=True)
    Type = Column(String)

class PSubscription(Base)
    __tablename__ = 'psubscriptions'
    SID = Column(Interger, Sequence('psub_id_seq'), primary_key=True)
    UID = Column(Integer, ForeignKey(User.UID))
    FID = Column(Integer, ForeignKey(Feed.FID))
    LatestCheck = Column(Time)

    user = relationship("User", back_populates="psubscriptions")
    feed = relationship("Feed")
