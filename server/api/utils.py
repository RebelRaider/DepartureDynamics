import jwt


async def check_username_unique(username: str, user: object) -> bool:
    """
    Проверяет уникальность имени пользователя.

    :param username: Имя пользователя для проверки.
    :param user: Объект пользователя для взаимодействия с базой данных.
    :return: True, если имя уникально, в противном случае - False.
    """
    return not await user.objects.filter(username=username).exists()


async def check_email_unique(email: str, user: object) -> bool:
    """
    Проверяет уникальность электронной почты.

    :param email: Адрес электронной почты для проверки.
    :param user: Объект пользователя для взаимодействия с базой данных.
    :return: True, если адрес уникален, в противном случае - False.
    """
    return not await user.objects.filter(email=email).exists()


async def get_user_from_token(token: str, user: object):
    """
    Получает пользователя по токену.

    :param token: Токен для декодирования.
    :param user: Объект пользователя для взаимодействия с базой данных.
    :return: Объект пользователя, соответствующий идентификатору из токена.
    """
    payload = jwt.decode(token, 'allelleo', algorithms=['HS256'])
    user_id = payload.get('user_id')
    return await user.objects.get_or_none(id=user_id)


async def check_model_name(model_name: str, Model) -> bool:
    """
    Проверяет уникальность названия модели.

    :param model_name: Название модели для проверки.
    :param Model: Класс модели для взаимодействия с базой данных.
    :return: True, если модель с таким названием уже существует, в противном случае - False.
    """
    return await Model.objects.filter(model_name=model_name).exists()


async def check_predict_name(predict_name: str, Model) -> bool:
    """
    Проверяет уникальность названия прогноза.

    :param predict_name: Название прогноза для проверки.
    :param Model: Класс модели для взаимодействия с базой данных.
    :return: True, если прогноз с таким названием уже существует, в противном случае - False.
    """
    return await Model.objects.filter(predict_name=predict_name).exists()


async def check_mail_parse(path_to_save: str, Model, user_id: int):
    """
    Проверяет наличие файла с указанным путем для конкретного пользователя и модели.

    :param path_to_save: Путь к сохраненным данным.
    :param Model: Класс модели для взаимодействия с базой данных.
    :param user_id: Идентификатор пользователя.
    :return: True, если путь совпадает с одним из путей данных модели, в противном случае - False.
    """
    return any(path_to_save in model.data_path for model in await Model.objects.filter(user_id=user_id).all())


async def check_file_expansion(filename: str, expansion: str):
    """
    Проверяет расширение файла.

    :param filename: Имя файла для проверки.
    :param expansion: Ожидаемое расширение файла.
    :return: True, если расширение совпадает, в противном случае - False.
    """
    return filename.endswith(expansion)