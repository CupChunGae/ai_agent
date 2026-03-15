import os
from google.genai import types

def get_files_info(working_directory, directory = "."):
    working_directory_path = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(working_directory_path, directory))
    if os.path.commonpath([working_directory_path, target_directory]) != working_directory_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'
    dir_list = []
    try:
        for item in os.listdir(target_directory):
            item_dir = os.path.join(target_directory,item)
            dir_list.append(f"- {item}: file_size={os.path.getsize(item_dir)} bytes, is_dir={os.path.isdir(item_dir)}")
            dir_string = "\n".join(dir_list)
        return dir_string
    except PermissionError:
        return f'Error: Permission denied to access "{directory}"'
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)