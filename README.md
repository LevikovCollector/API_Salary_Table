# Утилита для создания сводных таблиц по языкам программирования (сайты HH и SJ)
## Описание
Данная программа позволяет собрать статистику по зарплатам программистов на разных языках 
и сформировать таблицы в консоле 

## Как установить
Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
## Пример запуска скрипта
Для запуска скрипта требуется сделать следующее:
1. Требуется получить токен на сайта superjob.ru.
2. В папке со скаченным скриптом создать файл  ```.env```
3. Открыть файл в текстом редакторе и добавить строки 
```
SJ_TOKEN=<токен для сайта superjob>
```
4. Выполнить  команду (в папке со скаченным скриптом)
```
python statistic_hh.py - формируется таблица для hh
python statistic_sj.py - формируется таблица для sj
```

## Пример выполнения программы
![](https://github.com/LevikovCollector/API_Salary_Table/blob/levikov/for_readme/console.jpg)
