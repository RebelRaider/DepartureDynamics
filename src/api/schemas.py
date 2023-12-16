import pydantic
import datetime


class SignUpReturn(pydantic.BaseModel):
    """
    Класс Pydantic для структуры данных, возвращаемых при успешной регистрации.

    Содержит поля:
    - status: булево значение, указывающее на успешность операции.
    - user_id: целое число, идентификатор пользователя.
    """ 
    status: bool
    user_id: int


class SignInReturn(pydantic.BaseModel):
    """
    Класс Pydantic для структуры данных, возвращаемых при успешном входе.

    Содержит поле:
    - token: строка, предположительно, токен для аутентификации.
    """
    token: str


class ResetPasswordReturn(pydantic.BaseModel):
    """
    Класс Pydantic для структуры данных, возвращаемых при сбросе пароля.

    Содержит поле:
    - status: булево значение, указывающее на успешность операции.
    """
    status: bool


class ErrorModel(pydantic.BaseModel):
    """
    Класс Pydantic для структуры данных сообщений об ошибках.

    Содержит поля:
    - status: булево значение, указывающее на успешность операции.
    - error: строка, описание ошибки.
    - error_ru: строка на русском языке, описание ошибки.
    """
    status: bool = False
    error: str
    error_ru: str


class ModelReturn(pydantic.BaseModel):
    """
    Класс Pydantic для структуры данных возвращаемых значений, связанных с моделями.

    Содержит поле:
    - status: булево значение, указывающее на успешность операции.
    """
    status: bool


class InferenceReturn(pydantic.BaseModel):
    """
    Класс Pydantic для структуры данных возвращаемых значений результатов вывода (inference).

    Содержит поле:
    - result: строка, представляющая результат вывода.
    """
    result: str


class MeReturn(pydantic.BaseModel):
    """
    Класс Pydantic для структуры данных возвращаемых значений, связанных с данными о пользователе.

    Содержит поля:
    - id: целое число, идентификатор пользователя.
    - created: объект datetime.datetime, дата и время создания пользователя.
    - username: строка, имя пользователя.
    - first_name: строка, имя пользователя.
    - last_name: строка, фамилия пользователя.
    - email: pydantic.EmailStr, адрес электронной почты пользователя.
    """
    id: int
    created: datetime.datetime
    username: str
    first_name: str
    last_name: str
    email: pydantic.EmailStr


class ModelModel(pydantic.BaseModel):
    """
    Класс Pydantic для структуры данных представления модели.

    Содержит поля:
    - id: целое число, идентификатор модели.
    - created: объект datetime.datetime, дата и время создания модели.
    - model_type: строка, тип модели.
    - model_name: строка, имя модели.
    """
    id: int
    created: datetime.datetime
    model_type: str
    model_name: str


class GetModelReturn(pydantic.BaseModel):
    """
    Класс Pydantic для структуры данных возвращаемых значений, связанных с получением моделей.

    Содержит поле:
    - models: список объектов ModelModel, представляющих информацию о моделях.
    """
    models: list[ModelModel]


class PredictModel(pydantic.BaseModel):
    """
    Класс Pydantic для структуры данных представления прогноза (predict).

    Содержит поля:
    - id: целое число, идентификатор прогноза.
    - created: объект datetime.datetime, дата и время создания прогноза.
    - predict_file: строка, имя файла прогноза.
    - prediction: строка, описание прогноза.
    - predict_name: строка, имя прогноза.
    """
    id: int
    created: datetime.datetime
    predict_file: str
    prediction: str
    predict_name: str


class PredictReturn(pydantic.BaseModel):
    """
    Класс Pydantic для структуры данных возвращаемых значений, связанных с прогнозами.

    Содержит поле:
    - predicts: список объектов PredictModel, представляющих информацию о прогнозах.
    """
    predicts: list[PredictModel]


class FeedBackCreateReturn(ModelReturn):
    """
    Подкласс ModelReturn для возвращаемых значений, связанных с созданием обратной связи.

    Содержит поле:
    - status: булево значение, указывающее на успешность операции.
    """
    pass

class ParseMailReturn(pydantic.BaseModel):
    """
    Класс Pydantic для структуры данных возвращаемых значений, связанных с парсингом почты.

    Содержит поля:
    - file: строка, имя файла.
    - wrong_emails: список строк, содержащих неверные адреса электронной почты.
    """
    file:str
    wrong_emails: list[str]
    
class Feed(pydantic.BaseModel):
    """
    Класс Pydantic для структуры данных представления обратной связи.

    Содержит поля:
    - id: целое число, идентификатор обратной связи.
    - created: объект datetime.datetime, дата и время создания обратной связи.
    - user_fio: строка, ФИО пользователя.
    - user_email: строка, электронная почта пользователя.
    - user_message: строка, сообщение пользователя.
    """
    id: int
    created: datetime.datetime
    user_fio: str
    user_email: str
    user_message: str
    
class FeedBacks(pydantic.BaseModel):
    """
    Класс Pydantic для структуры данных возвращаемых значений, связанных с обратной связью.

    Содержит поле:
    - feedbacks: список объектов Feed, представляющих информацию об обратной связи.
    """
    feedbacks: list[Feed]
    

class HistoryModel(pydantic.BaseModel):
    """
    Класс Pydantic для структуры данных представления истории прогнозов.

    Содержит поля:
    - id: целое число, идентификатор записи истории.
    - created: объект datetime.datetime, дата и время создания записи.
    - predict_file: строка, имя файла прогноза.
    - prediction: строка, описание прогноза.
    - predict_name: строка, имя прогноза.
    """
    id: int
    created: datetime.datetime
    predict_file: str
    prediction: str
    predict_name: str
    
class GetHistoryReturn(pydantic.BaseModel):
    """
    Класс Pydantic для структуры данных возвращаемых значений, связанных с получением истории.

    Содержит поле:
    - result: список объектов HistoryModel, представляющих информацию о записях истории.
    """
    result: list[HistoryModel]
    
class DeleteHistoryReturn(ModelReturn):
    """
    Подкласс ModelReturn для возвращаемых значений, связанных с удалением записей истории.
    Содержит поле:
    - status: булево значение, указывающее на успешность операции.
    """
    pass