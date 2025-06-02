import eventlet
eventlet.monkey_patch()

import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send

# Импортируем обработчики
from server.mode_1_1_handlers import setup_mode_1_1_routes
from server.mode_1_2_handlers import setup_mode_1_2_routes

app = Flask(__name__)
app.secret_key = 'some_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Настройка маршрутов
setup_mode_1_1_routes(app)
setup_mode_1_2_routes(app)

# Основные маршруты
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/room_setup')
def room_setup():
    return render_template('room_setup.html')

@app.route('/game/<mode>')
def game_mode(mode):
    if mode == '1.1':
        return render_template('game_mode_1_1.html')
    elif mode == '1.2':
        return render_template('game_mode_1_2.html')
    elif mode in ['2.1', '2.2']:
        return render_template('room_setup.html', mode=mode)
    else:
        return "Неизвестный режим", 404

@app.route('/select_range_1_2')
def select_range_1_2():
    return render_template('range_select_1_2.html')

@app.route('/game_mode_1_2')
def game_mode_1_2():
    range_param = request.args.get('range', '0_100')
    try:
        min_range, max_range = map(int, range_param.split('_'))
    except ValueError:
        min_range, max_range = 0, 100
    return render_template('game_mode_1_2.html', min_range=min_range, max_range=max_range)

# WebSocket обработчик
@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))