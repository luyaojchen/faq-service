import tempfile
from llama_index import SimpleDirectoryReader

from models.statics_model import ResponseStatics, g_index


def upload_handler(knowledgebase_id, file):

    if not knowledgebase_id:
        return False

    # Check if knowledgebase exists
    if knowledgebase_id not in g_index:
        return False

    with tempfile.NamedTemporaryFile(delete=False) as fp:
        file.save(fp)
        doc = SimpleDirectoryReader(input_files=[fp.name]).load_data()
        g_index[knowledgebase_id].add_documents(doc)

    return True
