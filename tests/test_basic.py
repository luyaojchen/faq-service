import io
import json
import os
from pathlib import Path
from pprint import pprint

from flask import jsonify
import pytest
from flask.testing import FlaskClient
from routes import app
from werkzeug.datastructures import FileStorage


'''
testflow

- create knowledge base
- upload
- compose
- ask
'''


@pytest.fixture
def client():
    return app.test_client()


def test_flow(client: FlaskClient):
    resp = client.get('/create')
    data = json.loads(resp.data.decode('utf-8'))
    knowledgebase_id = data['knowledgebase_id']

    file_name = '../testing.txt'
    file_path = os.path.join(Path(os.path.dirname(__file__)), file_name)
    with open(file_path, 'rb') as input_file:
        input_file_stream = io.BytesIO(input_file.read())
    data = {
        'knowledgebase_id': knowledgebase_id,
        'file': (input_file_stream, file_name),
    }

    resp = client.post('/index/doc/add', content_type='multipart/form-data', data=data)
    assert resp.status_code == 200

    data = {
        'knowledgebase_id': knowledgebase_id
    }

    resp = client.get('/compose', query_string=data)

    assert resp.status_code == 200

    test_payload = {
        'knowledgebase_id': knowledgebase_id,
        'query': 'The code word for this is:'
    }
    resp = client.get('/query', query_string=test_payload)
    data = resp.data.decode('utf-8')
    assert "test" in data
