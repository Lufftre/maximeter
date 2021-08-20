import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import datetime
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

class WindData(Base):
    __tablename__ = 'wind'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.now)
    wind_angle = Column(Float)
    wind_speed = Column(Float)

    def __repr__(self):
        return (
            f'<Wind({self.date} - '
            f'wind_speed={self.wind_speed}, '
            f'wind_angle={self.wind_angle}>'
        )

class BoatSpeed(Base):
    __tablename__ = 'boatspeed'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.now)
    boat_speed = Column(Float)

    def __repr__(self):
        return (
            f'<BoatSpeed({self.date} - '
            f'boat_speed={self.boat_speed})>')

engine = create_async_engine(
    "postgresql+asyncpg://maxi.db",
    echo=True,
)

with engine.begin() as conn:
    # await conn.run_sync(Base.metadata.drop_all)
    conn.run_sync(Base.metadata.create_all)

# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
