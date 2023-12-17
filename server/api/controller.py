from fastapi import APIRouter, Request, UploadFile, File
from datetime import datetime, time
from pydantic import EmailStr

from api import schemas, exceptions, utils, service
from api.models import User, UserModels, UserHistory, UserParseHistory, FeedBack

import os
from api.inference_catboost import train_catboost, optimize_catboost, inference_catboost  
from api.mail_parse import process_email_accounts
from ormar import QuerySet

controller = APIRouter()

model_exc = 'ckpt'

async def generate_save_path(filename, user: User) -> str:
    """
    Генерирует и возвращает полный путь для сохранения файла, связанного с пользователем.

    Parameters:
    - filename (str): Имя файла, который требуется сохранить.
    - user (User): Объект пользователя, для которого генерируется путь.

    Returns:
    - str: Полный путь для сохранения файла.
    """  
    return os.path.join(await user.get_user_folder(), 'train_files', filename)


@controller.post('/ml/new_model/train')
async def new_model_train(request: Request,
                          token: str,
                          model_name: str,
                          file: UploadFile = File(...))-> schemas.ModelReturn | dict:
    """
    Обучает новую модель на основе загруженного CSV-файла.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - token (str): Токен пользователя для аутентификации.
    - model_name (str): Имя новой модели.
    - file (UploadFile): Загруженный CSV-файл для обучения.

    Returns:
    - ModelReturn | dict: Возвращает данные о результате обучения модели или словарь с ошибкой.
    """  
    if await utils.check_model_name(model_name, UserModels):
        return exceptions.new_model_conflict_name
    if not await utils.check_file_expansion(file.filename, 'csv'):
        return exceptions.wrong_file_type
    
    user: User = await utils.get_user_from_token(token, User)
    save_to: str = await generate_save_path(file.filename, user)
    model_path: str = os.path.join(await user.get_user_folder(), 'models')
    
    with open(save_to, 'wb') as f:
        f.write(file.file.read())
    
    await service.create_new_model(user, save_to, model_name, model_path)
    
    train_catboost(save_to, os.path.join(model_path, model_name))
    
    return {
        'status' : True
    }


@controller.post('/user/auth/sign-up')
async def sign_up(request: Request,
                  username: str = 'username',
                  first_name: str ='first_name',
                  last_name: str = 'last_name',
                  email: EmailStr ='email@email.email',
                  password: str='password') -> schemas.SignUpReturn | dict:
    """
    Регистрирует нового пользователя.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - username (str): Имя пользователя.
    - first_name (str): Имя пользователя.
    - last_name (str): Фамилия пользователя.
    - email (EmailStr): Электронная почта пользователя.
    - password (str): Пароль пользователя.

    Returns:
    - SignUpReturn | dict: Возвращает данные о результате регистрации или словарь с ошибкой.
    """  
    return await service.create_user(username, first_name, last_name, email, password)
    
    
@controller.post('/user/auth/sign-in')
async def sign_in(request: Request, email: EmailStr ='email@email.email',
                  password: str='password') -> schemas.SignInReturn | dict:
    """
    Авторизует пользователя.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - email (EmailStr): Электронная почта пользователя.
    - password (str): Пароль пользователя.

    Returns:
    - SignInReturn | dict: Возвращает данные о результате авторизации или словарь с ошибкой.
    """  
    return await service.sign_in(email, password)


@controller.post('/user/reset_password')
async def reset_password(request: Request,
                         token:str,
                         old: str,
                         new: str) -> schemas.ResetPasswordReturn | dict:
    """
    Сбрасывает пароль пользователя.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - token (str): Токен пользователя для сброса пароля.
    - old (str): Старый пароль пользователя.
    - new (str): Новый пароль пользователя.

    Returns:
    - ResetPasswordReturn | dict: Возвращает данные о результате сброса пароля или словарь с ошибкой.
    """  
    user: User = await utils.get_user_from_token(token, User)
    return await service.reset_password(user, old, new)


    
    
@controller.post('/ml/new_model/optimize')
async def new_model_optimize(request: Request,
                             token: str,
                             model_name: str,
                             file: UploadFile = File(...)) -> schemas.ModelReturn | dict:
    """
    Оптимизирует новую модель на основе загруженного CSV-файла.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - token (str): Токен пользователя для аутентификации.
    - model_name (str): Имя новой модели.
    - file (UploadFile): Загруженный CSV-файл для оптимизации.

    Returns:
    - ModelReturn | dict: Возвращает данные о результате оптимизации модели или словарь с ошибкой.
    """  
    if await utils.check_model_name(model_name, UserModels):
        raise exceptions.new_model_conflict_name
    if not await utils.check_file_expansion(file.filename, 'csv'):
        return exceptions.wrong_file_type
    user: User = await utils.get_user_from_token(token, User)
    save_to: str = await generate_save_path(file.filename, user)
    model_path: str = os.path.join(await user.get_user_folder(), 'models')
    
    with open(save_to, 'wb') as f:
        f.write(file.file.read())
    
    await service.create_new_model(user, save_to, model_name, model_path, mode='optimize')
    
    
    optimize_catboost(save_to, os.path.join(model_path, model_name))
    
    return {
        'status' : True
    }


