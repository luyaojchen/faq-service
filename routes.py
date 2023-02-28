import uuid

import flask
from flask import Flask
from gpt_index import LLMPredictor, GPTSimpleVectorIndex, SimpleDirectoryReader, PromptHelper, Document
import os
from dotenv import load_dotenv
from langchain import OpenAI
import tempfile
from collections import defaultdict
import shutil

app = Flask(__name__)
load_dotenv()
OpenAI.openai_api_key = os.getenv('OPENAI_API_KEY')

# for now keep in memory of all documents in list
g_index = {}
# helpers for llm
llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))
prompt_helper = PromptHelper(4096, 256, 20)


class Knowledgebase:

    def __init__(self, id):
        self.knowledgebase_id = id
        self.documents = []
        self.index = None

    def add_documents(self, *documents):
        for document in documents:
            self.documents.append(document)
    def build_index(self):
        #Go through the documents and flatten them
        flattened_documents = []
        for document in self.documents:
            if (isinstance(document, list)):
                # Flatten the list
                flattened_documents.extend(document)
            else:
                flattened_documents.append(document)

        index = GPTSimpleVectorIndex(
            documents=flattened_documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper
        )
        self.index = index

        return self.index

    # String repr is just the id
    def __repr__(self):
        return self.knowledgebase_id

    # Equality is just the knowledgebase ID
    def __eq__(self, other):
        return self.knowledgebase_id == other.knowledgebase_id

class Answer:
    def __init__(self, answer_id, answer_text):
        self.answer_id = answer_id
        self.answer_text = answer_text

def build_api_error(error_message):
    return flask.jsonify({"error": error_message})

def build_compose_success_message():
    return flask.jsonify({"message": "Successfully composed knowledgebase"})

def build_answer_response(answer: Answer):
    return flask.jsonify({"answer_id": answer.answer_id, "answer_text": answer.answer_text})

def build_creation_response(knowledgebase_id):
    return flask.jsonify({"knowledgebase_id": knowledgebase_id})


@app.route('/create', methods=['GET'])
def create():
    """Create a knowledgebase and return a knowlegebase ID"""
    # Create a unique ID for this creation request
    knowledgebase_id = str(uuid.uuid4())

    # Initialize the entry in g_index.
    g_index[knowledgebase_id] = Knowledgebase(knowledgebase_id)

    # Return the generated knowledgebase ID to the user
    return build_creation_response(knowledgebase_id)

@app.route('/doc/add', methods=['POST'])
def upload():
    # Extract the knowledgebase_id from the request
    knowledgebase_id = flask.request.form.get('knowledgebase_id')

    # Validate the knowledgebase ID
    if not knowledgebase_id:
        return build_api_error("knowledgebase_id is required")

    # Check if knowledgebase exists
    if knowledgebase_id not in g_index:
        return build_api_error("knowledgebase_id does not exist")

    data = flask.request.files['files']
    with tempfile.NamedTemporaryFile(delete=False) as fp:
        data.save(fp)
        doc = SimpleDirectoryReader(input_files=[fp.name]).load_data()
        g_index[knowledgebase_id].add_documents(doc)

    resp = flask.Response('Documents Added', 200)
    return resp


@app.route('/compose', methods=['GET'])
def compose():
    # Extract the knowledgebase_id from the request
    knowledgebase_id = flask.request.args.get('knowledgebase_id')
    print("1")

    # Validate the knowledgebase ID
    if not knowledgebase_id:
        return build_api_error("knowledgebase_id is required")

    print("2")

    # Check if knowledgebase exists
    if knowledgebase_id not in g_index:
        return build_api_error("knowledgebase_id does not exist")

    print('3')

    g_index[knowledgebase_id].build_index()
    print("4")
    return build_compose_success_message()


@app.route('/query', methods=['GET'])
def query():
    # Extract the query from the request (GET)
    query = flask.request.args.get('query')

    # Extract the knowledgebase_id from the request
    knowledgebase_id = flask.request.args.get('knowledgebase_id')

    # Validate the knowledgebase ID
    if not knowledgebase_id:
        return build_api_error("knowledgebase_id is required")

    # Check if knowledgebase exists
    if knowledgebase_id not in g_index:
        return build_api_error("knowledgebase_id does not exist")

    # Check if knowledgebase has a built index
    if not g_index[knowledgebase_id].index:
        return build_api_error("knowledgebase_id does not have an index, run compose first on this knowledgebase")

    # Validate the query
    if not query:
        return build_api_error("No query provided")

    # Query the index
    resp = g_index[knowledgebase_id].index.query(query)

    resp = flask.Response(resp.response, 200)
    print(resp.response)
    return resp


def init():
    app.run(host="0.0.0.0", port=8182, debug=True)


if __name__ == '__main__':
    init()
