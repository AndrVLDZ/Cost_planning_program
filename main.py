import SQLite_tools as sq

import sqlite3
from sqlite3 import Error

from dataclasses import dataclass
from typing import Any

from rich.console import Console
from rich.table import Table

import traceback


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

def calculation(table) -> int:
      with sqlite3.connect(data.db) as db:
            c = db.cursor()
            c.execute(f"SELECT price, value FROM {table}")
            records = c.fetchall()
            res = 0
            for row in records:
                  res += row[0] * row[1]
            return res

def table_print_rich(table: str, title: str, column_1: str, column_2: str, column_3: str):
      rtable = Table(title=title, show_header=True, header_style="bold blue")
      rtable.add_column(column_1)
      rtable.add_column(column_2)
      rtable.add_column(column_3)
      rows = sq.rows_cnt(table)
      for row in range(rows):
            rtable.add_row(str(sq.read_data(table,row,1)), str(sq.read_data(table,row,2)), str(sq.read_data(table,row,3)), style="yellow")
      rtable.add_row("Итого", str(calculation(table)), str(sq.rows_cnt(table)), style="bold blue")
      global console
      console.print(rtable)


def dialog():
      try:
            global console
            option = int(input('Выберите пункт меню: '))
            table = 'Tab_1'
            if option == 1:
                  cnt = sq.rows_cnt(table)
                  if cnt == 0: 
                        console.print('В таблице нет записей', style="bold red")
                        table_print_rich(table, 'Таблица доходов и расходов', 'Тип', 'Цена', 'Кол-во')
                  else:
                        table_print_rich(table, 'Таблица доходов и расходов', 'Тип', 'Цена', 'Кол-во')
                  menu()
                  dialog() 
            elif option == 2:
                  console.print('Введите данные')
                  type = str(input('Название: '))
                  price = int(input('Цена: '))
                  value = int(input('Кол-во: '))
                  console.print("Записей добавлено: ", sq.insert_data([(type,price,value)], 'Tab_1', 'type, price, value'), style="bold green")
                  menu()
                  dialog() 
            elif option == 3:
                  console = Console()
                  console.print("Расходы: ", str(calculation(table)), style="bold red")
                  console.print('Расходы: ' + str(calculation(table)))
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
      sq.db("Fare.db")
      rows = ('id INTEGER PRIMARY KEY, type TEXT, price INTEGER, value INTEGER')
      sq.create_table('Tab_1', rows)
      menu()
      dialog()