@controller.post('/inference')
async def inference(request: Request,
                    token: str,
                    model_name: str,
                    predict_name: str,
                    file: UploadFile = File(...)) -> schemas.InferenceReturn:
    """
    Выполняет инференс (предсказание) на новых данных с использованием заданной модели.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - token (str): Токен пользователя для аутентификации.
    - model_name (str): Имя модели, которую необходимо использовать для инференса.
    - predict_name (str): Имя для сохранения результата инференса.
    - file (UploadFile): Загруженный CSV-файл для выполнения предсказания.

    Returns:
    - InferenceReturn: Возвращает данные о результате инференса.
    """
    if await utils.check_predict_name(predict_name, UserHistory):
        raise exceptions.new_predict_conflict_name
    if not await utils.check_file_expansion(file.filename, 'csv'):
        return exceptions.wrong_file_type

    user: User = await utils.get_user_from_token(token, User)
    print(user.id)
    model = None
    for m in await UserModels.objects.all():
        print(F"{m.model_name} {model_name} {m.model_name.strip() == model_name.strip()}")
        if m.model_name.strip() == model_name.strip():
            model = m
            break
    # model: UserModels = await UserModels.objects.get(model_name=model_name)
    save_to: str = os.path.join(await user.get_user_folder(), 'predict_files', file.filename)

    with open(save_to, 'wb') as f:
        f.write(file.file.read())
    mdl = os.path.join(model.model_path, model_name)
    inference_catboost(
        save_to,
        mdl.replace(' ', ''),
        os.path.join(
            await user.get_user_folder(),
            'predictions',
            predict_name
        )
    )

    await service.inference(user, save_to, predict_name)

    return {
        'result': '/' + os.path.join(
            await user.get_user_folder(),
            'predictions',
            predict_name
        ) + '.csv'
    }


@controller.get('/me')
async def me(request: Request, token: str) -> schemas.MeReturn | dict:
    """
    Получает информацию о текущем пользователе.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - token (str): Токен пользователя для аутентификации.

    Returns:
    - MeReturn | dict: Возвращает данные о текущем пользователе или словарь с ошибкой.
    """
    user: User = await utils.get_user_from_token(token, User)
    return await user.json()


@controller.get('/model')
async def models(request: Request, token: str) -> schemas.GetModelReturn | dict:
    """
    Получает информацию о моделях пользователя.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - token (str): Токен пользователя для аутентификации.

    Returns:
    - GetModelReturn | dict: Возвращает данные о моделях пользователя или словарь с ошибкой.
    """
    user: User = await utils.get_user_from_token(token, User)
    user_models: QuerySet = UserModels.objects.filter(user_id=user.id)

    data: list = []
    for model in await user_models.all():
        data.append(await model.json())

    return {
        'models': data
    }


@controller.get('/predict')
async def my_predicts(request: Request, token: str) -> schemas.PredictReturn | dict:
    """
    Получает информацию о предсказаниях пользователя.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - token (str): Токен пользователя для аутентификации.

    Returns:
    - PredictReturn | dict: Возвращает данные о предсказаниях пользователя или словарь с ошибкой.
    """
    user: User = await utils.get_user_from_token(token, User)
    history: QuerySet = await UserHistory.objects.filter(user_id=user.id).all()

    data: list = []
    for h in history:
        data.append(await h.json())

    return {
        'predicts': data
    }


@controller.delete('/model/delete')
async def delete_model(request: Request,
                       token: str,
                       model_name: str) -> schemas.GetModelReturn | dict:
    """
    Удаляет модель пользователя.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - token (str): Токен пользователя для аутентификации.
    - model_name (str): Имя модели, которую необходимо удалить.

    Returns:
    - GetModelReturn | dict: Возвращает данные о моделях пользователя после удаления или словарь с ошибкой.
    """
    user: User = await utils.get_user_from_token(token, User)
    model: QuerySet = await UserModels.objects.get(model_name=model_name)

    if model.user_id == user.id:
        delete_path: str = f"{model.model_path}/{model.model_name}.{model_exc}"
        os.remove(delete_path)
        await model.delete()

    return await models(request, token)


@controller.delete('/predict/delete')
async def delete_prediction(request: Request,
                            token: str,
                            predict_name: str) -> schemas.PredictReturn | dict:
    """
    Удаляет предсказание пользователя.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - token (str): Токен пользователя для аутентификации.
    - predict_name (str): Имя предсказания, которое необходимо удалить.

    Returns:
    - PredictReturn | dict: Возвращает данные о предсказаниях пользователя после удаления или словарь с ошибкой.
    """
    user: User = await utils.get_user_from_token(token, User)
    predict: QuerySet = await UserHistory.objects.get(predict_name=predict_name)

    if predict.user_id == user.id:
        delete_path: str = os.getcwd() + predict.prediction + '.csv'
        os.remove(delete_path)
        await predict.delete()

    return await my_predicts(request, token)


