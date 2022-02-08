import sqlite3
from sqlite3 import Error
import traceback
# import datetime

from dataclasses import dataclass

from types import ModuleType
from typing import Any

from rich import pretty
pretty.install()

from rich.console import Console
from rich.table import Table

@dataclass(frozen=True)
class data:
    db: str = 'Fare.db'

    menu_1 = {
                1: 'Открыть таблицу',
                2: 'Добавить таблицу',
                3: 'Удалить таблицу',
                5: 'Выход',
                }
                
    menu_2 = {
                1: 'Открыть',
                2: 'Назад',
                3: 'Изменить трату',
                4: 'Удалить трату',
                5: 'Выход',
                }

    menu_options = {
                1: 'Показать таблицу',
                2: 'Добавить',
                3: 'Изменить',
                4: 'Удалить',
                5: 'Выход',
                }
console: Any = Console()


def menu() -> str:
    for key in data.menu_options.keys():
        console.print(key, '--', data.menu_options[key] )

def create_table(table: str) -> None:
      with sqlite3.connect(data.db) as db:
            c = db.cursor()   
            query_1 = f''' 
            CREATE TABLE IF NOT EXISTS {table} (
                  id INTEGER PRIMARY KEY,
                  type TEXT,
                  price INTEGER,
                  number INTEGER
                  ); '''
            c.execute(query_1)
            console.print("Подключен к SQLite")

def rows_cnt(table: str) -> int:
      with sqlite3.connect(data.db) as db:
          c = db.cursor()
          c.execute(f"SELECT Count(*) from {table}")
          cnt = c.fetchone()
          return cnt[0]

# def db_insert_default_values(table: str) -> None:
      with sqlite3.connect(data.db) as db:
            c = db.cursor()
            query = f'''
            INSERT OR REPLACE INTO {table}(id, type, price, number)
            VALUES
            (1,'Метро',41,44),
            (2,'Маршрутка',45,22)
            '''
            c.execute(query)
            db.commit
            print(f"+++ {rows_cnt('costs')}", style="bold green")

# def db_print(table: str) -> None:
      with sqlite3.connect(data.db) as db:
            c = db.cursor()
            c.execute("SELECT * FROM {table}")
            records = c.fetchall()
            for row in records:
                  print(row)

def db_read_data(table: str, row: int, column: int) -> str:
      with sqlite3.connect(data.db) as db:
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
      with sqlite3.connect(data.db) as db:
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
          global console
          console.print(f'Записей добавлено: {row_cnt}', style="bold green")

def calculation(table="costs") -> int:
      with sqlite3.connect(data.db) as db:
            c = db.cursor()
            c.execute(f"SELECT price, number FROM {table}")
            records = c.fetchall()
            res = 0
            for row in records:
                  res += row[0] * row[1]
            return res

def table_print_rich(table_name: str, title: str, column_1, column_2, column_3):
      table = Table(title=title)
      table.add_column(column_1)
      table.add_column(column_2)
      table.add_column(column_3)
      rows = rows_cnt(table_name)
      for row in range(rows):
            table.add_row(str(db_read_data('costs',row,1)), str(db_read_data('costs',row,2)), str(db_read_data('costs',row,3)))
      table.add_row("Итого", str(calculation()), str(rows_cnt(table_name)), style="bold red")
      global console
      console.print(table)


def dialog():
      try:
            global console
            #console.print('Выберите таблицу:')
            #список таблиц


            option = int(input('Выберите пункт меню: '))
            if option == 1:
                  console.print(rows_cnt('costs'), style="bold blue")
                  if rows_cnt('costs') == 0: 
                        console.print('В таблице нет записей', style="bold red")
                  else:
                        table_print_rich('costs', 'Таблица расходов', 'Тип', 'Цена', 'Кол-во')
                  menu()
                  dialog() 
            elif option == 2:
                  console.print('Введите данные')
                  type = str(input('Название: '))
                  price = int(input('Цена: '))
                  value = int(input('Кол-во: '))
                  db_insert_data([(type,price,value)])
                  menu()
                  dialog() 
            elif option == 3:
                  console = Console()
                  console.print("Расходы: ", str(calculation()), style="bold red")
                  console.print('Расходы: ' + str(calculation()))
                  menu()
                  dialog() 
            elif option == 4:
                  console.print('Здесь будет удаление')
                  return
            elif option == 5:
                  console.print('Работа программы завершена')
                  return
            else:
                  console.print('Такого пункта нет, введите целое число от 1 до 4')
                  menu()
                  dialog() 
      except:
            console.print('Ошибка ввода:\n', traceback.format_exc())
            menu()
            dialog()

if __name__ == '__main__':
      create_table("costs")
      menu()
      dialog()
      
else:
    console.print(f'Imported module with name {__name__}', style="bold green")

