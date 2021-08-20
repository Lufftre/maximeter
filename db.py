from sqlalchemy import create_engine
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///maxi.db')
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
            f'boat_speed={self.boat_speed})>'
        )


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def insert_speed(session, speed):
    print('add', speed)
    session.add(BoatSpeed(boat_speed=speed))
    session.commit()


def insert_wind(session, wind):
    print('add', wind)
    session.add(WindData(wind_angle=wind, wind_speed=wind))
    session.commit()


if __name__ == '__main__':
    session = Session()
    # datapoint = PolarData(wind_angle=45.1234, wind_speed=8.123, boat_speed=6.523)
    # session.add(datapoint)
    # session.commit()
    points = session.query(BoatSpeed).all()
    for p in points:
        print(p)
