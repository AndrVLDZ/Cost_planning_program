import sqlite3
from sqlite3 import Error
import traceback
# import datetime
from dataclasses import dataclass
from typing import Counter

@dataclass(frozen=True)
class TermColors:
    HEADER: str    = '\033[95m'
    BLUE: str      = '\033[94m'
    CYAN: str      = '\033[96m'
    GREEN: str     = '\033[92m'
    WARNING: str   = '\033[93m'
    FAIL: str      = '\033[91m'
    ENDC: str      = '\033[0m'
    BOLD: str      = '\033[1m'
    UNDERLINE: str = '\033[4m'


menu_options = {
            1: 'Таблица трат',
            2: 'Добавить трату',
            3: 'Сумма трат',
            4: 'Выход',
            }

def menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def db_check():
      with sqlite3.connect('Fare.db') as db:
            c = db.cursor()   
            query_1 = ''' 
            CREATE TABLE IF NOT EXISTS costs (
                  id INTEGER PRIMARY KEY,
                  type TEXT,
                  price INTEGER,
                  number INTEGER
                  ); '''
            c.execute(query_1)
            print("Подключен к SQLite")

def db_check_rows():
       with sqlite3.connect('Fare.db') as db:
            c = db.cursor()
            c.execute('SELECT COUNT(*)')
            cnt = c.fetchone()
            return cnt[0]

def db_insert_default_values():
      with sqlite3.connect('Fare.db') as db:
            c = db.cursor()
            query_2 = '''
            INSERT OR REPLACE INTO costs(id, type, price, number)
            VALUES
            (1,'Метро',41,44),
            (2,'Маршрутка',45,22)
            '''
            c.execute(query_2)
            db.commit
            print(f"{TermColors.GREEN}+++ {c.rowcount}{TermColors.ENDC}")

def db_print():
      with sqlite3.connect('Fare.db') as db:
            c = db.cursor()
            c.execute("SELECT * FROM costs")
            records = c.fetchall()
            for row in records:
                  print(row)
                  
def db_row_cnt(table="costs") -> int:
      with sqlite3.connect('Fare.db') as db:
          c = db.cursor()
          sqlite_select_query = f"SELECT Count(*) from {table}"
          c.execute(sqlite_select_query)
          cnt = c.fetchone()
          return cnt[0]

def db_read_data(row: int, column: int, table="costs") -> str:
      with sqlite3.connect('Fare.db') as db:
          c = db.cursor()
          sqlite_select_query = f"SELECT * from {table}"
          c.execute(sqlite_select_query)
          records = c.fetchall()
          value = records[row][column]
          return value

def db_edit_data():
      pass 

def db_insert_data(values: list, table="costs") -> None:
      with sqlite3.connect('Fare.db') as db:
          c = db.cursor()
          row_cnt: int = 0
          for item in values:
              c.execute(f'''
                    INSERT OR REPLACE INTO {table}(type, price, number)
                    VALUES
                    {item}
                    ''')
              row_cnt += 1 
          db.commit
          print(f"{TermColors.GREEN}Записей добавлено: {row_cnt}{TermColors.ENDC}")

def calculation():
      with sqlite3.connect('Fare.db') as db:
            c = db.cursor()
            c.execute("SELECT price, number FROM costs")
            records = c.fetchall()
            res = 0
            for row in records:
                  res += row[0] * row[1]
            return res

def costs_data_rich():
      from rich.console import Console
      from rich.table import Table
      table = Table(title='Таблица расходов')
      table.add_column('Тип')
      table.add_column('Цена')
      table.add_column('Кол-во')
      rows = db_row_cnt()
      for row in range(rows):
            table.add_row(str(db_read_data(row,1)), str(db_read_data(row,2)), str(db_read_data(row,3)))
            console = Console()
      console.print(table)

def dialog():
      try:
            option = int(input('Выберите пункт меню: '))
            if option == 1:
                  costs_data_rich()
                  menu()
                  dialog() 
            elif option == 2:
                  print('Введите данные')
                  type = str(input('Название: '))
                  price = int(input('Цена: '))
                  value = int(input('Кол-во: '))
                  data = [(type,price,value)]
                  db_insert_data(data)
                  menu()
                  dialog() 
            elif option == 3:
                  print('Расходы: ' + str(calculation()))
                  menu()
                  dialog() 
            elif option == 4:
                  print('Работа программы завершена')
                  return
            else:
                  print('Такого пункта нет, введите целое число от 1 до 4')
                  menu()
                  dialog() 
      except:
            print('Ошибка ввода:\n', traceback.format_exc())
            menu()
            dialog()

if __name__ == '__main__':
      db_check()
      print(db_check_rows())
      if db_check_rows == 1: 
            db_insert_default_values()
      menu()
      dialog()
      
else:
    print(f'Imported module with name {TermColors.GREEN}{__name__}{TermColors.ENDC}')





# def get_timestamp(y,m,d):
#       return datetime.datetime.timestamp(datetime.datetime(y,m,d))

# def get_date(tmstmp):
#       return datetime.datetime.fromtimestamp(tmstmp).date()
