from flask import jsonify
from game_logic.mode_1_1 import process_question

def setup_mode_1_1_routes(app):
    @app.route('/ask_1_1', methods=['POST'])
    def ask_1_1():
        question = request.json.get("question", "")
        answer = process_question(question)
        return jsonify({"answer": answer})