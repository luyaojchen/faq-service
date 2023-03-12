from pathlib import Path

from models.statics_model import ResponseStatics


# list all indexes from indexes directory with pathlib
async def list_handler():

    idx = []
    (Path.cwd() / 'indexes').exists()  # Make sure that the indexes folder exists first
    for index_file in Path("indexes").iterdir():
        # Define the path
        path = index_file.stem
        idx.append(path)
    return ResponseStatics.build_list_response(idx)

