"""Консольный скрипт для замера скорости скачивания.

Делает 10 последовательных GET-запросов к указанному URL,
дожидается полного ответа на каждый, считает среднее время
запроса и скорость скачивания.

Использование:
    python speedtest.py <url>

Пример:
    python speedtest.py "https://speed.cloudflare.com/__down?bytes=25000000"
"""
import sys
import time

import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}
TIMEOUT = 30          # секунд ожидания одного запроса
REQUESTS_COUNT = 10   # сколько раз скачиваем файл


def main():
    if len(sys.argv) < 2:
        print("Ошибка: не указан URL.")
        print(f"Использование: python {sys.argv[0]} <url>")
        sys.exit(1)

    url = sys.argv[1]
    times = []
    total_bytes = 0

    for i in range(1, REQUESTS_COUNT + 1):
        print(f"Запрос {i}/{REQUESTS_COUNT}...", end=" ", flush=True)

        start = time.perf_counter()
        try:
            response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            size_bytes = len(response.content)
        except requests.exceptions.RequestException as e:
            print(f"ОШИБКА: {e}")
            continue
        elapsed = time.perf_counter() - start

        times.append(elapsed)
        total_bytes += size_bytes
        print(f"{elapsed:.2f} с, {size_bytes / (1024 * 1024):.2f} МБ")

    if not times:
        print("\nВсе запросы завершились ошибкой, статистика недоступна.")
        sys.exit(1)

    avg_time = sum(times) / len(times)
    total_time = sum(times)
    avg_speed = total_bytes / total_time / (1024 * 1024)

    print()
    print(f"Успешных запросов:     {len(times)}/{REQUESTS_COUNT}")
    print(f"Среднее время запроса: {avg_time:.2f} с")
    print(f"Всего скачано:         {total_bytes / (1024 * 1024):.2f} МБ")
    print(f"Скорость скачивания:   {avg_speed:.2f} МБ/с")


main()
