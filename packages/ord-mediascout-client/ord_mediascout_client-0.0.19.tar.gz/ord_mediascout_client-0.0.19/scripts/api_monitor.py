from typing import List
import os
from dotenv import load_dotenv
import filecmp
import difflib
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


load_dotenv('.env')
data_dir = f'{os.getcwd()}/data/'


"""
При отправке почты через smtp.gmail.com, сначала необходимо разрешить доступ для ненадежных приложений к аккаунту, 
который будет использоваться для отправки почты на странице https://myaccount.google.com/lesssecureapps
"""
SMTP_SERVER=str(os.getenv('SMTP_SERVER'))
SMTP_PORT=int(os.getenv('SMTP_PORT'))
SMTP_USERNAME=str(os.getenv('SMTP_USERNAME'))
SMTP_PASSWORD=str(os.getenv('SMTP_PASSWORD'))

MAIL_TO = str(os.getenv('MAIL_TO'))
MAIL_FROM = str(os.getenv('MAIL_FROM'))
MAIL_SUBJECT = str(os.getenv('MAIL_SUBJECT'))

API_SWAGGER_JSON_URL=str(os.getenv('API_SWAGGER_JSON_URL'))

PREVIOUS_FILE = data_dir+str(os.getenv('PREVIOUS_FILENAME') or 'swagger.json')
CURRENT_FILE = data_dir+str(os.getenv('CURRENT_FILENAME') or 'new_swagger.json')
DIFF_ADDITIONAL_LINES = int(os.getenv('DIFF_ADDITIONAL_LINES') or 5)


def get_api_json() -> str:
    response = requests.get(API_SWAGGER_JSON_URL)
    if response.status_code == 200:
        return response.text


def generate_html_diff(prev_file_content: list, curr_file_content: list) -> str:
    return difflib.HtmlDiff().make_file(
        prev_file_content,
        curr_file_content,
        fromdesc='Текущий JSON',
        todesc='Новый JSON',
        context=True,
        numlines=DIFF_ADDITIONAL_LINES,
    )


def open_file(file: str) -> List:
    with open(file, 'r') as f:
        content = f.readlines()

    return content


def write_file(file: str, content: str) -> None:
    with open(file, 'w') as f:
        f.write(content)


def send_notification(html_notification: str) -> None:
    message = MIMEMultipart()
    message['From'] = MAIL_FROM
    message['To'] = MAIL_TO
    message['Subject'] = MAIL_SUBJECT
    message.attach(MIMEText(html_notification, 'html'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        if SMTP_SERVER == 'smtp.gmail.com':
            server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, MAIL_TO, message.as_string())


json_data = get_api_json()

if json_data is not None:
    # если это первый запуск и предыдущего файла нет, то создать его
    if not os.path.exists(PREVIOUS_FILE):
        write_file(PREVIOUS_FILE, json_data)
    else:
        write_file(CURRENT_FILE, json_data)
        result = filecmp.cmp(PREVIOUS_FILE, CURRENT_FILE)
        # проверить, отличаются ли файлы, если да, то получить diff и отправить его на почту
        if not result:
            prev_file_content = open_file(PREVIOUS_FILE)
            curr_file_content = open_file(CURRENT_FILE)
            # получить таблицу с различием файлов
            diff = generate_html_diff(prev_file_content, curr_file_content)
            # отправить уведомление с различиями
            send_notification(diff)
            # заменить предыдущую версию файла новой
            os.remove(PREVIOUS_FILE)
            os.rename(CURRENT_FILE, PREVIOUS_FILE)
