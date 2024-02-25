import pytest
import requests_mock
import time
import random

from main import app, fetch_weather, Users


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


import pytest


@pytest.fixture
def mocker():
    import requests_mock
    with requests_mock.Mocker() as m:
        yield m


def test_fetch_weather(mocker):
    city = "London"
    temperature = 20
    api_key = '6452fac8c7f98465f0f77d11ba388902'
    mocker.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric",
               json={'main': {'temp': temperature}})

    result = fetch_weather(city)
    assert result == temperature


def test_update_balance(client):
    user_id = 1
    city = "London"

    response = client.post(f'/update_balance?userId={user_id}&city={city}')
    assert response.status_code == 400  # Ожидаем статус 400, так как запрос с неправильными данными

    # Создаем пользователя с пустым именем и начальным балансом 0
    user = Users(user_id, username='', balance=0)
    balance = user.get_balance()
    assert balance >= 0


def test_system_load(client):
    start_time = time.time()
    end_time = start_time + 60  # 20 минут

    while time.time() < end_time:
        user_id = random.randint(1, 5)
        city = random.choice(["London", "Paris", "Berlin", "New York", "Tokyo"])
        response = client.post(f'/update_balance?userId={user_id}&city={city}')
        assert response.status_code == 400  # Ожидаем статус 400

    # Отправка 1000 запросов в секунду
    for _ in range(1000):
        user_id = random.randint(1, 5)
        city = random.choice(["London", "Paris", "Berlin", "New York", "Tokyo"])
        response = client.post(f'/update_balance?userId={user_id}&city={city}')
        assert response.status_code == 400  # Ожидаем статус 400

    elapsed_time = time.time() - start_time
    assert elapsed_time <= 60.1  # Проверка, что все запросы были обработаны за 20 минут
