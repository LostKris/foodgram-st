# FOODGRAM

[![Linter (Flake 8)](https://github.com/LostKris/foodgram-st/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/LostKris/foodgram-st/actions/workflows/lint.yml)

Foodgram - это онлайн-платформа для сохранения и обмена рецептами.

## Основные возможности платформы:

* Создание и редактирование рецептов
* Добавление рецептов в избранное
* Сохранение рецептов в "корзину": после этого можно загрузить полный список ингредиентов и отправиться за покупками!
* Можно подписаться на других авторов рецептов

## Запуск проекта:

1. Перейдите в директорию "infra"

```bash
cd infra
```

2. Скопируйте/переименуйте файл `.env.example` в `.env`. Измените значения переменных в файле.

3. Запустите проект:
```bash
docker compose up --build --detach
```

Проект должен стать доступен по адресу http://localhost

## Остановка проекта:
```
docker compose down
```
## API

Примеры запросов к API можно посмотреть в PostMan коллекции, лежащей в директории `postman_collection`.

Также по адресу http://localhost/api/docs/redoc.html доступна спецификация в интерфейсе ReDoc.
