import json
import sqlalchemy as sq
import config as cfg

from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), nullable=False)

    books = relationship('Book', backref='publisher')

    def __str__(self):
        return f'Publisher: {self.name}'


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=200), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='books')

    def __str__(self):
        return f'Book: {self.title}'


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), nullable=False)

    books = relationship(Book, backref='shop')

    def __str__(self):
        return f'Shop: {self.name}'

class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False, default=0)

    book = relationship(Book, backref='stock')
    shop = relationship(Shop, backref='stock')

    def __str__(self):
        return f'Stock: {self.count}'

class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref='sale')

    def __str__(self):
        return f'Sale: price = {self.price}, count = {self.count}'

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def find_publisher_sales(session):
    query = input('Enter publisher name or id: ')

    if query.isdigit():
        publisher = session.query(Publisher).filter(Publisher.id == int(query)).first()
    else:
        publisher = session.query(Publisher).filter(Publisher.name == query).first()
    if not publisher:
        print('Publisher not found')
        return

    result = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
        .join(Stock, Stock.id == Sale.id_stock) \
        .join(Shop, Stock.id_shop == Shop.id) \
        .join(Book, Book.id == Stock.id_book) \
        .filter(Book.id_publisher == publisher.id) \
        .all()

    if not result:
        print('Sales not found')
        return
    else:
        for book, shop, price, date in result:
            print(f'{book} | {shop} | {price} | {date}')

DSN = f'postgresql://{cfg.DB_USER}:{cfg.DB_PASSWORD}@{cfg.DB_HOST}:{cfg.DB_PORT}/{cfg.DB_NAME}'
engine = sq.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()