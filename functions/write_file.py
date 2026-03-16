import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_directory_path = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_directory_path, file_path))
    if os.path.commonpath([working_directory_path, target_file_path]) != working_directory_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
    try:
        with open(target_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Failed to write to file "{file_path}": {e}'
    
schema_overwrite_file = types.FunctionDeclaration(
    name="write_file",
    description="Allows access to the specified file and overwrite the contents with the content argument in the function.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"]
    ),
)