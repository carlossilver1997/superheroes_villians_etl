import argparse
import logging

import pandas as pd
from hero import HeroVillian
from base import Base, engine, Session


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def main(filename):
    Base.metadata.create_all(engine)
    session = Session()
    heroes = pd.read_csv(filename)
    for index, row in heroes.iterrows():
        logger.info('Loading article {} into DB'.format(row['id']))
        hero = HeroVillian(row['id'], row['name'], row['intelligence'], row['strength'], row['speed'], row['durability'], row['power'], row['combat'], row['publisher'], row['alignment'], row['gender'], row['height'], row['weight'], row['image'])
        session.add(hero)
    session.commit()
    session.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', 
        help='The file you want to load into the db',
        type=str
    )
    args = parser.parse_args()
    main(args.filename)
