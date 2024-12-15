import json
import sqlalchemy as sq
import config as cfg

from sqlalchemy.orm import sessionmaker
from main import Publisher, Book, Shop, Stock, Sale, create_tables

DSN = f'postgresql://{cfg.DB_USER}:{cfg.DB_PASSWORD}@{cfg.DB_HOST}:{cfg.DB_PORT}/{cfg.DB_NAME}'
engine = sq.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json') as f:
    data = json.load(f)

    for item in data:
        model = {
            'publisher': Publisher,
            'book': Book,
            'shop': Shop,
            'stock': Stock,
            'sale': Sale}[item.get('model')]
        session.add(model(id = item.get('pk'), **item.get('fields')))
    session.commit()