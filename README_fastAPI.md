# 📝 FastAPI Todo API

A simple **Todo REST API** built with [FastAPI](https://fastapi.tiangolo.com/), SQLAlchemy, and Pydantic.  
This project demonstrates CRUD operations (Create, Read, Update, Delete) with a PostgreSQL/MySQL/SQLite backend.

---

## 🚀 Features

- ✅ Create todos
- 📌 Retrieve all todos or a single todo by ID
- ✏️ Update todos (title, status)
- ❌ Delete todos
- 🗄️ SQLAlchemy ORM integration
- 🛡️ Pydantic validation
- ⚡ FastAPI with automatic docs (`/docs`, `/redoc`)

---

## 🛠️ Tech Stack

- **Backend:** FastAPI
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Database:** SQLite (default, but supports PostgreSQL/MySQL)
- **Server:** Uvicorn

---

## 📂 Project Structure

```text
todo-app/
├── database.py       # Database connection & session
├── models.py         # SQLAlchemy models
├── schemas.py        # Pydantic schemas
├── main.py           # FastAPI routes
├── requirements.txt  # Dependencies
└── README.md         # Project documentation

```

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/charlesaloaye/fastapi-todo.git
   cd fastapi-todo
   ```

2. **Create & activate virtual environment**

   ```bash
   python -m venv .venv or python3 -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows

   ```

3. **Install dependencies**

   ```bash
    pip install -r requirements.txt or
    pip3 install -r requirements.txt

   ```

4. **Run the server**

   ```bash
   uvicorn main:app --reload

   ```

5. **Open your browser at:**
   ```bash
   Swagger docs → http://127.0.0.1:8000/docs
   Redoc docs → http://127.0.0.1:8000/redoc
   ```

| Method | Endpoint      | Description             |
| ------ | ------------- | ----------------------- |
| GET    | `/todos/`     | Fetch all todos         |
| GET    | `/todos/{id}` | Fetch a single todo     |
| POST   | `/todos/`     | Create a new todo       |
| PUT    | `/todos/{id}` | Update an existing todo |
| DELETE | `/todos/{id}` | Delete a todo           |

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

📜 License

This project is licensed under the MIT License.
