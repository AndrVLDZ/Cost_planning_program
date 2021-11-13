import sqlite3
from sqlite3 import Error
import datetime
from dataclasses import dataclass

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
            1: 'Таблица расходов',
            2: 'Изменить данные',
            3: 'Посчитать расходы',
            4: 'Выход',
            }

def menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def db_check():
      with sqlite3.connect('Fare.db') as db:
            c = db.cursor()   
            query_1 = ''' 
            CREATE TABLE IF NOT EXISTS trips (
                  id INTEGER PRIMARY KEY,
                  type TEXT,
                  price INTEGER,
                  number INTEGER
                  ); '''
            c.execute(query_1)
            print("Подключен к SQLite")

def db_insert():
      with sqlite3.connect('Fare.db') as db:
            c = db.cursor()
            query_2 = '''
            INSERT OR REPLACE INTO trips(id, type, price, number)
            VALUES
            (1,'Метро',41,44),
            (2,'Маршрутка',40,22)
            '''
            c.execute(query_2)
            db.commit
            print(f"{TermColors.GREEN}+++ {c.rowcount}{TermColors.ENDC}")

def db_print():
      with sqlite3.connect('Fare.db') as db:
            c = db.cursor()
            c.execute("SELECT * FROM trips")
            records = c.fetchall()
            for row in records:
                  print(row)
                  

def db_read_data(row, column, table="trips"):
      with sqlite3.connect('Fare.db') as db:
          sqlite_connection = sqlite3.connect('Fare.db')
          c = sqlite_connection.cursor()
          sqlite_select_query = f"SELECT * from {table}"
          c.execute(sqlite_select_query)
          records = c.fetchall()
          value = records[row][column]
          return value 

def calculation():
      with sqlite3.connect('Fare.db') as db:
            c = db.cursor()
            c.execute("SELECT price, number FROM trips")
            records = c.fetchall()
            res = 0
            for row in records:
                  res += row[0] * row[1]
            return res

def trips_data_rich():
      from rich.console import Console
      from rich.table import Table
      table = Table(title='Таблица расходов')
      table.add_column('Тип')
      table.add_column('Цена')
      table.add_column('Кол-во')
      table.add_row(str(db_read_data(0,1)), str(db_read_data(0,2)), str(db_read_data(0,3)))
      table.add_row(str(db_read_data(1,1)), str(db_read_data(1,2)), str(db_read_data(1,3)))
      console = Console()
      console.print(table)

def dialog():
      try:
            option = int(input('Выберите пункт меню: '))
            if option == 1:
                  trips_data_rich()
                  menu()
                  dialog() 
            elif option == 2:
                  print('Здесь будет изменение данных')
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
            print('Ошибка ввода!')
            menu()
            dialog()

if __name__ == '__main__':
      db_check()
      db_insert()
      menu()
      dialog()
      
else:
    print(f'Imported module with name {TermColors.GREEN}{__name__}{TermColors.ENDC}')





# def get_timestamp(y,m,d):
#       return datetime.datetime.timestamp(datetime.datetime(y,m,d))

# def get_date(tmstmp):
#       return datetime.datetime.fromtimestamp(tmstmp).date()
