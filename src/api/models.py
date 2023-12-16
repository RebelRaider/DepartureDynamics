from ormar import String, Integer, ForeignKey, Boolean, Model, DateTime, ManyToMany, Date
from db import BaseMeta
import datetime, bcrypt, os

class FeedBack(Model):
    """
    Модель обратной связи.

    Attributes:
        id (int): Уникальный идентификатор обратной связи.
        created_date (datetime.datetime): Дата и время создания обратной связи.
        user_fio (str): ФИО пользователя, оставившего обратную связь.
        user_email (str): Электронная почта пользователя.
        user_message (str): Сообщение пользователя.

    Methods:
        async def json(self) -> dict:
            Возвращает словарь с данными модели в формате JSON.
    """
    id: int = Integer(primary_key=True)
    created_date: datetime.datetime = DateTime(default=datetime.datetime.now)
    user_fio = String(max_length=255)
    user_email = String(max_length=255)
    user_message = String(max_length=1000)
    
    async def json(self):
        """
        Возвращает словарь с данными модели в формате JSON.

        Returns:
            dict: Словарь с данными модели.
        """
        return {
            'id': self.id,
            'created': self.created_date,
            'user_fio': self.user_fio,
            'user_email': self.user_email,
            'user_message': self.user_message
        }
    class Meta(BaseMeta):
        """
        Метакласс для определения настроек таблицы базы данных для модели FeedBack.
        """
        tablename = 'feedback'
        
    

class UserModels(Model):
    """
    Класс, представляющий модели пользователя.

    Содержит информацию о моделях, связанных с пользователем.
    """

    id: int = Integer(primary_key=True)
    created_date: datetime.datetime = DateTime(default=datetime.datetime.now)
    updated_date: datetime.datetime = DateTime(default=datetime.datetime.now)
    
    model_type = String(max_length=100)
    data_path = String(max_length=100)
    
    model_name = String(max_length=100)

    model_path = String(max_length=100)
    
    user_id = Integer()

    class Meta(BaseMeta):
        """
        Метакласс для определения настроек таблицы базы данных для модели UserModels.
        """
        tablename = 'models'
    
    async def json(self):
        """
        Преобразует объект UserModels в словарь.

        :return: Словарь с данными объекта UserModels.
        """
        return {
            'id': self.id,
            'created': self.created_date,
            'model_type': self.model_type,
            'model_name': self.model_name
        }

class UserHistory(Model):
    """
    Класс, представляющий историю пользователя.

    Содержит информацию об истории действий пользователя.
    """

    id: int = Integer(primary_key=True)
    created_date: datetime.datetime = DateTime(default=datetime.datetime.now)
    updated_date: datetime.datetime = DateTime(default=datetime.datetime.now)
    
    predict_file = String(max_length=200)
    prediction = String(max_length=200)
    predict_name = String(max_length=200)
    
    user_id = Integer()

    class Meta(BaseMeta):
        """
        Метакласс для определения настроек таблицы базы данных для модели UserHistory.
        """
        tablename = 'history'
        
    async def json(self):
        """
        Преобразует объект UserHistory в словарь.

        :return: Словарь с данными объекта UserHistory.
        """
        return {
            'id': self.id,
            'created': self.created_date,
            'predict_file': '/' + self.predict_file,
            'prediction': self.prediction,
            'predict_name': self.predict_name +'.csv'
        }

class UserParseHistory(Model):
    """
    Класс, представляющий историю разбора данных пользователя.

    Содержит информацию о процессе разбора данных.
    """

    id: int = Integer(primary_key=True)
    created_date: datetime.datetime = DateTime(default=datetime.datetime.now)
    updated_date: datetime.datetime = DateTime(default=datetime.datetime.now)
    
    start_date_baseline = Date()
    end_date_baseline = Date()
    
    start_date_comparison = Date()
    end_date_comparison = Date()
    
    work_start_time_hours = Integer()
    work_start_time_minutes = Integer()
    
    work_end_time_hours = Integer()
    work_end_time_minutes = Integer()
    
    data_path = String(max_length=200)
    save_to = String(max_length=200)
    
    user_id = Integer()

    class Meta(BaseMeta):
        """
        Метакласс для определения настроек таблицы базы данных для модели UserParseHistory.
        """
        tablename = 'parse_history'
        
    async def json(self):
        """
        Преобразует объект UserParseHistory в словарь.

        :return: Словарь с данными объекта UserParseHistory.
        """
        return {
            'id': self.id,
            'created': self.created_date,
            'start_date_baseline': self.start_date_baseline,
            'end_date_baseline': self.end_date_baseline,
            'start_date_comparison': self.start_date_comparison,
            'end_date_comparison': self.end_date_comparison,
            'work_start_hours': self.work_start_time_hours,
            'work_start_minutes': self.work_start_time_minutes,
            'work_end_hours': self.work_end_time_hours,
            'work_end_minutes': self.work_end_time_minutes,
            'data_path': self.data_path,
            'save_to': self.save_to
        }


class User(Model):
    """
    Класс, представляющий пользователя.

    Содержит информацию о пользователе и методы для работы с учетной записью.
    """

    id: int = Integer(primary_key=True)
    created_date: datetime.datetime = DateTime(default=datetime.datetime.now)
    updated_date: datetime.datetime = DateTime(default=datetime.datetime.now)

    is_admin = Boolean(default=False)
    
    username = String(max_length=100, unique=True)
    first_name = String(max_length=100)
    last_name = String(max_length=100)
    email = String(max_length=100, unique=True)
    
    password = String(max_length=255)
    
    async def set_password(self, password: str) -> None:
        """
        Устанавливает пароль пользователя.

        :param password: Новый пароль.
        """
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    async def check_password(self, password: str) -> bool:
        """
        Проверяет соответствие введенного пароля текущему паролю пользователя.

        :param password: Пароль для проверки.
        :return: True, если пароль верен, в противном случае - False.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    class Meta(BaseMeta):
        """
        Метакласс для определения настроек таблицы базы данных для модели User.
        """
        tablename = 'users_db'
    
    async def get_user_folder(self):
        """
        Возвращает путь к папке пользователя.

        :return: Путь к папке пользователя.
        """
        return os.path.join('static', 'userdata', self.username)

    async def json(self):
        """
        Преобразует объект User в словарь.

        :return: Словарь с данными объекта User.
        """
        return {
            'id': self.id,
            'created': self.created_date,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }
