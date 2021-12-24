import sqlite3
from sqlite3 import Error
import traceback
# import datetime
from dataclasses import dataclass
from typing import Counter
from rich import console

from rich.console import Console
from rich.table import Table


# @dataclass(frozen=True)
# class TermColors:
#     HEADER: str    = '\033[95m'
#     BLUE: str      = '\033[94m'
#     CYAN: str      = '\033[96m'
#     GREEN: str     = '\033[92m'
#     WARNING: str   = '\033[93m'
#     FAIL: str      = '\033[91m'
#     ENDC: str      = '\033[0m'
#     BOLD: str      = '\033[1m'
#     UNDERLINE: str = '\033[4m'

console = Console()
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

def rows_cnt(table="costs") -> int:
      with sqlite3.connect('Fare.db') as db:
          c = db.cursor()
          c.execute(f"SELECT Count(*) from {table}")
          cnt = c.fetchone()
          return cnt[0]

def db_insert_default_values(table="costs") -> None:
      with sqlite3.connect('Fare.db') as db:
            c = db.cursor()
            query_2 = '''
            INSERT OR REPLACE INTO {table}(id, type, price, number)
            VALUES
            (1,'Метро',41,44),
            (2,'Маршрутка',45,22)
            '''
            c.execute(query_2)
            db.commit
            print(f"{TermColors.GREEN}+++ {c.rowcount}{TermColors.ENDC}")

def db_print(table="costs") -> None:
      with sqlite3.connect('Fare.db') as db:
            c = db.cursor()
            c.execute("SELECT * FROM {table}")
            records = c.fetchall()
            for row in records:
                  print(row)

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

def db_remove_data():
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

def calculation(table="costs") -> int:
      with sqlite3.connect('Fare.db') as db:
            c = db.cursor()
            c.execute(f"SELECT price, number FROM {table}")
            records = c.fetchall()
            res = 0
            for row in records:
                  res += row[0] * row[1]
            return res

def costs_data_rich():
      table = Table(title='Таблица расходов')
      table.add_column('Тип')
      table.add_column('Цена')
      table.add_column('Кол-во')
      rows = rows_cnt()
      for row in range(rows):
            table.add_row(str(db_read_data(row,1)), str(db_read_data(row,2)), str(db_read_data(row,3)))
      table.add_row("Итого", str(rows_cnt()), str(calculation()), style="bold red")
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
                  console = Console()
                  console.print("Расходы: ", str(calculation()), style="bold red")
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
      print(rows_cnt())
      if rows_cnt == 0: 
            db_insert_default_values()
      menu()
      dialog()
      
else:
    console.print(f'Imported module with name {__name__}', style="bold green")





# def get_timestamp(y,m,d):
#       return datetime.datetime.timestamp(datetime.datetime(y,m,d))

# def get_date(tmstmp):
#       return datetime.datetime.fromtimestamp(tmstmp).date()
