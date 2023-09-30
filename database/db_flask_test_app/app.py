from flask import Flask, render_template
from sqlalchemy import create_engine, MetaData, Table
import logging

# Set up logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

DATABASE_URL = "sqlite:////home/qwe/Pulpit/asystent/test.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Create a table object without loading
messages_table = Table('messages', metadata)

# Check the columns present in the messages table
columns = [column.name for column in messages_table.c]
logging.info(f"Columns in 'messages' table: {columns}")

@app.route('/')
def index():
    # Pobranie wszystkich wiadomości z tabeli
    with engine.connect() as connection:
        # Adjust the columns in the select statement to match the actual columns
        selected_columns = [getattr(messages_table.c, col) for col in columns]
        
        # Check if selected_columns is not empty
        if not selected_columns:
            logging.error("No columns found in the 'messages' table.")
            return "No columns found in the 'messages' table.", 500

        results = connection.execute(messages_table.select().with_only_columns(*selected_columns)).fetchall()

    # Wyświetlenie wyników na stronie
    return render_template('index.html', messages=results)

if __name__ == '__main__':
    app.run(debug=True)
