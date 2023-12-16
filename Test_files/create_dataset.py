from faker import Faker
import pandas as pd
import numpy as np


def create_synthetic_dataset(N, is_test):
    """
    Генерирует синтетический датасет для анализа активности электронной почты.

    Параметры:
    - N (int): Количество записей (наблюдений) в датасете.
    - is_test (bool, по умолчанию False): Флаг, указывающий, создается ли тестовый датасет. 
      Если True, исключает колонку 'Probability of Leaving' из результирующего датасета.

    Возвращаемое значение:
    - pandas.DataFrame: Датасет, содержащий базовые и сравнительные данные для анализа активности электронной почты.

    Структура данных:
    - 'Email': Сгенерированные электронные адреса.
    - 'Sent Messages': Количество отправленных сообщений.
    - 'Received Messages': Количество полученных сообщений.
    - 'Recipients in Sent Messages': Количество получателей в отправленных сообщениях.
    - 'Bcc Recipients in Sent Messages': Количество скрытых получателей (Bcc) в отправленных сообщениях.
    - 'Cc Recipients in Sent Messages': Количество копии (Cc) в отправленных сообщениях.
    - 'Replies to Messages': Количество ответов на сообщения.
    - 'Characters in Outgoing Messages': Общее количество символов в отправленных сообщениях.
    - 'Messages Outside Working Hours': Количество сообщений за пределами рабочего времени.
    - "Bytes Sent": Объем отправленных данных в байтах.
    - "Bytes Received": Объем полученных данных в байтах.
    - 'Unanswered Questions': Количество неотвеченных вопросов.
    - 'Attachments in Sent Messages': Количество вложений в отправленных сообщениях.
    - 'Probability of Leaving': Вероятность ухода (генерируется случайным образом в диапазоне [0, 1]).

    Пример использования:
    
    df = create_synthetic_dataset(1000, is_test=False)

    """
    fake = Faker()
    baseline_data = {
        'Email': [fake.email() for _ in range(N)],
        'Sent Messages (Baseline)':  np.random.randint(5, 200, size=N),
        'Received Messages (Baseline)':  np.random.randint(5, 200, size=N),
        'Recipients in Sent Messages (Baseline)':  np.random.randint(1, 100, size=N),
        'Bcc Recipients in Sent Messages (Baseline)': np.random.randint(0, 20, size=N),
        'Cc Recipients in Sent Messages (Baseline)': np.random.randint(0, 20, size=N),
        'Replies to Messages (Baseline)': np.random.randint(5, 200, size=N),
        'Characters in Outgoing Messages (Baseline)': np.random.randint(100, 10000, size=N),
        'Messages Outside Working Hours (Baseline)': np.random.randint(0, 60, size=N),
        "Bytes Sent (Baseline)" : np.random.randint(5000, 90000000, size=N),
        "Bytes Received (Baseline)": np.random.randint(5000, 90000000, size=N),
        'Unanswered Questions (Baseline)': np.random.randint(1, 85, size=N),
        'Attachments in Sent Messages (Baseline)' : np.random.randint(0, 30, size=N),
        'Probability of Leaving': np.random.randint(0, 2, size=N),
    }
    baseline_df = pd.DataFrame(baseline_data)

    comparison_data = {
        'Sent Messages (Comparison)': (baseline_df['Sent Messages (Baseline)'] * (1 - 0.15 * baseline_df['Probability of Leaving']) * (1 + np.random.normal(loc=0, scale=0.3, size=N))).astype(int),
        'Received Messages (Comparison)': (baseline_df['Received Messages (Baseline)'] * (1 - 0.18 * baseline_df['Probability of Leaving']) * (1 + np.random.normal(loc=0, scale=0.3, size=N))).astype(int),
        'Recipients in Sent Messages (Comparison)': (baseline_df['Recipients in Sent Messages (Baseline)'] * (1 - 0.2 * baseline_df['Probability of Leaving']) * (1 + np.random.normal(loc=0, scale=0.25, size=N))).astype(int),
        'Bcc Recipients in Sent Messages (Comparison)': (baseline_df['Bcc Recipients in Sent Messages (Baseline)'] * (1 - 0.22 * baseline_df['Probability of Leaving']) * (1 + np.random.normal(loc=0, scale=0.25, size=N))).astype(int),
        'Cc Recipients in Sent Messages (Comparison)': (baseline_df['Cc Recipients in Sent Messages (Baseline)'] * (1 - 0.2 * baseline_df['Probability of Leaving']) * (1 + np.random.normal(loc=0, scale=0.3, size=N))).astype(int),
        'Replies to Messages (Comparison)': (baseline_df['Replies to Messages (Baseline)'] * (1 - 0.15 * baseline_df['Probability of Leaving']) * (1 + np.random.normal(loc=0, scale=0.2, size=N))).astype(int),
        'Characters in Outgoing Messages (Comparison)': (baseline_df['Characters in Outgoing Messages (Baseline)'] * (1 - 0.18 * baseline_df['Probability of Leaving']) * (1 + np.random.normal(loc=0, scale=0.33, size=N))).astype(int),
        'Messages Outside Working Hours (Comparison)': (baseline_df['Messages Outside Working Hours (Baseline)'] * (1 - 0.15 * baseline_df['Probability of Leaving']) * (1 + np.random.normal(loc=0, scale=0.35, size=N))).astype(int),
        "Bytes Sent (Comparison)" : (baseline_df['Bytes Sent (Baseline)'] * (1 - 0.2 * baseline_df['Probability of Leaving']) * (1 + np.random.normal(loc=0, scale=0.25, size=N))).astype(int),
        "Bytes Received (Comparison)": (baseline_df['Bytes Received (Baseline)'] * (1 - 0.18 * baseline_df['Probability of Leaving']) * (1 + np.random.normal(loc=0, scale=0.2, size=N))).astype(int),
        'Unanswered Questions (Comparison)': (baseline_df['Unanswered Questions (Baseline)'] * (1 - 0.15 * baseline_df['Probability of Leaving']) * (1 + np.random.normal(loc=0, scale=0.4, size=N))).astype(int),
        'Attachments in Sent Messages (Comparison)': (baseline_df['Attachments in Sent Messages (Baseline)'] * (1 - 0.2 * baseline_df['Probability of Leaving']) * (1 + np.random.normal(loc=0, scale=0.5, size=N))).astype(int),
    }
    comparison_df = pd.DataFrame(comparison_data)

    df = pd.concat([baseline_df, comparison_df], axis=1)
    if is_test:
        df.drop("Probability of Leaving", inplace=True, axis=1)
    return df

# Пример использования
df_train = create_synthetic_dataset(40000, False)
df_train.to_csv("synthetic_dataset.csv", index=False)

df_test = create_synthetic_dataset(5000, True)
df_test.to_csv("synthetic_dataset_test.csv", index=False)
