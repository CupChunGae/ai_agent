from functions.get_file_content import get_file_content
from config import reading_limit

return_value_lorem = get_file_content("calculator", "lorem.txt")
if len(return_value_lorem) > reading_limit and return_value_lorem.endswith(f'[...File "lorem.txt" truncated at {reading_limit} characters]'):
    print(len(return_value_lorem))
    print("File content read successfully.")
else:
    print(len(return_value_lorem))
    print("Failed to read file content.")

print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))