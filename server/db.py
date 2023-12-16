import sqlalchemy
import databases
import ormar

# Определение URL базы данных (в данном случае, PostgreSQL)
DATABASE_URL = "postgresql://leha:a11e11eo@89.232.176.235:5432/test1"

# Инициализация объекта базы данных с использованием databases
database = databases.Database(DATABASE_URL)

# Инициализация объекта метаданных для работы с SQLAlchemy
metadata = sqlalchemy.MetaData()

# Определение метакласса BaseMeta для использования в ормар-моделях
class BaseMeta(ormar.ModelMeta):
    # Указание объекта метаданных и базы данных для моделей
    metadata = metadata
    database = database
    
# Импорт моделей из модуля api.models
from api import models
