import os
from config import reading_limit
from google.genai import types

def get_file_content(working_directory, file_path):
    working_directory_path = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_directory_path, file_path))
    if os.path.commonpath([working_directory_path, target_file_path]) != working_directory_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        print(f"reading_limit = {reading_limit}")
        with open(target_file_path, "r") as f:
            content = f.read(reading_limit)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {reading_limit} characters]'
            return content
    except Exception as e:
        return f'Error: Failed to read file "{file_path}": {e}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Accesses a specified file from a directory relative to the working directory, providing the file contents as a string.",
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