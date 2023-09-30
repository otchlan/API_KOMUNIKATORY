import sys
import os
from db_session import init_db


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    init_db()
    print("Database initialized!")
