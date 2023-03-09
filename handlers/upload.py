import tempfile
from llama_index import SimpleDirectoryReader

from models.statics_model import ResponseStatics, g_index


def upload_handler(knowledgebase_id, file):

    if not knowledgebase_id:
        return False

    # Check if knowledgebase exists
    if knowledgebase_id not in g_index:
        return False

    # Get the content type of the file
    content_type = "" if not file.content_type else file.content_type
    suffix = ""

    if content_type == "application/pdf":
        suffix = ".pdf"
    elif content_type == "application/msword":
        suffix = ".docx"
    elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        suffix = ".docx"
    elif content_type == "application/vnd.oasis.opendocument.text":
        suffix = ".odt"
    elif content_type == "text/plain":
        suffix = ".txt"
    # csv check
    elif content_type == "text/csv":
        suffix = ".csv"
    # markdown check
    elif content_type == "text/markdown":
        suffix = ".md"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as fp:
        file.save(fp)
        doc = SimpleDirectoryReader(input_files=[fp.name]).load_data()
        g_index[knowledgebase_id].add_documents(doc)

    return True
