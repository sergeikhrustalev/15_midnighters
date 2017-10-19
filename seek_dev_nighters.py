from datetime import datetime
import pytz
import requests


def load_attempts():

    api_url = 'https://devman.org/api/challenges/solution_attempts/'

    number_of_pages = requests.get(
        api_url,
        params={'page': '1'}
        ).json()['number_of_pages']

    for page in range(number_of_pages):

        current_page_records = requests.get(
                api_url,
                params={'page': str(page+1)}
            ).json()['records']

        for attempts_record in current_page_records:
            yield attempts_record


def get_midnighters():

    midnight_hour = 0
    server_timezone = pytz.timezone('Europe/Moscow')

    for attempts_record in load_attempts():

        server_datetime = server_timezone.localize(
            datetime.fromtimestamp(attempts_record['timestamp']))
        client_timezone = pytz.timezone(attempts_record['timezone'])
        client_datetime = server_datetime.astimezone(client_timezone)

        if client_datetime.hour == midnight_hour:
            yield attempts_record


if __name__ == '__main__':

    print('Users who send their tasks for a verification after 24:00.')
    print('First column is sent datetime, second is username')

    for attempts_records in get_midnighters():

        client_datetime = datetime.fromtimestamp(
            attempts_records['timestamp']).strftime('%d.%m.%Y %H.%M.%S')

        print(client_datetime, '\t', attempts_records['username'])
