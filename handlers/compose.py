from models.statics_model import g_index


def compose_handler(knowledgebase_id):

    if not knowledgebase_id:
        return False

    # Check if knowledgebase exists
    if knowledgebase_id not in g_index:
        return False

    g_index[knowledgebase_id].build_index()
    return True
