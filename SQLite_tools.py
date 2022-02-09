#SQLite tools for python by AndrVLDZ
import sqlite3

class data:
      db: str = None

def add_db(input_db: str) -> None:
      data.db = input_db
      
def create_table(table: str, rows: str) -> None:
      with sqlite3.connect(data.db) as db:  
            query = f'CREATE TABLE IF NOT EXISTS {table} ({rows});'
            db.cursor().execute(query)

def rows_cnt(table: str) -> int:
      with sqlite3.connect(data.db) as db:
          c = db.cursor()
          c.execute(f'SELECT Count(*) from {table}')
          return c.fetchone()[0]

def db_insert_data(values: list, table: str, rows: str) -> int:
      with sqlite3.connect(data.db) as db:
          c = db.cursor()
          row_cnt: int = 0
          for item in values:
              c.execute(f'''
                    INSERT OR REPLACE INTO {table}({rows})
                    VALUES
                    {item}
                    ''')
              row_cnt += 1 
          db.commit
          return row_cnt