from pathlib import Path

import flask
import openai
from langchain.llms import OpenAIChat
from llama_index import LLMPredictor, GPTSimpleVectorIndex, SimpleDirectoryReader, PromptHelper, Document
from langchain import OpenAI

from services.environment_service import EnvService

openai.openai_api_key = EnvService.get_openai_api_key()

llm_predictor = LLMPredictor(llm=OpenAIChat(temperature=0, model_name="gpt-3.5-turbo"))
prompt_helper = PromptHelper(3900, 256, 20)
# for now keep in memory of all documents in list
g_index = {}


file_extensions_mappings = {
    "application/pdf": ".pdf",
    "application/msword": ".docx",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.oasis.opendocument.text": ".odt",
    "text/plain": ".txt",
    "text/csv": ".csv",
    "text/markdown": ".md",
    "text/html": ".html",
    # Epub
    "application/epub+zip": ".epub",
}

class Answer:
    def __init__(self, answer_id, answer_text):
        self.answer_id = answer_id
        self.answer_text = answer_text


class ResponseStatics:

    @staticmethod
    def build_api_error(error_message):
        return flask.jsonify({"error": error_message})

    @staticmethod
    def build_compose_success_message():
        return flask.jsonify({"message": "Successfully composed knowledgebase"})

    @staticmethod
    def build_upload_success_message():
        return flask.jsonify({"message": "Successfully uploaded document"})

    @staticmethod
    def build_answer_response(answer: Answer):
        return flask.jsonify({"answer_id": answer.answer_id, "answer_text": answer.answer_text})

    @staticmethod
    def build_creation_response(knowledgebase_id):
        return flask.jsonify({"knowledgebase_id": knowledgebase_id})

    @staticmethod
    def build_list_response(knowledgebase_ids):
        return flask.jsonify({"knowledgebase_ids": knowledgebase_ids})