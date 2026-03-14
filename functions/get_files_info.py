import os

def get_files_info(working_directory, directory = "."):
    if os.path.abspath() not in working_directory: #fix this if condition
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(directory) == False:
        return f'Error: "{directory}" is not a directory'
    pass