import imaplib
import pandas as pd
from email import message_from_bytes
from email.header import decode_header
from datetime import datetime
from collections import Counter
from email.utils import parsedate_tz, mktime_tz


def get_message_size(msg):
    """
    Возвращает размер сообщения, включая его вложения.

    Parameters:
    - msg (email.message.Message): Объект сообщения.

    Returns:
    - int: Размер сообщения в байтах.
    """
    size = len(msg.as_bytes())
    for part in msg.walk():
        if part.get_payload(decode=True) is not None:
            size += len(part.as_bytes())
    return size


def get_text_content(msg):
    """
    Извлекает текстовое содержимое из сообщения.

    Parameters:
    - msg (email.message.Message): Объект сообщения.

    Returns:
    - str: Текстовое содержимое сообщения.
    """
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                return part.get_payload(decode=True).decode('utf-8', 'ignore')
    else:
        return msg.get_payload(decode=True).decode('utf-8', 'ignore')


def handle_mailbox_error(folder_name, status):
    """
    Обрабатывает ошибку выбора почтовой папки.

    Parameters:
    - folder_name (str): Имя папки.
    - status (str): Статус ошибки.

    Returns:
    - None
    """
    print(f"Не удалось выбрать папку '{folder_name}'. Код ошибки: {status}")
    return None


def parse_email(email_address, password, start_date, end_date, work_start_time, work_end_time):
    """
    Анализирует электронную почту пользователя и возвращает статистику использования.

    Parameters:
    - email_address (str): Адрес электронной почты пользователя.
    - password (str): Пароль для доступа к электронной почте.
    - start_date (datetime): Начальная дата для анализа сообщений.
    - end_date (datetime): Конечная дата для анализа сообщений.
    - work_start_time (datetime.time): Начальное время рабочего дня.
    - work_end_time (datetime.time): Конечное время рабочего дня.

    Returns:
    - dict: Словарь с результатами анализа электронной почты.
    """
    result_dict = {
        "Email": email_address,
        "Sent Messages": 0,
        "Received Messages": 0,
        "Recipients in Sent Messages": 0,
        "Bcc Recipients in Sent Messages": 0,
        "Cc Recipients in Sent Messages": 0,
        "Replies to Messages": 0,
        "Characters in Outgoing Messages": 0,
        "Messages Outside Working Hours": 0,
        "Bytes Sent" : 0,
        "Bytes Received": 0,
        "Unanswered Questions": 0,
        "Attachments in Sent Messages": 0,
    }

    with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
        mail.login(email_address, password)
        
        start_date_str = start_date.strftime("%d-%b-%Y")
        end_date_str = end_date.strftime("%d-%b-%Y")

        date_search_query = f'(SINCE "{start_date_str}" BEFORE "{end_date_str}")'

        status, _ = mail.select('[Gmail]/&BB4EQgQ,BEAEMAQyBDsENQQ9BD0ESwQ1-') #Sent
        if status != 'OK':
            return handle_mailbox_error('Sent', status)
        
        sent_result, sent_data = mail.search(None, date_search_query)
        
        if sent_result != 'OK':
            print(f"Ошибка при поиске отправленных сообщений: {sent_result}")
            return None
        sent_message_numbers = sent_data[0].split()
        result_dict["Sent Messages"] = len(sent_message_numbers)

        recipients_counter = Counter()
        bcc_recipients_counter = Counter()
        cc_recipients_counter = Counter()
        
        for num in sent_message_numbers:
            try:
                _, sent_msg_data = mail.fetch(num, '(RFC822)')
                sent_msg = message_from_bytes(sent_msg_data[0][1])
                
                result_dict["Bytes Sent"] += get_message_size(sent_msg)
                
                date_str = sent_msg["Date"]
                timestamp = mktime_tz(parsedate_tz(date_str))
                sent_time = datetime.utcfromtimestamp(timestamp).time()

                if not (work_start_time <= sent_time <= work_end_time):
                    result_dict["Messages Outside Working Hours"] += 1

                to_address = sent_msg.get("To", "")
                if to_address:
                    recipients_counter.update(to_address.split(","))
                    
                cc_address = sent_msg.get("Cc", "")
                if cc_address:
                    cc_recipients_counter.update(cc_address.split(","))

                bcc_address = sent_msg.get("Bcc", "")
                if bcc_address:
                    bcc_recipients_counter.update(bcc_address.split(","))
                
                if sent_msg.get("In-Reply-To") or sent_msg.get("References"):
                    result_dict["Replies to Messages"] += 1
                
                subject = decode_header(sent_msg.get("Subject", ""))[0][0]
                decoded_subject = subject.decode("utf-8") if isinstance(subject, bytes) else subject
                text_content = get_text_content(sent_msg)
                if sent_msg.is_multipart():
                    for part in sent_msg.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is not None:
                            result_dict["Attachments in Sent Messages"] += 1

                result_dict["Characters in Outgoing Messages"] += len(decoded_subject) + len(text_content)

                
            except Exception as e:
                print(f"Ошибка при получении данных для сообщения {num}: {e}")

        result_dict["Recipients in Sent Messages"] = len(recipients_counter)
        result_dict["Bcc Recipients in Sent Messages"] = len(bcc_recipients_counter)
        result_dict["Cc Recipients in Sent Messages"] = len(cc_recipients_counter)
        

        status, _ = mail.select("inbox")
        if status != 'OK':
            return handle_mailbox_error('inbox', status)
        
        received_result, received_data = mail.search(None, date_search_query)

        if received_result != 'OK':
            print(f"Ошибка при поиске полученных сообщений: {received_result}")
            return None
        received_message_numbers = received_data[0].split()
        result_dict["Received Messages"] = len(received_message_numbers)
        
        for num in received_message_numbers:
            try:
                _, received_msg_data = mail.fetch(num, '(RFC822)')
                received_msg = message_from_bytes(received_msg_data[0][1])
                
                result_dict["Bytes Received"] += get_message_size(received_msg)
                
                text_content = get_text_content(received_msg)

                if text_content and '?' in text_content:
                    if not received_msg.get("In-Reply-To") and not received_msg.get("References"):
                        result_dict["Unanswered Questions"] += 1
            except Exception as e:
                print(f"Ошибка при получении данных для сообщения {num}: {e}")

        
    return result_dict 


