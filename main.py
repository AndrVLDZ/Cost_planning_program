import profile
from tkinter import N
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

def menu() -> None:
    print('\n')
    for key in data.menu_options.keys():
        console.print(key, '--', data.menu_options[key])
    print('\n')

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
      rtable = Table(title=title, show_header=True, header_style='bold blue')
      rtable.add_column(column_1)
      rtable.add_column(column_2)
      rtable.add_column(column_3)
      rows = sq.rows_cnt(table)
      for row in range(rows):
            rtable.add_row(str(sq.read_data(table,row,1)), str(sq.read_data(table,row,2)), str(sq.read_data(table,row,3)), style='yellow')
      rtable.add_row('Итого', str(calculation(table)), str(sq.rows_cnt(table)), style='bold blue')
      global console
      console.print(rtable)


def dialog():
      try:
            global console
            option = int(input('Выберите пункт меню: '))
            table = '1231'
            if option == 1:
                  cnt = sq.rows_cnt(table)
                  if cnt == 0: 
                        console.print('В таблице нет записей', style='bold red')
                        table_print_rich(table, 'Таблица доходов и расходов', 'Тип', 'Цена', 'Кол-во')
                  else:
                        table_print_rich(table, 'Таблица доходов и расходов', 'Тип', 'Цена', 'Кол-во')
                  menu()
                  dialog() 
            elif option == 2:
                  console.print('\nВведите данные')
                  answ: int = ''
                  row_data = []
                  while answ != 0:      
                        type = str(input('Название: '))
                        price = int(input('Цена: '))
                        value = int(input('Кол-во: '))
                        row_data.append((type,price,value))
                        console.print('Запись добавлена', style='bold green')
                        try:
                              answ = int(input('\nЗакончить ввод - 0 \nПродолжить - 1\n -> '))
                        except:
                              console.print('Введите 0 или 1:\n', traceback.format_exc())
                  console.print("\nВсего записей добавлено: ", sq.insert_data(table, row_data, 'type, price, value'), style="bold green")
                  menu()
                  dialog() 
            elif option == 3:
                  console = Console()
                  console.print("Расходы: ", str(calculation(table)), style='bold red')
                  console.print('Расходы: ' + str(calculation(table)))
                  menu()
                  dialog() 
            elif option == 4:
                  answ: int = ''
                  row_data = []
                  while answ != 0:      
                        type = str(input('\nВведите тип для удаления: '))
                        row_data.append(type)
                        console.print('Запись добавлена на удаление', style='red')
                        try:
                              answ = int(input('\nЗакончить ввод - 0 \nПродолжить - 1\n -> '))
                        except:
                              console.print('Введите 0 или 1:\n', traceback.format_exc())
                  try:
                        print(row_data)
                        console.print("\nВсего записей удалено: ", sq.remove_rows_by_names(table, 'type', row_data), style="bold red")
                  except:
                        console.print('Ошибка в одном из типов:\n', traceback.format_exc())
                  
                  menu()
                  dialog() 
                  return
            elif option == 5:
                  console.print('Работа программы завершена')
                  return
            else:
                  console.print('Такого пункта нет, введите целое число от 1 до 4')
                  menu()
                  dialog() 
      except:
            console.print('Введите цифру:\n', traceback.format_exc())
            menu()
            dialog()

if __name__ == '__main__':
      sq.db('Fare.db')
      rows = ('id INTEGER PRIMARY KEY, type TEXT, price INTEGER, value INTEGER')
      sq.create_table('Tab_1', rows)
      # sq.remove_rows_by_id('Tab_1', [1])
      menu()
      dialog()

