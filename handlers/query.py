import flask

from models.statics_model import g_index, ResponseStatics


def query_handler(knowledgebase_id, query):

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
    resp = g_index[knowledgebase_id].index.query(query)

    resp = flask.Response(resp.response, 200)

    return resp
