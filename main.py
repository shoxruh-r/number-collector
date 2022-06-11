from time import sleep
from requests import get
from bs4 import BeautifulSoup
from os import rename, system, uname
from datetime import datetime
from sys import stdout
from config import TOKEN


LIMIT = 25
CATEGORIES = (
    'https://www.olx.uz/oz/detskiy-mir/',
    'https://www.olx.uz/oz/nedvizhimost/',
    'https://www.olx.uz/oz/transport/',
    'https://www.olx.uz/oz/rabota/',
    'https://www.olx.uz/oz/zhivotnye/',
    'https://www.olx.uz/oz/dom-i-sad/',
    'https://www.olx.uz/oz/elektronika/',
    'https://www.olx.uz/oz/uslugi/',
    'https://www.olx.uz/oz/moda-i-stil/',
    'https://www.olx.uz/oz/hobbi-otdyh-i-sport/',
    'https://www.olx.uz/oz/otdam-darom/',
    'https://www.olx.uz/oz/obmen-barter/'
)
NUMBER_OF_CATEGORIES = len(CATEGORIES)


def main():
    with open('databases/phones.txt', 'w') as file:
        print("Parsing Started!")
        page_number = 1
        index = 0
        parsed = 0

        while (True):
            response = get(f'{CATEGORIES[index]}?page={page_number}')

            if (page_number <= LIMIT):
                page_number += 1
            elif (page_number == 25 and index < NUMBER_OF_CATEGORIES - 1):
                page_number = 1
                index += 1
            else:
                break

            if (response.status_code != 200):
                continue

            soup = BeautifulSoup(response.content, 'html.parser')

            links = map(
                (lambda anchor: anchor.attrs['href'].split('#')[0]),
                soup.select('.detailsLink:not(.rel, .promoted-list *)')
            )

            for link in links:
                response = get(link)

                if (response.status_code != 200):
                    continue

                soup = BeautifulSoup(response.content, 'html.parser')

                id = soup.select_one('span.css-9xy3gn-Text')

                if (id):
                    id = id.text.replace('ID: ', '')

                response = get(
                    f'https://www.olx.uz/api/v1/offers/{id}/limited-phones/',
                    headers={'Authorization': f'Bearer {TOKEN}'}
                )

                if (response.status_code != 200):
                    if (response.status_code == 401):
                        print("Please, update token!")
                        return
                    elif (response.status_code == 403):
                        sleep(10)
                        continue
                    elif (response.status_code == 429):
                        sleep(30)
                        continue

                    print("Error: " + response.status_code)
                    continue

                phones = response.json()['data']['phones']

                if (len(phones) > 0):
                    file.write(phones[0] + '\n')
                    parsed += 1
                    stdout.write('\r')
                    stdout.write(f"Parsed: {parsed}")
                    stdout.flush()
                sleep(5)

    print("Parsing Completed!")


if __name__ == '__main__':
    try:
        main()

        if (uname().sysname == "Linux"):
            system("shutdown now")
        else:
            system("shutdown /s /t 1")
    except KeyboardInterrupt:
        print("\nYou stopped the parser!")
    finally:
        rename(
            'databases/phones.txt',
            f"databases/{str(datetime.today()).split('.')[0]}.txt"
        )
