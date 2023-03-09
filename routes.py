import sys

import flask
from flask import Flask
import os
from dotenv import load_dotenv
from langchain import OpenAI

from handlers.compose import compose_handler
from handlers.create import create_handler
from handlers.query import query_handler
from handlers.upload import upload_handler
from models.statics_model import ResponseStatics, g_index

app = Flask(__name__)
load_dotenv()
OpenAI.openai_api_key = os.getenv('OPENAI_API_KEY')


@app.route('/create', methods=['GET'])
async def create():
    """Create a knowledgebase and return a knowlegebase ID"""
    # Create a unique ID for this creation request
    return ResponseStatics.build_creation_response(create_handler())


@app.route('/doc/add', methods=['POST'])
async def upload():
    # Extract the knowledgebase_id from the request
    knowledgebase_id = flask.request.form.get('knowledgebase_id')

    # Validate the knowledgebase ID
    if not upload_handler(knowledgebase_id, flask.request.files['file']):
        return ResponseStatics.build_api_error("Invalid knowledgebase ID or none provided")
    return ResponseStatics.build_upload_success_message()


@app.route('/compose', methods=['GET'])
async def compose():
    # Extract the knowledgebase_id from the request
    knowledgebase_id = flask.request.args.get('knowledgebase_id')

    # Validate the knowledgebase ID
    if not await compose_handler(knowledgebase_id):
        return ResponseStatics.build_api_error("Invalid knowledgebase ID or none provided")

    return ResponseStatics.build_compose_success_message()


@app.route('/query', methods=['GET'])
async def query():
    # Extract the query from the request (GET)
    query = flask.request.args.get('query')

    # Extract the knowledgebase_id from the request
    knowledgebase_id = flask.request.args.get('knowledgebase_id')

    return await query_handler(knowledgebase_id, query)


def init():
    app.run(host="0.0.0.0", port=8182, debug=True)


if __name__ == '__main__':
    sys.exit(init())
