# Bank Webhook Receiver (Django)

Backend сервис на Django для приёма webhook-ов от банка

## Стек
Python 3.9
Django 4.2.17
MySQL

## Установка

1. Установить зависимости:

```bash
pip install -r requirements.txt
```

2. Создать .env файл для бд:

```bash
DB_NAME=db_name
DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=3306
```

3. Применить миграции:

```bash
python manage.py migrate
```

4. Запуск

```bash
python manage.py runserver
```


