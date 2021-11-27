import os
import argparse

import requests
from dotenv import load_dotenv


URL = "https://api-ssl.bitly.com/v4/bitlinks"


def shorten_link(token, url, headers, payload):
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    answer = response.json()
    link = answer["link"]
    return link


def count_clicks(token, url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    answer = response.json()
    total_clicks = answer["total_clicks"]
    return total_clicks


if __name__ == "__main__":
    load_dotenv()
    billy_token = os.getenv("BITLY_TOKEN")
    parser = argparse.ArgumentParser(description="""1. Сокращает ссылки.
        2. Выводит кол - во кликов по короткой - ссылке.""")
    parser.add_argument("link", help="Ссылка на сайт")
    args = parser.parse_args()
    link = args.link
    url_count = "{}/{}/clicks/summary".format(URL, link[8:])
    headers = {"Authorization": "Bearer {}".format(billy_token)}
    params = {"unit": "day", "units": "-1"}
    payload = {"long_url": link}

    if link.startswith("bit.ly", 8):
        try:
            clicks_count = count_clicks(billy_token, url_count, headers,
                                        params)
        except requests.exceptions.HTTPError as error:
            print("Неправильная ссылка.")
            print("Ответ: {content}".format(content=error.response.content))
        else:
            print("По вашей ссылке прошли {} раз(а).".format(clicks_count))
    else:
        try:
            bit_link = shorten_link(billy_token, URL, headers, payload)
        except requests.exceptions.RequestException as error:
            print("Неправильная ссылка.")
            print("Ответ: {content}".format(content=error.response.content))
        else:
            print("Короткая ссылка: {}".format(bit_link))
