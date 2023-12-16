from fastapi import FastAPI
import db as database
import sqlalchemy
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from client import client

# Создание экземпляра FastAPI
app = FastAPI()

# Привязка объекта базы данных к экземпляру приложения
app.state.database = database.database

# Создание соединения с базой данных с использованием SQLAlchemy
engine = sqlalchemy.create_engine(database.DATABASE_URL)

# Создание таблиц в базе данных при запуске приложения
database.metadata.create_all(engine)

# Обработчики событий при запуске и завершении приложенияaiosqlite
@app.on_event("startup")
async def startup() -> None:
    """
    Обработчик события "startup". Выполняется при старте приложения.

    Устанавливает соединение с базой данных.
    """
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()

@app.on_event("shutdown")
async def shutdown() -> None:
    """
    Обработчик события "shutdown". Выполняется при завершении приложения.

    Разрывает соединение с базой данных.
    """
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()

# Подключение роутера из модуля api.controller с префиксом и тегом
from api.controller import controller

app.include_router(controller, prefix='/api/v1', tags=['Сюда лезь!)'])

# Подключение роутера из модуля client с тегом
from client import client

app.include_router(client, tags=['Сюда не лезь!'])

# Монтирование статических файлов из директории "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Добавление middleware для обработки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
