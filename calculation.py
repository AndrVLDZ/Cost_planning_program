import sqlite3
from sqlite3 import Error
import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
                  transport_type TEXT,
                  price INTEGER,
                  number INTEGER
                  ); '''
            c.execute(query_1)
            print("Подключен к SQLite")

def db_insert():
      with sqlite3.connect('Fare.db') as db:
            c = db.cursor()
            query_2 = '''
            INSERT OR REPLACE INTO trips(id, transport_type, price, number)
            VALUES
            (1,'Метро',41,44),
            (2,'Маршрутка',45,22)
            '''
            c.execute(query_2)
            db.commit
            # print(bcolors.GREEN,'+++',c.rowcount,bcolors.ENDC)
            print(f"{bcolors.GREEN}+++ {c.rowcount}{bcolors.ENDC}")

def db_print():
      with sqlite3.connect('Fare.db') as db:
            c = db.cursor()
            c.execute("SELECT * FROM trips")
            records = c.fetchall()
            for row in records:
                  print(row)
                  

def db_read_data(row, column):
      with sqlite3.connect('Fare.db') as db:
        sqlite_connection = sqlite3.connect('Fare.db')
        c = sqlite_connection.cursor()
        sqlite_select_query = """SELECT * from trips"""
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
                  res += row[0]*row[1]
            return res


def trips_data():
      print('Таблица расходов')
      print('  Тип   Цена Кол-во')
      print(f'||{db_read_data(0,1)}: {db_read_data(0,2)} || {db_read_data(0,3)}')
      print(f'||{db_read_data(1,1)}: {db_read_data(1,2)}||{db_read_data(1,3)}')
      # print('Кол-во поездок')
      # print(f'||{db_read_data(0,1)}: {db_read_data(0,3)}')
      # print(f'||{db_read_data(1,1)}: {db_read_data(1,3)}')

      # # Number of trips 
      # metro_trips = int(input('Кол-во поездок на метро: '))
      # land_trips = int(input('Кол-во поездок на наземном траспорте: ')) 
      # # Trips price
      # metro_price = int(input('Цена проезда на метро: '))
      # land_price = int(input('Цена проезда на наземном транспорте: '))


def dialog():
      try:
            option = int(input('Выберите пункт меню: '))
      except:
            print('Ошибка ввода!')
            menu()
            dialog() 
      if option == 1:
            trips_data()
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
            exit()
      else:
            print('Такого пункта нет, введите целое число от 1 до 4')
            menu()
            dialog() 


      # # Number of trips 
      # metro_trips = int(input('Кол-во поездок на метро: '))
      # land_trips = int(input('Кол-во поездок на наземном траспорте: ')) 
      # # Trips price
      # metro_price = int(input('Цена проезда на метро: '))
      # land_price = int(input('Цена проезда на наземном транспорте: '))

if __name__ == '__main__':
      # create_connection(r"pythonsqlite.db")
      db_check()
      db_insert()
      # db_print()1
      menu()
      dialog()
      
else:
    print(f'Imported module with name {bcolors.GREEN}{__name__}{bcolors.ENDC}')


# def get_timestamp(y,m,d):
#       return datetime.datetime.timestamp(datetime.datetime(y,m,d))

# def get_date(tmstmp):
#       return datetime.datetime.fromtimestamp(tmstmp).date()
