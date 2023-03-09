import asyncio
from functools import partial

import flask
from llama_index.prompts.chat_prompts import CHAT_REFINE_PROMPT

from models.statics_model import g_index, ResponseStatics
from models.statics_model import llm_predictor
from models.statics_model import prompt_helper


async def query_handler(knowledgebase_id, query):

    # Validate the knowledgebase ID
    if not knowledgebase_id:
        return ResponseStatics.build_api_error("knowledgebase_id is required")

    # Check if knowledgebase exists
    if knowledgebase_id not in g_index:
        return ResponseStatics.build_api_error("knowledgebase_id does not exist")

    # Check if knowledgebase has a built index
    if not g_index[knowledgebase_id].index:
        return ResponseStatics.build_api_error("knowledgebase_id does not have an index, run compose first on this knowledgebase")

    # Validate the query
    if not query:
        return ResponseStatics.build_api_error("No query provided")

    # Query the index
    resp = await g_index[knowledgebase_id].index.aquery(query, llm_predictor=llm_predictor, refine_template=CHAT_REFINE_PROMPT, similarity_top_k=3, prompt_helper=prompt_helper)

    resp = flask.Response(resp.response, 200)

    return resp
