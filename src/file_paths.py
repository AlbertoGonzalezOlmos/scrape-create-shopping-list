import os
import glob


def _format_path(
    path: str,
) -> str:
    root_path = "./noSubmit"

    if path.find(".txt") > 0:
        path = path[:-4]

    if not (path.startswith("/") or path.startswith(".")):
        path = f"/{path}"

    if path.find(root_path) < 0:
        path = f"{root_path}{path}"

    if not path.endswith("/"):
        path = f"{path}/"

    return path


def create_output_path(path: str) -> str:

    path = _format_path(path)

    print(f"checking path -> {path}")
    if not os.path.exists(path):
        print(f"it doesn't exist, creating it...")
        os.makedirs(path)
        if not os.path.exists(path):
            print(f"it couldn't create path in -> {path}, exiting...")
            return
        print(f"path created!")
    return path


def get_latest_file(
    path: str = "input_Ingredients/", extension: str = ".txt"
) -> tuple[str, str]:

    path = _format_path(path)

    if not extension.startswith("."):
        extension = f".{extension}"

    list_of_files = glob.glob(os.path.join(path, f"*{extension}"))

    if len(list_of_files) < 1:
        print(f"no files found in '{path}' with extension '{extension}'")
        return

    # get latest file added to the folder by date.

    latest_file = max(list_of_files, key=os.path.getctime)
    file_path = os.path.dirname(latest_file)
    file_path = _format_path(file_path)
    file_name = latest_file[len(file_path) :]
    print(f"latest file: {latest_file}")

    # print(f"the latest file is: {file_path+file_name}")
    return file_path, file_name


def main():

    path, name = get_latest_file()
    print(path)
    print(name)
    pass


if __name__ == "__main__":
    main()
