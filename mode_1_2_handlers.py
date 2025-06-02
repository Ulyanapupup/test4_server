from flask import jsonify, request
import uuid
from game_logic.mode_1_2 import Game

games = {}  # хранилище активных игр для режима 1.2

def setup_mode_1_2_routes(app):
    @app.route('/start_game_1_2', methods=['POST'])
    def start_game_1_2():
        data = request.json
        secret = int(data.get('secret'))
        min_range = int(data.get('min_range'))
        max_range = int(data.get('max_range'))

        game_id = str(uuid.uuid4())
        games[game_id] = Game(secret, min_range, max_range)
        first_question = games[game_id].next_question()
        return jsonify({'game_id': game_id, 'question': first_question})

    @app.route('/answer_1_2', methods=['POST'])
    def answer_1_2():
        data = request.json
        game_id = data.get('game_id')
        answer = data.get('answer')

        game = games.get(game_id)
        if not game:
            return jsonify({'error': 'Игра не найдена'}), 404

        response = game.process_answer(answer)
        done = getattr(game, 'finished', False)

        return jsonify({'response': response, 'done': done})