def process_email_accounts( start_date_baseline,
                            end_date_baseline,
                            start_date_comparison,
                            end_date_comparison,
                            work_start_time, work_end_time,
                            path_to_save, path_to_file):
    """
    Обрабатывает учетные записи электронной почты и создает сводный отчет.

    :param start_date_baseline: Начальная дата базового периода (строка формата 'ГГГГ-ММ-ДД').
    :param end_date_baseline: Конечная дата базового периода (строка формата 'ГГГГ-ММ-ДД').
    :param start_date_comparison: Начальная дата периода сравнения (строка формата 'ГГГГ-ММ-ДД').
    :param end_date_comparison: Конечная дата периода сравнения (строка формата 'ГГГГ-ММ-ДД').
    :param work_start_time: Начальное время рабочего дня (строка формата 'ЧЧ:ММ').
    :param work_end_time: Конечное время рабочего дня (строка формата 'ЧЧ:ММ').
    :param path_to_save: Путь для сохранения сводного отчета (строка).
    :param path_to_file: Путь к файлу с логинами и паролями для электронной почты (строка).

    :return: Список электронных адресов, для которых не удалось получить данные.
    """
    
    login_password_df = pd.read_csv(path_to_file)
    bad_emails = []
    
    result_df = pd.DataFrame(columns=[
        'Email',
        'Sent Messages (Baseline)',
        'Received Messages (Baseline)',
        'Recipients in Sent Messages (Baseline)',
        'Bcc Recipients in Sent Messages (Baseline)',
        'Cc Recipients in Sent Messages (Baseline)',
        'Replies to Messages (Baseline)',
        'Characters in Outgoing Messages (Baseline)',
        'Messages Outside Working Hours (Baseline)',
        'Bytes Sent (Baseline)',
        'Bytes Received (Baseline)',
        'Unanswered Questions (Baseline)',
        'Attachments in Sent Messages (Baseline)',
        'Sent Messages (Comparison)',
        'Received Messages (Comparison)',
        'Recipients in Sent Messages (Comparison)',
        'Bcc Recipients in Sent Messages (Comparison)',
        'Cc Recipients in Sent Messages (Comparison)',
        'Replies to Messages (Comparison)',
        'Characters in Outgoing Messages (Comparison)',
        'Messages Outside Working Hours (Comparison)',
        'Bytes Sent (Comparison)',
        'Bytes Received (Comparison)',
        'Unanswered Questions (Comparison)',
        'Attachments in Sent Messages (Comparison)'
    ])

    for _, row in login_password_df.iterrows():
        email_address = row['login']
        password = row['password']

        baseline_result = parse_email(  email_address,
                                        password,
                                        start_date_baseline,
                                        end_date_baseline,
                                        work_start_time,
                                        work_end_time)

        comparison_result = parse_email(email_address,
                                        password,
                                        start_date_comparison,
                                        end_date_comparison,
                                        work_start_time,
                                        work_end_time)

        if baseline_result is not None or comparison_result is not None:
            result_df = pd.concat([result_df, pd.DataFrame({
                'Email': [email_address],
                'Sent Messages (Baseline)': baseline_result["Sent Messages"],
                'Received Messages (Baseline)': baseline_result["Received Messages"],
                'Recipients in Sent Messages (Baseline)': baseline_result["Recipients in Sent Messages"],
                'Bcc Recipients in Sent Messages (Baseline)': baseline_result["Bcc Recipients in Sent Messages"],
                'Cc Recipients in Sent Messages (Baseline)': baseline_result["Cc Recipients in Sent Messages"],
                'Replies to Messages (Baseline)': baseline_result["Replies to Messages"],
                'Characters in Outgoing Messages (Baseline)': baseline_result["Characters in Outgoing Messages"],
                'Messages Outside Working Hours (Baseline)': baseline_result["Messages Outside Working Hours"],
                "Bytes Sent (Baseline)": baseline_result["Bytes Sent"],
                "Bytes Received (Baseline)": baseline_result["Bytes Received"],
                'Unanswered Questions (Baseline)': baseline_result["Unanswered Questions"],
                'Attachments in Sent Messages (Baseline)' : baseline_result["Attachments in Sent Messages"],

                'Sent Messages (Comparison)': comparison_result["Sent Messages"],
                'Received Messages (Comparison)': comparison_result["Received Messages"],
                'Recipients in Sent Messages (Comparison)': comparison_result["Recipients in Sent Messages"],
                'Bcc Recipients in Sent Messages (Comparison)': comparison_result["Bcc Recipients in Sent Messages"],
                'Cc Recipients in Sent Messages (Comparison)': comparison_result["Cc Recipients in Sent Messages"],
                'Replies to Messages (Comparison)': comparison_result["Replies to Messages"],
                'Characters in Outgoing Messages (Comparison)': comparison_result["Characters in Outgoing Messages"],
                'Messages Outside Working Hours (Comparison)': comparison_result["Messages Outside Working Hours"],
                "Bytes Sent (Comparison)": comparison_result["Bytes Sent"],
                "Bytes Received (Comparison)": comparison_result["Bytes Received"],
                'Unanswered Questions (Comparison)': comparison_result["Unanswered Questions"],
                'Attachments in Sent Messages (Comparison)' : comparison_result["Attachments in Sent Messages"]
                })], ignore_index=True)
        else:
            bad_emails.append(email_address)

    result_df.to_csv(path_to_save, index=False)
    return bad_emails