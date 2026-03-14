import os

def overwrite_file(working_directory, file_path, content):
    working_directory_path = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_directory_path, file_path))
    if os.path.commonpath([working_directory_path, target_file_path]) != working_directory_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    try:
        with open(target_file_path, "w") as f:
            f.write(content)
        return f'Successfully overwrote file "{file_path}"'
    except Exception as e:
        return f'Error: Failed to write to file "{file_path}": {e}'