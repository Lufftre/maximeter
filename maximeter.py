#!/usr/bin/env python3
from db import Session, PolarData
from gnd10 import read_messages2


if __name__ == '__main__':
    session = Session()
    for data in read_messages2():
        datapoint = PolarData(**data)
        print(datapoint)
        session.add(datapoint)
    session.commit()

    print('Table:')
    points = session.query(PolarData).all()
    for p in points:
        print(p)
