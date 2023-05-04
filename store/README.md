# "Internet-shop of something goods"

## Technologies:
- Python (Django)
- Celery
- Redis

В данном проекте реализован следующий функционал:
- Аутентификация и авторизация, регистрация клиентов на сайте с подтверждением профиля по email
- Авторизация через социальные сети
- Возможность изменять свои данные в личном кабинете (ФИО, аватар)
- На странице товаров можно их фильтровать по категориям
- Товары можно добавлять в корзину и совершать оформление заказов
- Есть возможность просматривать историю заказов и видеть статус своего заказа
- Статус заказа меняется после оплаты и после создания
- Подключена в тестовом режиме онлайн оплата при помощи сервиса Stripe
- Настроены права на администратора для работы с контентом магазина, настроена админ панель

This project in a particular case is a clothing store.
This project implements the following functionality:
- Authentication and authorization, registration of clients on the site with profile confirmation by email
- Authorization through social networks
- The ability to change your data in your personal account (name, avatar)
- On the product page, you can filter them by category
- Items can be added to cart and checkout
- It is possible to view the history of orders and see the status of your order
- Order status changes after payment and after creation
- Connected in test mode online payment using the Stripe service
- Administrator rights are configured to work with the content of the store, the admin panel is configured

## Create venv:
### `python3 -m venv venv`

## Install requirements.txt
### `pip freeze > requirements.txt`

## Run project
### `python manage.py runserver`


## Requirements
```
amqp==5.1.1
asgiref==3.5.2
async-timeout==4.0.2
billiard==3.6.4.0
celery==5.2.7
certifi==2022.12.7
cffi==1.15.1
charset-normalizer==2.1.1
click==8.1.3
click-didyoumean==0.3.0
click-plugins==1.1.1
click-repl==0.2.0
cryptography==39.0.0
defusedxml==0.7.1
Django==3.2.13
django-allauth==0.52.0
django-redis==5.2.0
django_debug_toolbar==3.8.1
djangorestframework==3.14.0
idna==3.4
isort==5.12.0
kombu==5.2.4
oauthlib==3.2.2
Pillow==9.3.0
prompt-toolkit==3.0.36
psycopg2==2.9.5
pycparser==2.21
PyJWT==2.6.0
python-dotenv==1.0.0
python3-openid==3.2.0
pytz==2022.6
redis==4.5.1
requests==2.28.1
requests-oauthlib==1.3.1
six==1.16.0
sqlparse==0.4.3
stripe==5.1.1
urllib3==1.26.14
vine==5.0.0
wcwidth==0.2.6

```