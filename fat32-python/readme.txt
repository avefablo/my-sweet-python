Приложение для парсинга FAT32:
    -умеет парсить образы:
      -считывать bios parameter block
      -находить и считывать root
      -переходить в другие папки
      -собирать цепочки данных по кластерам
    -есть консольная и графическая утилиты:
      -хождение по директориям
      -просмотр файлов
      -сохранение файлов на диск
      -отображение содержимого директорий
    -работать с именами (как с лонг-нейм так и с 8.3)


Содержимое каталога:
.
├── abstract_app.py - описывает абстрактное приложение с функциями save, cat, cd, ls
├── fat_fs_lib - модуль работы с фат
│   ├── __init__.py
│   ├── bpb.py - BiosParameterBlock
│   ├── directory.py - представляет кластеризованную директорию
│   ├── entries.py -
│   ├── fat.py - представляет таблицу FAT
│   ├── fat_fs.py
│   ├── fat_time.py - методы для конвертирования времени FAT в DateTime
│   ├── long_name.py - методы для генерирования длинного имени FAT
│   ├── misc.py - разные маленькие функции
│   └── mock_fs.py - fs для mock тестирования
├── completer.py - комплитер для командной строки (основан на readline)
├── gui.py - графическая утилита (PyQt5)
├── main.py - консольная утилита
├── mock - файлы для MOCK (см раздел тестирование)
│   ├── 08\ Vilaines\ filles,\ mauvais\ garçons.mp3
│   ├── PolishNotationParser.java
│   ├── bmpinfo.py
│   ├── bpb
│   ├── data
│   ├── fat0
│   └── fat1
├── readme.md
├── saved - папка для сохранений
└── tests.py - тесты


Тестирование:
для тестирования был взят образ диска с такой структурой:
.
├── java
│   └── PolishNotationParser.java
├── longdirnameawesome
│   └── 08\ Vilaines\ filles,\ mauvais\ garçons.mp3
└── python
    └── bmpinfo.py
после чего извлечены в файлы bpb, fat0, fat1 и data соответственно Bios Parameter Block,
две таблицы фат и данные

тестирование проводится так:
в конструктор Fat образа передается MockFs, после чего мы начинаем работать с ним как с обычным образом:
-проверяем BPB
-пытаемся ходить по директориям
-сохраняем файлы
Name                      Stmts   Miss  Cover
---------------------------------------------
fat_fs_lib/__init__.py        0      0   100%
fat_fs_lib/bpb.py            37      0   100%
fat_fs_lib/directory.py     100     10    90%
fat_fs_lib/entries.py        69      7    90%
fat_fs_lib/fat.py            41      2    95%
fat_fs_lib/fat_fs.py         31      0   100%
fat_fs_lib/fat_time.py       14      0   100%
fat_fs_lib/long_name.py      22      1    95%
fat_fs_lib/misc.py           10      2    80%
fat_fs_lib/mock_fs.py        31      2    94%
tests.py                    111      0   100%
---------------------------------------------
TOTAL                       466     24    95% 
