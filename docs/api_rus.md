# Документация для **api-gateway**

### Регистрация

>[!TIP]
> Регистрация выполняется через почту, пока что без подтвержения почты, но в скоре оно будет. Аутентификация выполняется с помощью [JWT](https://habr.com/ru/articles/842056/), токены хранятся в [cookie](https://habr.com/ru/articles/710578/)

Путь  - ```api/register```

Тело запроса:
```json
{
    "email":"example@gmail.com",
    "password":"example"
}
```

Тело ответа:
```json
{
    "user_id": 1,
}
```

### Вход в аккаунт 

Путь - ```api/login```

Тело запроса:
```json
{
    "email":"example@gmail.com",
    "password":"example"
}
```

Тело ответа:
```json
{
    "access_jwt" : "access_token",
    "refresh_jwt": "refresh_token"
}
```

### Обновление токенов

Путь - ```api/refresh```

Тело запроса:
Ожидается, что токены будут в [cookie](https://habr.com/ru/articles/710578/)

Тело ответа:
```json
{
    "access_jwt" : "access_token",
    "refresh_jwt": "refresh_token"
}
```

### Проверка ссылок

>[!TIP]
> Проверка ссылок доступна только для авторизованных пользователей

Путь - api/check
Тело запроса:
```json
{
    "links":[
        "google.com",
        "ya.ru",
    ]
}
```

Тело ответа:
```json
[
    {
        "link": "ya.ru",
        "status": true
    },
    {
        "link": "google.com",
        "status": true
    }
]
```
