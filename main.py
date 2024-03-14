import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return {"id": self.id, "name": self.name}

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"))
    publisher = relationship(Publisher, backref="books")

    def __str__(self):
        return {"id": self.id, "title": self.title, "id_publisher": self.id_publisher}

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return {"id": self.id, "name": self.name}

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"))
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"))
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

    def __str__(self):
        return {"id": self.id, "id_book": self.id_book, "id_shop": self.id_shop, "count": self.count}

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer)
    date_sale = sq.Column(sq.Date)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"))
    count = sq.Column(sq.Integer)

    stock = relationship(Stock, backref="sale")

    def __str__(self):
        return {"id": self.id, "price": self.price, "date_sale": self.date_sale, "id_stock": self.id_stock, "count": self.count}


def get_info(author):
    query = session.query(Book.title, Shop.name, Stock.count, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale)
    if isinstance(author, int):
        result = query.filter(Publisher.id == author).all()
    elif isinstance(author, str):
        result = query.filter(Publisher.name.like(f"%{author}%")).all()
    else:
        return "Author not found"
    for book, shop, stock_count, sale_date in result:
        return book, shop, stock_count, sale_date

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

login = "postgres"
password = "(LilBoPeep2017)"
db_name = "data_bases_sophie"
host = "localhost"
port = 5432
DSN = f'postgresql://{login}:{password}@{host}:{port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

jo = Publisher(name="Джордж Оруэлл")
rb = Publisher(name="Рэй Брэдбери")

jo1 = Book(title="1984", id_publisher=jo.id)
jo2 = Book(title="Глотнуть воздуха", id_publisher=jo.id)

rb1 = Book(title="Вино из одуванчиков", id_publisher=rb.id)
rb2 = Book(title="Смерть - дело одинокое", id_publisher=rb.id)

shop1 = Shop(name="Читай-город")
shop2 = Shop(name="Лабиринт")

stock1 = Stock(id_book=jo1.id, id_shop=shop1.id, count=300)
stock2 = Stock(id_book=jo2.id, id_shop=shop2.id, count=100)
stock3 = Stock(id_book=rb1.id, id_shop=shop1.id, count=200)
stock4 = Stock(id_book=rb2.id, id_shop=shop2.id, count=150)

sale1 = Sale(price=800, date_sale="2024-01-06", id_stock=stock1.id, count=200)
sale2 = Sale(price=450, date_sale="2024-02-12", id_stock=stock2.id, count=50)
sale3 = Sale(price=650, date_sale="2024-01-18", id_stock=stock3.id, count=100)
sale4 = Sale(price=500, date_sale="2024-03-24", id_stock=stock4.id, count=80)


session.add_all([jo, rb])
session.add_all([jo1, jo2, rb1, rb2])
session.add_all([shop1, shop2])
session.add_all([stock1, stock2, stock3, stock4])
session.add_all([sale1, sale2, sale3, sale4])
session.commit()


if __name__ == '__main__':
    author = input("Автор: ")
    print(get_info(author))

session.close()


