import os
import glob
import json
from typing import Literal
import subprocess


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

    path_home_squad = "$HOME/data/squad/"
    path_file = f"{path_home_squad}{file_to_import}"
    print(eval(f"subprocess.getoutput('test -f {path_file}')"))

    exist_file = glob.glob(path_file)
    print(path_file)
    if not exist_file:
        print("file NOT")
    else:
        print("file EXIST")

        # $HOME/data/squad

    # folder_paths = "./noSubmit/RAG_data/"
    # if not os.path.exists(folder_paths):
    #     os.mkdir(folder_paths)
    #     if os.path.exists(folder_paths):
    #         print(f"path '{folder_paths}' created.")
    # else:
    #     print(f"path '{folder_paths}' already exists.")

    return output_dictionary


def main():
    import_data("dev")

    pass


if __name__ == "__main__":
    main()
