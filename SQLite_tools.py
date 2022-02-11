#SQLite tools for python by AndrVLDZ
import sqlite3
from dataclasses import dataclass

@dataclass
class data:
      db: str = None

def db(input_db: str) -> None:
      data.db = input_db
      
def create_table(table: str, rows: str) -> None:
      with sqlite3.connect(data.db) as db:  
            query = f'CREATE TABLE IF NOT EXISTS {table} ({rows});'
            db.cursor().execute(query)

def db_print(table: str) -> None:
      with sqlite3.connect(data.db) as db:
            c = db.cursor()
            c.execute("SELECT * FROM {table}")
            records = c.fetchall()
            for row in records:
                  print(row)

def remove_table():
      pass

def rename_table():
      pass

def rows_cnt(table: str) -> int:
      with sqlite3.connect(data.db) as db:
          c = db.cursor()
          c.execute(f'SELECT Count(*) from {table}')
          return c.fetchone()[0]

def insert_data(values: list, table: str, rows: str) -> int:
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

def read_data(table: str, row: int, column: int) -> str:
      with sqlite3.connect(data.db) as db:
          c = db.cursor()
          sqlite_select_query = f"SELECT * from {table}"
          c.execute(sqlite_select_query)
          records = c.fetchall()
          value = records[row][column]
          return value

def edit_data():
      pass 

def remove_data():
      pass