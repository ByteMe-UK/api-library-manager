# 📚 REST API — Library Manager

A full-featured **CRUD REST API** for managing a book library, built with **FastAPI** and **SQLite**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Live Demo

> 🔗 _Coming soon — will be deployed on Render_

## 📸 Screenshots

> _Screenshots will be added after the API is built_

## ✨ Features

- Full CRUD operations (Create, Read, Update, Delete)
- Auto-generated interactive API docs (Swagger UI)
- SQLite database — no external DB server needed
- Input validation with Pydantic models
- Search and filter books by title, author, genre

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.10+ | Core language |
| FastAPI | Web framework |
| SQLite | Database |
| Pydantic | Data validation |
| Uvicorn | ASGI server |

## 📦 Getting Started

```bash
# Clone the repo
git clone https://github.com/ByteMe-UK/api-library-manager.git
cd api-library-manager

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn app.main:app --reload
```

Then visit `http://localhost:8000/docs` for interactive API docs.

## 📁 Project Structure

```
api-library-manager/
├── app/
│   ├── main.py            ← FastAPI app entry point
│   ├── models.py          ← SQLAlchemy models
│   ├── schemas.py         ← Pydantic schemas
│   ├── database.py        ← DB connection
│   └── routers/           ← API route handlers
├── requirements.txt
└── README.md
```

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

**Part of the [ByteMe-UK](https://github.com/ByteMe-UK) portfolio collection.**
