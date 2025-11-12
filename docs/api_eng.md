# Documentation for **api-gateway**

### Registration

>[!TIP]
> Registration is done via mail, so far without mail confirmation, but it will be soon. Authentication is performed using [JWT](https://habr.com/ru/articles/842056/), tokens are stored in [cookie](https://habr.com/ru/articles/710578/)

URL - ```api/register```

Request body:
```json
{
    "email":"example@gmail.com",
    "password":"example"
}
```

Response body:
```json
{
    "user_id": 1,
}
```

### Log in to your account 

URL - ```api/login```

Request body:
```json
{
    "email":"example@gmail.com",
    "password":"example"
}
```

Response body:
```json
{
    "access_jwt": "access_token",
    "refresh_jwt": "refresh_token"
}
```

### Refresh tokens

URL - ```api/refresh```

Request body:
The tokens are expected to be in [cookie](https://habr.com/ru/articles/710578/)

Response body:
```json
{
    "access_jwt": "access_token",
    "refresh_jwt": "refresh_token"
}
```

### Check link

>[!TIP]
> Link checking is only available for authorized users

URL - ```api/check```
Request body:
```json
{
    "links":[
        "google.com",
        "ya.ru",
    ]
}
```

Response body:
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