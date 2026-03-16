import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args = None):
    try:
        working_directory_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_path, file_path))
        if os.path.commonpath([working_directory_path, target_file_path]) != working_directory_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        abs_file_path = os.path.abspath(target_file_path)
        command = ["python", abs_file_path]
        if args != None:
            command.extend(args)
                
        process_object = subprocess.run(command, cwd = working_directory_path, capture_output = True, text = True, timeout = 30)
        output_str = ""
        if process_object.returncode != 0:
            output_str += f"Process exited with code {process_object.returncode}"
        if process_object.stdout == "" and process_object.stderr == "":
            output_str += "No output produced"
        else:
            if process_object.stdout:
                output_str += f"STDOUT: {process_object.stdout}"
            if process_object.stderr:
                output_str += f"STDERR: {process_object.stderr}"
        return output_str
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file from the specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)