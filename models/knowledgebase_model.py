from llama_index import GPTSimpleVectorIndex
from models.statics_model import llm_predictor
from models.statics_model import prompt_helper
class Knowledgebase:

    def __init__(self, id, name=None):
        self.knowledgebase_id = id
        self.documents = []
        self.index = None
        self.name = name

    def add_documents(self, *documents):
        for document in documents:
            self.documents.append(document)

    def build_index(self):
        #Go through the documents and flatten them
        flattened_documents = []
        for document in self.documents:
            if isinstance(document, list):
                # Flatten the list
                flattened_documents.extend(document)
            else:
                flattened_documents.append(document)

        index = GPTSimpleVectorIndex(
            documents=flattened_documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper
        )
        self.index = index

        return self.index

    # String repr is just the id
    def __repr__(self):
        return self.knowledgebase_id

    # Equality is just the knowledgebase ID
    def __eq__(self, other):
        return self.knowledgebase_id == other.knowledgebase_id
