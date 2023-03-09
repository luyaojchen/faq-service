import tempfile

import llama_index
from llama_index import SimpleDirectoryReader
import aiohttp
from llama_index.readers.web import DEFAULT_WEBSITE_EXTRACTOR

from models.statics_model import ResponseStatics, g_index


def upload_doc_handler(knowledgebase_id, file):

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


async def upload_link_handler(knowledgebase_id, url):

    if not knowledgebase_id:
        return False

    # Check if knowledgebase exists
    if knowledgebase_id not in g_index:
        return False

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return False

            if response.headers["Content-Type"] == "application/pdf":
                data = await response.read()
                f = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
                f.write(data)
                f.close()
                doc = SimpleDirectoryReader(input_files=[f.name]).load_data()
                g_index[knowledgebase_id].add_documents(doc)

            else:
                documents = llama_index.BeautifulSoupWebReader(website_extractor=DEFAULT_WEBSITE_EXTRACTOR).load_data(urls=[url])
                g_index[knowledgebase_id].add_documents(documents)

    return True
