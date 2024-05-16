import os
import glob
import json
from typing import Literal


def import_data(dev_train: str = Literal["dev", "train"]) -> dict:
    output_dictionary = {}

    folder_paths = "./noSubmit/"
    if not os.path.exists(folder_paths):
        os.mkdir(folder_paths)
        if os.path.exists(folder_paths):
            print(f"path '{folder_paths}' created.")
    else:
        print(f"path '{folder_paths}' already exists.")

    folder_paths = "./noSubmit/RAG_data/"
    if not os.path.exists(folder_paths):
        os.mkdir(folder_paths)
        if os.path.exists(folder_paths):
            print(f"path '{folder_paths}' created.")
    else:
        print(f"path '{folder_paths}' already exists.")

    file_to_import = f"{dev_train}-v1.1.json"
    exist_file = glob.glob(folder_paths + file_to_import)
    if not exist_file:
        pass

        # $HOME/data/squad

    folder_paths = "./noSubmit/RAG_data/"
    if not os.path.exists(folder_paths):
        os.mkdir(folder_paths)
        if os.path.exists(folder_paths):
            print(f"path '{folder_paths}' created.")
    else:
        print(f"path '{folder_paths}' already exists.")

    return output_dictionary


def main():
    import_data("dev")

    pass


if __name__ == "__main__":
    main()
