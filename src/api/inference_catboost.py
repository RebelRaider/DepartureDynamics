from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import train_test_split
import pandas as pd
import optuna
from sklearn.metrics import roc_auc_score
import numpy as np

def get_statistic_from_data(df, is_test):
    """
    Генерирует статистический отчет на основе предоставленных данных.

    Аргументы:
    - df (pd.DataFrame): Исходный DataFrame с данными, содержащими информацию о электронных сообщениях.
    - is_test (bool): Флаг, указывающий, являются ли предоставленные данные тестовыми. 
                     Если True, то в результирующем DataFrame будет отсутствовать информация о вероятности ухода.

    Возвращает:
    - pd.DataFrame: Новый DataFrame, содержащий статистические показатели, вычисленные на основе предоставленных данных.
                    В случае, если is_test равно False, будет также включена информация о вероятности ухода.

    Примечание:
    - Для избежания деления на ноль в отношениях, в случае нулевого значения в знаменателе будет установлено значение 0.
    
    Пример использования:
    ```python
    data = pd.read_csv('data.csv')
    result = get_statistic_from_data(data, is_test=True)
    ```
    """
    new_data = {
    'Email': df['Email'],
    'Change in Sent Messages': df['Sent Messages (Comparison)'] - df['Sent Messages (Baseline)'],
    'Change in Received Messages': df['Received Messages (Comparison)'] - df['Received Messages (Baseline)'],
    'Change in Recipients in Sent Messages': df['Recipients in Sent Messages (Comparison)'] - df['Recipients in Sent Messages (Baseline)'],
    'Change in Bcc Recipients in Sent Messages': df['Bcc Recipients in Sent Messages (Comparison)'] - df['Bcc Recipients in Sent Messages (Baseline)'],
    'Change in Cc Recipients in Sent Messages': df['Cc Recipients in Sent Messages (Comparison)'] - df['Cc Recipients in Sent Messages (Baseline)'],
    'Change in Replies to Messages': df['Replies to Messages (Comparison)'] - df['Replies to Messages (Baseline)'],
    'Change in Characters in Outgoing Messages': df['Characters in Outgoing Messages (Comparison)'] - df['Characters in Outgoing Messages (Baseline)'],
    'Change in Messages Outside Working Hours': df['Messages Outside Working Hours (Comparison)'] - df['Messages Outside Working Hours (Baseline)'],
    'Change in Unanswered Questions': df['Unanswered Questions (Comparison)'] - df['Unanswered Questions (Baseline)'],
    'Change in Attachments in Sent Messages': df['Attachments in Sent Messages (Comparison)'] - df['Attachments in Sent Messages (Baseline)'],

    'Ratio of Sent Messages': np.where(df['Sent Messages (Baseline)'] != 0, df['Sent Messages (Comparison)'] / df['Sent Messages (Baseline)'], 0),
    'Ratio of Received Messages': np.where(df['Received Messages (Baseline)'] != 0, df['Received Messages (Comparison)'] / df['Received Messages (Baseline)'], 0),
    'Ratio of Characters in Outgoing Messages': np.where(df['Characters in Outgoing Messages (Baseline)'] != 0, df['Characters in Outgoing Messages (Comparison)'] / df['Characters in Outgoing Messages (Baseline)'], 0),
    'Ratio of Attachments in Sent Messages': np.where(df['Attachments in Sent Messages (Baseline)'] != 0, df['Attachments in Sent Messages (Comparison)'] / df['Attachments in Sent Messages (Baseline)'], 0),
    'Ratio of Bytes Sent' : np.where(df['Bytes Sent (Baseline)'] !=0, df['Bytes Sent (Comparison)'] / df['Bytes Sent (Baseline)'], 0),
    'Ratio of Bytes Received': np.where(df['Bytes Received (Baseline)'] != 0, df['Bytes Received (Comparison)'] / df['Bytes Received (Baseline)'], 0),

}
    new_df = pd.DataFrame(new_data)
    if not is_test:
        new_df['Probability of Leaving'] = df['Probability of Leaving']
    return new_df


