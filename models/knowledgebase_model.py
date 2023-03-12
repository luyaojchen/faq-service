import asyncio
from functools import partial
from pathlib import Path

from llama_index import GPTSimpleVectorIndex
from models.statics_model import llm_predictor, g_index
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

    async def build_index(self):
        #Go through the documents and flatten them
        flattened_documents = []
        for document in self.documents:
            if isinstance(document, list):
                # Flatten the list
                flattened_documents.extend(document)
            else:
                flattened_documents.append(document)

        index = await asyncio.get_event_loop().run_in_executor(None, partial(GPTSimpleVectorIndex, documents=flattened_documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper))

        self.index = index

        # Save the index to disk
        self.index.save_to_disk(f"indexes/{self.knowledgebase_id}.index")

        return self.index

    # String repr is just the id
    def __repr__(self):
        return self.knowledgebase_id

    # Equality is just the knowledgebase ID
    def __eq__(self, other):
        return self.knowledgebase_id == other.knowledgebase_id

# Using Pathlib open all the files under the "indexes" folder
Path("indexes").mkdir(parents=True, exist_ok=True) # Make sure that the indexes folder exists first
for index_file in Path("indexes").iterdir():
    # Load the index from disk
    # Define the path
    path = Path("indexes") / f"{index_file.stem}.index"
    index = GPTSimpleVectorIndex.load_from_disk(str(path))
    # Add the index to the global index
    g_index[index_file.stem] = Knowledgebase(index_file.stem)
    g_index[index_file.stem].index = index