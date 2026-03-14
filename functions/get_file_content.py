import os

def get_file_content(working_directory, file_path):
    working_directory_path = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_directory_path, file_path))
    if os.path.commonpath([working_directory_path, target_file_path]) != working_directory_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: "{file_path}" is not a file'
    with open(target_file_path, "r") as f:
        content = f.read()
    return content