import os
from flask import Flask, render_template
from sqlalchemy import create_engine, MetaData, Table
import logging

# Set up logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Ustal ścieżkę do bazy danych na podstawie lokalizacji bieżącego skryptu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = "sqlite:///" + os.path.join(BASE_DIR, "test.db")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Load the table schema from the database
metadata.reflect(bind=engine)

if 'messages' in metadata.tables:
    messages_table = metadata.tables['messages']
    columns = [column.name for column in messages_table.c]
    logging.info(f"Columns in 'messages' table: {columns}")
else:
    logging.error("Table 'messages' not found in the database.")
    messages_table = None

@app.route('/')
def index():
    if messages_table is None:
        return "Table 'messages' not found in the database.", 500

    # Pobranie wszystkich wiadomości z tabeli
    with engine.connect() as connection:
        results = connection.execute(messages_table.select()).fetchall()

    # Wyświetlenie wyników na stronie
    return render_template('index.html', messages=results, db_path=DATABASE_URL, headers=columns)


if __name__ == '__main__':
    app.run(debug=True)
