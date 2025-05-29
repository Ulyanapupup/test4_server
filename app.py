import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send
from game_logic import mode_1_1
from game_logic import mode_1_2

import os

# Импортируем логику
from game_logic import mode_1_1, mode_1_2

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


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
        
@app.route('/range_select_1_2')
def range_select_1_2():
    return render_template('range_select_1_2.html')

@app.route('/game_mode_1_2.html')
def game_mode_1_2():
    return render_template('game_mode_1_2.html')

@app.route('/game')
def game():
    room_code = request.args.get('room')
    if not room_code:
        return "Ошибка: не указан код комнаты", 400
    return render_template('game.html', room_code=room_code)

@app.route('/start_1_2', methods=['POST'])
def start_1_2():
    mode_1_2.reset()
    q = mode_1_2.next_question()
    return jsonify({"question": q})

@app.route('/answer_1_2', methods=['POST'])
def answer_1_2():
    answer = request.json.get("answer", "")
    response, done = mode_1_2.process_answer(answer)
    return jsonify({"response": response, "done": done})

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get("question", "")
    mode = request.json.get("mode", "1.1")

    if mode == "1.1":
        answer = mode_1_1.process_question(question)
    elif mode == "1.2":
        # в этом режиме вопрос — это ключ (например, "число чётное")
        # и дополнительно приходит ответ игрока ("да" или "нет")
        answer_yes = request.json.get("answer") == "да"
        mode_1_2.filter_numbers(question, answer_yes)
        answer = ", ".join(map(str, mode_1_2.get_possible_numbers()))
    else:
        answer = "Неподдерживаемый режим"

    return jsonify({"answer": answer})


@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
