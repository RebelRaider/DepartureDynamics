# Словарь для сообщения об ошибке при регистрации, если адрес электронной почты не уникален
sign_up_email_unique: dict = {
    'status': False,
    'error': 'unique email fail',
    'error_ru': "Почта не уникальна."
}

# Словарь для сообщения об ошибке при регистрации, если имя пользователя не уникально
sign_up_username_unique: dict = {
    'status': False,
    'error': 'unique username fail',
    'error_ru': "Имя пользователя не уникально."
}

# Словарь для общего сообщения об ошибке при регистрации, если данные не уникальны
sign_up_error: dict = {
    'status': False,
    'error': 'unique fail',
    'error_ru': "Данные не уникальны."
}

# Словарь для сообщения об ошибке при входе, если пользователь не найден по электронной почте
sign_in_user_not_found_by_email: dict = {
    'status': False,
    'error': 'not found by email',
    'error_ru': "Пользователь не найден по почте."
}

# Словарь для сообщения об ошибке при входе, если введен неверный пароль
sign_in_wrong_password: dict =  {
    'status': False,
    'error': 'invalid password',
    'error_ru': "Пароль не верный."
}

# Словарь для сообщения об ошибке при создании новой модели, если название модели не уникально
new_model_conflict_name: dict = {
    'status': False,
    'error': 'model name is not unique',
    'error_ru': "Такое имя модели уже используется."
}

# Словарь для сообщения об ошибке при загрузке файла с неподдерживаемым типом
wrong_file_type: dict = {
    'status': False,
    'error': 'wrong file type',
    'error_ru': "Не поддерживаемый тип файла."
}

# Словарь для сообщения об ошибке при создании нового прогноза, если имя прогноза не уникально
new_predict_conflict_name: dict = {
    'status': False,
    'error': 'predict name is not unique',
    'error_ru': "Такое имя уже используется."
}

# Словарь для сообщения об ошибке при обработке почты, если имя разбора почты не уникально
new_parse_mail_conflict_name: dict = {
    'status': False,
    'error': 'parse mail name is not unique',
    'error_ru': "Такое имя уже используется."
}

# Словарь для сообщения об ошибке при запросе обратной связи, если пользователь не админ
user_is_not_admin: dict = {
    'status': False,
    'error': 'user is not admin',
    'error_ru': "Пользователь не является администратором."
}