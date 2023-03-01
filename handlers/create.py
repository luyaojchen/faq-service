import uuid

from models.knowledgebase_model import Knowledgebase
from models.statics_model import ResponseStatics, g_index


def create_handler():
    # Create a unique ID for this creation request
    knowledgebase_id = str(uuid.uuid4())

    # Initialize the entry in g_index.
    g_index[knowledgebase_id] = Knowledgebase(knowledgebase_id)

    # Return the generated knowledgebase ID to the user
    return knowledgebase_id
