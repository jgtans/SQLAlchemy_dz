# Домашнее задание: SQLAlchemy часть 1

Решение задания из файла `02_4_dz.pdf`.

## Реализовано

- Класс подключения к базе данных `DatabaseConnection`.
- Абстрактный класс таблицы `BaseModel` с конструктором, который заполняет поля модели из словаря.
- Таблицы для данных DummyJSON:
  - `categories`
  - `brands`
  - `products`
  - `reviews`
- Загрузчик данных из DummyJSON.

## Установка

```bash
python -m pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

По умолчанию используется SQLite. После запуска будет создан файл `dummyjson.sqlite3`.