def train_catboost(file_name, model_name):
    """
    Обучает модель CatBoost на предоставленных данных и сохраняет ее в файл.

    :param file_name: Имя файла с данными для обучения.
    :param model_name: Имя файла для сохранения обученной модели.
    """
    data = pd.read_csv(file_name)
    data = get_statistic_from_data(data, is_test=False)
    data = data.drop(['Email'], axis=1)

    X = data.drop(['Probability of Leaving'], axis=1)
    y = data['Probability of Leaving']

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)


    train = Pool(
        data=X_train.values,
        label=y_train.values,
        feature_names=X_train.columns.to_list()
    )

    val = Pool(
        data=X_val.values,
        label=y_val.values,
        feature_names=X_val.columns.to_list()
    )

    parameters = {
        
        'verbose': False,
        'iterations': 1000,
}
    model = CatBoostClassifier(**parameters)
    model = model.fit(
            train,
            eval_set=val,
            use_best_model=True,
            metric_period=50
            )
    model.save_model(f'{model_name}.ckpt')


def inference_catboost(file_name, model_name, output_file_name):
    """
    Проводит предсказания с использованием обученной модели CatBoost и сохраняет результаты в CSV-файл.

    :param file_name: Имя файла с данными для предсказания.
    :param model_name: Имя файла с сохраненной моделью CatBoost.
    :param output_file_name: Имя файла для сохранения результатов предсказания в формате CSV.
    :return: Имя созданного CSV-файла.
    """
    df = pd.read_csv(file_name)
    df = get_statistic_from_data(df, is_test=True)
    
    email_data = df[['Email']]
    df = df.drop(['Email'], axis=1)

    model = CatBoostClassifier()
    model.load_model(f'{model_name}.ckpt')
    
    predict_pool = Pool(
        data=df.values,
        feature_names=df.columns.to_list()
    )

    predictions = model.predict_proba(predict_pool)[:, 1]

    email_data['predict'] = predictions

    email_data.to_csv(f'{output_file_name}.csv', index=False)

    return f'{output_file_name}.csv'


def objective(trial, X, y, X_val, y_val):
    """
    Целевая функция для оптимизации параметров модели XGBoost с использованием Optuna.

    :param trial: Объект Trial для оптимизации гиперпараметров.
    :param X: Обучающие признаки.
    :param y: Целевая переменная обучающей выборки.
    :param X_val: Валидационные признаки.
    :param y_val: Целевая переменная валидационной выборки.
    :return: Значение ROC AUC для текущих гиперпараметров.
    """
    train = Pool(
        data=X.values,
        label=y.values,
        feature_names=X.columns.to_list()
    )

    val = Pool(
        data=X_val.values,
        label=y_val.values,
        feature_names=X_val.columns.to_list()
    )

    parameters = {
        'iterations': 1000,
        'depth': trial.suggest_int('depth', 4, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'random_strength': trial.suggest_float('random_strength', 1e-9, 10, log=True),
        'bagging_temperature': trial.suggest_float('bagging_temperature', 0.0001, 1.0, log=True),
        'border_count': trial.suggest_int('border_count', 32, 255),
        'verbose': False,
    }

    model = CatBoostClassifier(**parameters)
    model.fit(train, eval_set=val, use_best_model=True, metric_period=50)
    predictions = model.predict_proba(X_val)[:, 1]
    roc_auc = roc_auc_score(y_val, predictions)

    return roc_auc


def optimize_catboost(file_name, model_name):
    """
    Оптимизирует гиперпараметры модели CatBoost с использованием Optuna и сохраняет оптимальную модель.

    :param file_name: Имя файла с данными для оптимизации.
    :param model_name: Имя файла для сохранения оптимальной модели.
    """
    data = pd.read_csv(file_name)
    data = get_statistic_from_data(data, is_test=False)    
    data = data.drop(['Email'], axis=1)

    X = data.drop(['Probability of Leaving'], axis=1)
    y = data['Probability of Leaving']

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, X_train, y_train, X_val, y_val), n_trials=75)

    best_params = study.best_params
    best_params['verbose'] = False
    best_params['iterations'] = 1000

    print(f"Best Hyperparameters: {best_params}")

    
    train = Pool(
        data=X_train.values,
        label=y_train.values,
        feature_names=X_train.columns.to_list()
    )

    val = Pool(
        data=X_val.values,
        label=y_val.values,
        feature_names=X_val.columns.to_list()
    )

    model = CatBoostClassifier(**best_params)
    model.fit(
        train,
        eval_set=val,
        use_best_model=True,
        metric_period=50
    )

    model.save_model(f'{model_name}.ckpt')