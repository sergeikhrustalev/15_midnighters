from datetime import datetime
import pytz
import requests


def load_page(page_number):

    api_url = 'https://devman.org/api/challenges/solution_attempts/'

    return requests.get(
        api_url,
        params={'page': page_number}
    ).json()


def get_attempts_record():

    first_page = load_page('1')

    yield from first_page['records']

    number_of_pages = first_page['number_of_pages']

    for page in range(2, number_of_pages+1):

        yield from load_page(str(page))['records']


def is_midnighter(attempts_record, start_hour=0, end_hour=4):

    server_timezone = pytz.timezone('Europe/Moscow')

    server_datetime = server_timezone.localize(
        datetime.fromtimestamp(attempts_record['timestamp'])
    )

    client_timezone = pytz.timezone(attempts_record['timezone'])

    client_datetime = server_datetime.astimezone(client_timezone)

    return client_datetime.hour >= start_hour \
        and client_datetime.hour <= end_hour


if __name__ == '__main__':

    print('Users who send their tasks for a verification after 24:00.')
    print('First column is sent datetime, second is username')

    for attempts_record in get_attempts_record():

        if is_midnighter(attempts_record):

            client_datetime = datetime.fromtimestamp(
                attempts_record['timestamp']
            ).strftime('%d.%m.%Y %H.%M.%S')

            print(client_datetime, '\t', attempts_record['username'])
