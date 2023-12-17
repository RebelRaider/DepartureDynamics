from api import models
from datetime import datetime
from api import utils
from api.models import User
import jwt
import os
from api import exceptions
from api import schemas

user_folders = [
    'train_files', 'models', 'predict_files', 'predictions', 'data_for_parse', 'data_from_parse'
]

async def create_user_folder(username: str):
    """
    Создает папку для пользователя и подпапки для хранения данных.

    Parameters:
    - username (str): Имя пользователя.

    Returns:
    - None
    """
    user_data = os.path.join('static', 'userdata', username)
    os.mkdir(user_data)
    for folder in user_folders:
        os.mkdir(os.path.join(user_data, folder))

     
async def create_user(username: str,
                      first_name: str,
                      last_name: str,
                      email: str,
                      password: str):
    """
    Создает нового пользователя в базе данных и соответствующую папку для хранения данных.

    Parameters:
    - username (str): Имя пользователя.
    - first_name (str): Имя пользователя.
    - last_name (str): Фамилия пользователя.
    - email (str): Электронная почта пользователя.
    - password (str): Пароль пользователя.

    Returns:
    - dict: Возвращает статус регистрации и идентификатор пользователя, если успешно, или словарь с ошибкой.
    """
    if not await utils.check_email_unique(email, User):
        return exceptions.sign_up_email_unique
    if not await utils.check_username_unique(username, User):
        return exceptions.sign_up_username_unique
    user = models.User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password='allelleo',
        is_admin=False
    )
    await user.set_password(password=password)
    user.created_date = datetime.now()
    user.updated_date = datetime.now()

    try:
        await user.save()
        await create_user_folder(user.username)
    except:
        return exceptions.sign_up_error
    return {
        'status': True,
        'user_id': user.id
    }
    
async def sign_in(email: str, password: str):
    """
    Авторизует пользователя.

    Parameters:
    - email (str): Электронная почта пользователя.
    - password (str): Пароль пользователя.

    Returns:
    - dict: Возвращает токен аутентификации, если успешно, или словарь с ошибкой.
    """
    if not await User.objects.filter(email=email).exists():
        return exceptions.sign_in_user_not_found_by_email
    user = await User.objects.get(email=email)
    if await user.check_password(password):
        return {
            "token": jwt.encode({
                'user_id': user.id
            }, 'allelleo', algorithm='HS256')
        }
    return exceptions.sign_in_wrong_password

async def reset_password(user, old: str, new: str) -> schemas.ResetPasswordReturn:
    """
    Сбрасывает пароль пользователя.

    Parameters:
    - user (User): Объект пользователя.
    - old (str): Старый пароль пользователя.
    - new (str): Новый пароль пользователя.

    Returns:
    - dict: Возвращает статус сброса пароля или словарь с ошибкой.
    """
    if await user.check_password(old):
        await user.set_password(new)
        await user.update()
        return {
            'status': True
        }
    return exceptions.sign_in_wrong_password

async def create_new_model(user, save_to, model_name, model_path, mode='simple'):
    """
    Создает новую модель и записывает ее в базу данных.

    Parameters:
    - user (User): Объект пользователя.
    - save_to (str): Путь к данным модели.
    - model_name (str): Имя новой модели.
    - model_path (str): Путь для сохранения модели.
    - mode (str): Режим создания модели (по умолчанию 'simple').

    Returns:
    - None
    """
    user_model = models.UserModels(
        data_path=save_to,
        model_path=str(model_path),
        model_type=mode,
        model_name=model_name,
        user_id=user.id
    )
    user_model.created_date = datetime.now()
    user_model.updated_date = datetime.now()
    
    await user_model.save()

async def inference(user, save_to, predict_name):
    """
    Записывает результаты инференса в базу данных.

    Parameters:
    - user (User): Объект пользователя.
    - save_to (str): Путь к результатам инференса.
    - predict_name (str): Имя предсказания.

    Returns:
    - None
    """
    history = models.UserHistory(
        predict_file=save_to,
        prediction='/' + os.path.join(await user.get_user_folder(), 'predictions', predict_name),
        predict_name=predict_name,
        user_id=user.id
    )
    history.created_date = datetime.now()
    history.updated_date = datetime.now()
    
    await history.save()

async def parse_mail(user, start_date_baseline: datetime,
                    end_date_baseline: datetime, start_date_comparison: datetime,
                    end_date_comparison: datetime,
                    work_start_time_hours: int, work_start_time_minutes: int,
                    work_end_time_hours: int, work_end_time_minutes: int,
                    path_to_save: str, save_to: str):
    """
    Записывает результаты парсинга электронных писем в базу данных.

    Parameters:
    - user (User): Объект пользователя.
    - start_date_baseline (datetime): Начальная дата базового периода для парсинга.
    - end_date_baseline (datetime): Конечная дата базового периода для парсинга.
    - start_date_comparison (datetime): Начальная дата периода для сравнения.
    - end_date_comparison (datetime): Конечная дата периода для сравнения.
    - work_start_time_hours (int): Час начала рабочего времени.
    - work_start_time_minutes (int): Минута начала рабочего времени.
    - work_end_time_hours (int): Час окончания рабочего времени.
    - work_end_time_minutes (int): Минута окончания рабочего времени.
    - path_to_save (str): Путь к результатам парсинга.
    - save_to (str): Путь к данным для парсинга.

    Returns:
    - None
    """
    parse = models.UserParseHistory(
        start_date_baseline=start_date_baseline,
        end_date_baseline=end_date_baseline,
        start_date_comparison=start_date_comparison,
        end_date_comparison=end_date_comparison,
        work_start_time_hours=work_start_time_hours,
        work_start_time_minutes=work_start_time_minutes,
        work_end_time_hours=work_end_time_hours,
        work_end_time_minutes=work_end_time_minutes,
        path_to_save=path_to_save,
        save_to=save_to,
        user_id=user.id
    )
    parse.created_date = datetime.now()
    parse.updated_date = datetime.now()
    
    await parse.save()
