# Разворачивание сервера
Сервер написан на `python 3.7.4`, для этой версии гарантируется корректность работы и совместимости всех использовавшихся пакетов.

Перед запуском сервера необходимо поставить необходимые пакеты командой `pip3 install -r requirements.txt`.
Соверщить инициализацию бд можно командами

```
python3 manage.py makemigrations polling
python3 manage.py migrate
```

Для запуска сервера ввести команду `python3 manage.py runserver` из директории проекта.

# Документация по API

Все запросы выполняются с помощью одного из 4 методов - `GET`, `POST`, `PUT`, `DELETE`

content_type - application/json

## Основные объекты
### Poll - опрос
#### Поля:
* `title` - Название опроса (строка)
* `start_date` - дата начала (дата)
* `end_date` - дата окончания (дата)

Все поля обязательные

#### Методы:
* `GET /api/poll` - возвращает все актиыне опросы (`end_date` не меньше текуей даты).

* `POST /api/poll` - создание опроса. При `start_date > end_date` возвращается ошибка 400.

* `GET/PUT/DELETE /api/poll/{id}` - возвращает/изменяет/удаляет опрос с id, равным `id`.
При наличии `start_date` в `PUT`-запросе не изменит начальную дату.


### Question - вопрос
Описывает вопрос (внутри опроса)
Существуют вопросы 3 типов:
* `O` - (One answer) - вопрос с одним ответом
* `S` - (Several answers) - вопрос с возможностю выбрать несколько вариантов ответов
* `T` - (Text answer) - вопрос с текстовым ответом (пользователь сам вводит ответ)

#### Поля:
* `text` - текст опроса (текст)
* `ttype` - тип опроса (символ, их предыдущего списка)
* `poll` - id опроса (число)

Все поля обязательные, текст не может быть пустым. 

#### Методы:
* `GET /api/questoin` - возвращает все вопросы во всех активных опросах.
* `GET /api/questoin?poll={poll_id}` - возвращает все вопросы в опросе с id, равным `poll_id`.
* `POST /api/question` - создание вопроса. 
Если тип вопроса - текстовый, автоматически создастся ответ на него с пустым текстом.
* `GET/PUT/DELETE /api/question/{id}` - возвращает/изменяет/удаляет вопрос с id, равным `id`.

### Answer - ответ
Описывает ответ на вопрос
#### Поля:
* `text` - текст ответа (строка)
* `question` - id вопроса (число)
Все поля обязательные, непустые

#### Методы:
* `GET /api/answer` - возвращает все ответы на все вопросы во всех активных опросах
* `GET /api/anser?question={question_id}` - возвращает все ответы на вопрос с id, равным `question_id`
* `POST /api/anser` - создание вопроса. При попытке создать ответ на текстовый вопрос вернется ошибка.
* `GET/PUT/DELETE /api/ansewr/{id}` - возвращает/изменяет/удаляет ответ с id, равным `id`.

### Result - результат
Описывает ответ польщователя на вопрос

#### Поля:
* `user` - id пользователя (строка)
* `text` - текст (если вопрос текстовый)
* `answer` - id ответа

Данная структура записывает ответ польщователя на вопрос
Поля `user`, `answer` обязательные, `text` обязателен, если `answer` относится к текстовому вопросу,
в остальных случаях поле недолжно передаваться в запросе.

#### Методы:
* `GET /api/result` - возвращает все ответы всех пользователей
* `GET /api/result/{uset_id}` - возвращает все ответы пользователя с id, равным `user_id`
* `GET /api/result/{uset_id}?poll={poll_id}` - возвращает все ответы пользователя с id, равным `user_id`
на вопросы в опросе с id, равным `poll_id`
* `POST /api/anser` - щапись ответа пользователя.
Ответы на вопросы с одним ответом и текстовым ответом могут быть записаны только один раз.
При повторном запросе с такими же данными вернется ошибка.

## Авторизация

При отправке `POST/PUT/DELETE` запросов по всем объектам, кроме `result`, необхдимы права администратора.
Для доступа в строке запроса неободимо прописать логин и пароль в виде парметров, например:
`POST /api/poll/login=admin&password=PassWord123` позволит создать опрос.  