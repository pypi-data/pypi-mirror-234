# Библиотека для Analytic Workspace

## Получение токена

Перейдите по ссылке https://aw.example.ru/data-master/get-token (вместо https://aw.example.ru/ укажите адрес вашего сервера Analytic Workspace).

Значение токена лучше всего сохранить в отдельном файл или поместить в переменную окружения `AW_DATA_TOKEN`.

## Пример использования

```python
from aw_client import Session


with open('aw_token', 'rt') as f:
    aw_token = f.read()

session = Session(token=aw_token, aw_url='https://aw.example.ru')

# Если токен доступа указан в переменной окружения AW_DATA_TOKEN, то объект сессии можно создавать 
# без явного указания параметра token: session = Session(aw_url='https://aw.example.ru')

df = session.load()  # df: pandas.DataFrame

display(df)
```