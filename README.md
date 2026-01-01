# StripeTestTask
---
Integration of test payment forms built with Django using [Stripe](https://docs.stripe.com/)
[Project](https://stripetesttask.onrender.com/admin/) is hosted with [Render](https://render.com/)
## Локальный запуск
---
1. Склонировать репозиторий:
```bash
git clone https://github.com/Eleverkuhn/StripeTestTask
cd StripeTestTask
```
2. Создать виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate
```
3. Установить зависимости:
```bash
pip install -r requirements.txt
```
4. Создать `.env` файл с переменными окружения:
```bash
touch .env
vim .env
```
5. Заполнить `.env` файл по образцу:
```env
TEST_ENV=docker

POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=stripedb
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

DJANGO_HOST=django
DJANGO_PORT=8000
DJANGO_KEY=...
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@email.com
ADMIN_PASSWORD=...

STRIPE_SK=sk_test_...
STRIPE_PK=pk_test_...

PYTHONPATH=payments/
```
6. Запустить Docker контейнер:
```bash
docker compose up --build
```
7. Перейти по [localhost](http://localhost:8000/item/1)
## Примечания
---
Все тестовые данные уже загружены через фикстуры. 
Всего 5 товаров, с 1-3 цены в рублях, 4 и 5 в долларах

Также реализован отдельный эндпоинт `/order/id`
Всего заказов два: в одном все товары в рублях, в другом все в долларах (id 1 и 2)
## Used Libraries
---
- Django
- Stripe
- psycopg
- gunicorn
- pydantic-settings