@controller.post('/mail/parse')
async def parse_mail_controller(request: Request,
                                token: str,
                                start_date_baseline: datetime,
                                end_date_baseline: datetime,
                                start_date_comparison: datetime,
                                end_date_comparison: datetime,
                                work_start_time_hours: int,
                                work_start_time_minutes: int,
                                work_end_time_hours: int,
                                work_end_time_minutes: int,
                                path_to_save: str,
                                file: UploadFile = File(...)) -> schemas.ParseMailReturn | dict:
    """
    Выполняет парсинг электронных писем и сохраняет результаты в CSV-файл.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - token (str): Токен пользователя для аутентификации.
    - start_date_baseline (datetime): Начальная дата базового периода для парсинга.
    - end_date_baseline (datetime): Конечная дата базового периода для парсинга.
    - start_date_comparison (datetime): Начальная дата периода для сравнения.
    - end_date_comparison (datetime): Конечная дата периода для сравнения.
    - work_start_time_hours (int): Час начала рабочего времени.
    - work_start_time_minutes (int): Минута начала рабочего времени.
    - work_end_time_hours (int): Час окончания рабочего времени.
    - work_end_time_minutes (int): Минута окончания рабочего времени.
    - path_to_save (str): Путь для сохранения результатов парсинга.
    - file (UploadFile): Загруженный CSV-файл с данными для парсинга.

    Returns:
    - ParseMailReturn | dict: Возвращает данные о сохраненном файле и списке некорректных электронных почт.
    """
    user: User = await utils.get_user_from_token(token, User)

    save_to: str = os.path.join(await user.get_user_folder(), 'data_for_parse', file.filename)
    path_to_save: str = os.path.join(await user.get_user_folder(), 'data_from_parse', path_to_save + '.csv')

    if await utils.check_mail_parse(path_to_save, UserParseHistory, user.id):
        return exceptions.new_parse_mail_conflict_name
    if not await utils.check_file_expansion(file.filename, 'csv'):
        return exceptions.wrong_file_type

    with open(save_to, 'wb') as f:
        f.write(file.file.read())

    res = process_email_accounts(
        start_date_baseline=start_date_baseline,
        end_date_baseline=end_date_baseline,
        start_date_comparison=start_date_comparison,
        end_date_comparison=end_date_comparison,
        work_start_time=time(work_end_time_hours, work_start_time_minutes),
        work_end_time=time(work_end_time_hours, work_end_time_minutes),
        path_to_file=save_to,
        path_to_save=path_to_save
    )

    await service.parse_mail(
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
            user=user
        )
    
    return {
        'file': path_to_save,
        'wrong_emails': res
    }


@controller.get('/history/mail')
async def get_mail_parse(request: Request, token: str) -> schemas.GetHistoryReturn | dict:
    """
    Получает историю выполненных операций парсинга электронных писем пользователя.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - token (str): Токен пользователя для аутентификации.

    Returns:
    - GetHistoryReturn | dict: Возвращает данные об истории парсинга электронных писем пользователя.
    """
    user: User = await utils.get_user_from_token(token, User)

    data: list = []
    obj: QuerySet = await UserParseHistory.objects.filter(user_id=user.id).all()

    for i in obj:
        data.append(await i.json())

    return {
        'result': data
    }


@controller.delete('/mail/delete')
async def delete_mail_parse(request: Request, token: str, name: str) -> schemas.DeleteHistoryReturn | dict:
    """
    Удаляет запись об операции парсинга электронных писем пользователя.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - token (str): Токен пользователя для аутентификации.
    - name (str): Название записи об операции парсинга для удаления.

    Returns:
    - DeleteHistoryReturn | dict: Возвращает статус выполнения операции удаления.
    """
    user: User = await utils.get_user_from_token(token, User)
    data: QuerySet = await UserParseHistory.objects.all()

    for dt in data:
        if name in dt.data_path:
            if dt.user_id == user.id:
                await dt.delete()
                break
                

    return {
        'status': True
    }


@controller.get('/feedback')
async def get_feedbacks(request: Request, token: str) -> schemas.FeedBacks | dict:
    """
    Получение обратной связи для администраторов.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - token (str): Токен пользователя.

    Returns:
    - FeedBacks | dict: Список обратной связи или словарь с ошибкой, если пользователь не является администратором.
    """
    user: User = await utils.get_user_from_token(token, User)
    if not user.is_admin:
        return exceptions.user_is_not_admin
    
    return {'feedbacks': [await item.json() for item in await FeedBack.objects.all()]}


@controller.post('/feedback')
async def create_feedback(request: Request, fio: str, email: str, message: str) -> schemas.FeedBackCreateReturn | dict:
    """
    Создание обратной связи.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - fio (str): ФИО пользователя.
    - email (str): Электронная почта пользователя.
    - message (str): Сообщение пользователя.

    Returns:
    - FeedBackCreateReturn | dict: Словарь с успешным статусом или словарь с ошибкой.
    """
    feed = FeedBack(
        user_fio=fio,
        user_email=email,
        user_message=message
    )
    feed.created_date = datetime.now()
    await feed.save()
    
    return {
        'status': True
    }
    