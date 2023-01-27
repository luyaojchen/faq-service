import flask
from flask import Flask
import sys

app = Flask(__name__)

class Answer:
    def __init__(self, answer_id, answer_text):
        self.answer_id = answer_id
        self.answer_text = answer_text


def build_api_error(error_message):
    return flask.jsonify({"error": error_message})

def build_answer_response(answer: Answer):
    return flask.jsonify({"answer_id": answer.answer_id, "answer_text": answer.answer_text})

@app.route('/answer', methods=['GET'])
def ask():
    sample_ans = Answer('123', 'sample')
    return build_answer_response(sample_ans)

@app.route('/adjust', methods=['POST'])
def adjust():
    answer_id = flask.request.args.get('answer_id',None)
    answer_text = flask.request.args.get('answer_text',None)

    if not answer_id or not answer_text:
        return build_api_error("Missing answer_id or answer_text")

    resp = flask.Response('', 200)
    return resp

def init():
    app.run(host="0.0.0.0", port=8182)

if __name__ == '__main__':
    init()
