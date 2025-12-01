import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import get_db
from models import Base


from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import get_db
from models import Base

# Создание отдельной БД для тестов
TEST_DATABASE_URL = "sqlite:///./test_todos.db"

test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)

Base.metadata.create_all(bind=test_engine)

# Функция для очистки БД перед каждым тестом
def reset_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)


# Переопределяем зависимость get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Создаём TestClient, через него будем использовать API
client = TestClient(app)





# Тест №1
def test_get_todos_empty_returns_404():
    reset_database()

    # Отправляем GET-запрос
    response = client.get("/todos/")

    # Проверяем, что сервер вернул 404
    assert response.status_code == 404

    # Дополнительно проверяем текст ошибки
    data = response.json()
    assert data["detail"] == "No Todos at the moment try creating one"










# Тест №2
def test_create_todo_success():
    reset_database()

    # Формируем тело запроса для создания новой задачи
    payload = {
        "title": "Сходить в зал",
        "is_complete": False
    }

    # Отправляем POST-запрос на /todos/
    response = client.post("/todos/", json=payload)

    # Проверяем, что сервер вернул статус 201 (Created)
    assert response.status_code == 201

    data = response.json()

    # Проверяем, что сервер вернул те же данные, что мы отправили
    assert data["title"] == payload["title"]
    assert data["is_complete"] == payload["is_complete"]

    # Проверяем, что сервер добавил служебные поля
    assert "id" in data
    assert data["id"] > 0
    assert "created_at" in data
    assert "updated_at" in data









# Тест №3
def test_get_todo_by_id_success():
    reset_database()

    # Сначала создаём новую задачу через POST /todos/
    create_payload = {
        "title": "Выучить FastAPI",
        "is_complete": False
    }
    create_response = client.post("/todos/", json=create_payload)

    # Убедимся, что создание прошло успешно
    assert create_response.status_code == 201

    # Достаём id созданной задачи из ответа
    created_todo = create_response.json()
    todo_id = created_todo["id"]

    # Теперь пытаемся получить эту задачу по id через GET /todos/{id}
    get_response = client.get(f"/todos/{todo_id}")

    # Проверяем, что сервер вернул 200
    assert get_response.status_code == 200

    # Проверяем тело ответа
    data = get_response.json()
    assert data["id"] == todo_id
    assert data["title"] == create_payload["title"]
    assert data["is_complete"] == create_payload["is_complete"]





# Тест №4
def test_create_todo_duplicate_title_returns_400():
    reset_database()

    # Формируем тело запроса с заголовком задачи
    payload = {
        "title": "Повторяющаяся задача",
        "is_complete": False
    }

    # Первый запрос на создание задачи
    first_response = client.post("/todos/", json=payload)
    assert first_response.status_code == 201

    # Второй запрос с тем же title должен вызвать ошибку 400
    second_response = client.post("/todos/", json=payload)

    # Проверяем статус ответа
    assert second_response.status_code == 400

    # Проверяем текст ошибки
    data = second_response.json()
    assert data["detail"] == "This Todo already exist"






# Тест №5
def test_update_todo_success():
    reset_database()

    # Сначала создаём задачу, которую потом будем обновлять
    create_payload = {
        "title": "Помыть посуду",
        "is_complete": False
    }
    create_response = client.post("/todos/", json=create_payload)
    assert create_response.status_code == 201

    created_todo = create_response.json()
    todo_id = created_todo["id"]

    # Формируем новые данные для задачи
    update_payload = {
        "title": "Помыть всю посуду",
        "is_complete": True
    }

    #Отправляем PUT /todos/{id} с новыми данными
    update_response = client.put(f"/todos/{todo_id}", json=update_payload)

    # Проверяем, что сервер вернул 200
    assert update_response.status_code == 200

    # Проверяем, что поля задачи действительно обновились
    data = update_response.json()
    assert data["id"] == todo_id
    assert data["title"] == update_payload["title"]
    assert data["is_complete"] == update_payload["is_complete"]





# Тест №6
def test_delete_todo_success_and_then_not_found():
    reset_database()

    # Сначала создаём задачу, которую потом удалим
    create_payload = {
        "title": "Удалить эту задачу",
        "is_complete": False
    }
    create_response = client.post("/todos/", json=create_payload)
    assert create_response.status_code == 201

    created_todo = create_response.json()
    todo_id = created_todo["id"]

    dummy_body = {
        "title": "не важно",
        "is_complete": False
    }

    # Удаляем задачу через DELETE /todos/{id}
    delete_response = client.request("DELETE", f"/todos/{todo_id}", json=dummy_body)

    # Проверяем, что удаление прошло успешно
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Todo deleted successfully"}

    # Пытаемся удалить эту же задачу ещё раз
    second_delete_response = client.request("DELETE", f"/todos/{todo_id}", json=dummy_body)

    # Теперь задача уже должна отсутствовать, ожидаем 400 и нужный текст ошибки
    assert second_delete_response.status_code == 400
    data = second_delete_response.json()
    assert data["detail"] == "This Todo does not exist"
