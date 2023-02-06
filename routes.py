import flask
from flask import Flask
from gpt_index import LLMPredictor, GPTSimpleVectorIndex, SimpleDirectoryReader, PromptHelper, Document
import os
from dotenv import load_dotenv
from langchain import OpenAI
import tempfile
import shutil

app = Flask(__name__)
load_dotenv()
OpenAI.openai_api_key = os.getenv('OPENAI_API_KEY')

# for now keep in memory of all documents in list
g_index = list()
# helpers for llm
llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))
prompt_helper = PromptHelper(4096, 256, 20)

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


@app.route('/doc/add', methods=['POST'])
def upload():
    data = flask.request.files['files']
    with tempfile.NamedTemporaryFile(delete=False) as fp:
        data.save(fp)
        doc = SimpleDirectoryReader(input_files=[fp.name]).load_data()
        [g_index.append(_doc) for _doc in doc]
    resp = flask.Response('', 200)
    return resp



@app.route('/compose', methods=['GET'])
def compose():
    print(g_index)
    index = GPTSimpleVectorIndex(
        documents=g_index, llm_predictor=llm_predictor, prompt_helper=prompt_helper
    )
    resp = index.query('what is this document about?')
    print(resp)
    resp = flask.Response('', 200)
    return resp

@app.route('/index', methods=['POST'])
def index():
    # file = flask.request.file['file']
    documents = SimpleDirectoryReader('./test').load_data()
    index = GPTSimpleVectorIndex(
        documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper
    )

    resp = index.query('what is this document about?')
    print(resp)
    resp = flask.Response('', 200)
    return resp


@app.route('/adjust', methods=['POST'])
def adjust():
    answer_id = flask.request.args.get('answer_id', None)
    answer_text = flask.request.args.get('answer_text', None)

    if not answer_id or not answer_text:
        return build_api_error("Missing answer_id or answer_text")

    resp = flask.Response('', 200)
    return resp


def init():
    app.run(host="0.0.0.0", port=8182)


if __name__ == '__main__':
    init()
