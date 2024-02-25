import sqlite3
import random
import requests
from flask import Flask, request, g
from user import Users

app = Flask(__name__)
api_key = '6452fac8c7f98465f0f77d11ba388902'


def add_random_users(cursor):
    for i in range(1, 6):
        username = f'user{i}'
        balance = random.randint(5000, 15000)
        cursor.execute("INSERT INTO users (username, balance) VALUES (?, ?)", (username, balance))


def setup():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            balance INTEGER
        )
    ''')
    add_random_users(cursor)
    conn.commit()
    conn.close()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('users.db')
    return db


def fetch_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        temperature = data['main']['temp']
        return temperature
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


@app.route('/update_balance', methods=['POST'])
def update_balance():
    user_id = request.form.get('userId')
    city = request.form.get('city')

    if not user_id or not city:
        return 'Missing userId or city in request', 400

    temperature = fetch_weather(city)
    if temperature is None:
        return 'Failed to fetch temperature data for the city', 500

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        user = Users(user_data[0], user_data[1], user_data[2])
        user.update_balance(temperature)

        cursor.execute('UPDATE users SET balance=? WHERE id=?', (user.balance, user.id))
        conn.commit()

        return 'Balance updated successfully'
    else:
        return 'User not found', 404


if __name__ == '__main__':
    app.run(debug=False)
