import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from orm import create_tables, Publisher, Shop, Book, Stock, Sale

login = "postgres"
password = ""
db_name = ""
host = "localhost"
port = 5432

DSN = f'postgresql://{login}:{password}@{host}:{port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('models.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
for i in data:
    model = {
        'publisher': Publisher,
        'book': Book,
        'shop': Shop,
        'stock': Stock,
        'sale': Sale,
    }[i.get('model')]
    session.add(model(id=i.get('pk'), **i.get('fields')))
session.commit()

def get_info(author):
    results = session.query(Book) \
        .with_entities(Book.title, Shop.name, Sale.price, Sale.date_sale) \
        .join(Publisher, Publisher.id == Book.id_publisher) \
        .join(Stock, Stock.id_book == Book.id) \
        .join(Shop, Shop.id == Stock.id_shop) \
        .join(Sale, Sale.id_stock == Stock.id)
    if author.isdigit():
        result = results.filter(Publisher.id == author).all()
    else:
        result = results.filter(Publisher.name == author).all()
    for book, shop, stock_count, sale_date in result:
        print(f"{book} | {shop} | {stock_count} | {sale_date.strftime('%d-%m-%Y')}")



if __name__ == '__main__':
    author = input("Введите фамилию или идентификатор автора: ")
    get_info(author)

session.close()

