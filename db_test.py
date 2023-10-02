import sqlite3

# Ścieżka do bazy danych
DATABASE_PATH = "test.db"

def fetch_all_tables_content():
    # Połączenie z bazą danych
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Pobranie listy wszystkich tabel w bazie danych
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        print(f"\nTabela: {table_name}\n{'-' * 40}")

        # Pobranie i wyświetlenie wszystkich rekordów z tabeli
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    # Zamknięcie połączenia z bazą danych
    conn.close()

if __name__ == "__main__":
    fetch_all_tables_content()
