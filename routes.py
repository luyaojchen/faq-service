import flask
from flask import Flask
import sys

app = Flask(name)


# make types file later
class Answer:
    def int(self, answer_id, answer_text):
        self.answer_id = answer_id
        self.answer_text = answer_text


@app.route('/answer', methods=['GET'])
def ask(query):
    # FAQ service -> get answer
    print(query)
    sample_ans = Answer('123', 'sample')
    return sample_ans


@app.route('/adjust', methods=['POST'])
def adjust(answer_id, adjustment):
    print(adjustment)
    print(answer_id, file=sys.stderr)
    resp = flask.Response('', 200)
    return resp
