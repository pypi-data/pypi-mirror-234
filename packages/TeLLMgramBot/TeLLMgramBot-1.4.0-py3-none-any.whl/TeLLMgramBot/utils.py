# Utility Functions
import re, yaml
from datetime import datetime

# File Name Friendly Timestamp
def get_timestamp() -> str:
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    return timestamp

# File Name Friendly UserName
def get_safe_username(name: str) -> str:
    # Remove leading '@' and any other special characters to exclude
    return re.sub(r'[^\w\s]', '', name.lstrip('@'))

# Basic open text file function
def open_file(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Reads the file per line in reverse order
# Source: https://thispointer.com/python-read-a-file-in-reverse-order-line-by-line/
def read_reverse_order(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        # Get all lines in a file as list to reverse order
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        lines = reversed(lines)
        return lines

# Read a YAML-formatted file, useful for configurations
def read_yaml(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data

# Read a plain text file, useful for system prompts
def read_text(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Generate a Chat Session Log filename
def generate_filename(bot_name: str, user_name: str) -> str:
    timestamp = get_timestamp()
    return f'{bot_name}-{user_name}-{timestamp}.log'

# Log error messages to a file including an error type and timestamp
def log_error(error: Exception or str, error_type: str, error_filename: str):
    timestamp = get_timestamp()
    with open(error_filename, 'a') as error_file:
        error_file.write(f'{timestamp} {error_type}: {error}\n')
        # Also print the error to the console
        print(f'{timestamp} {error_type}: {error}')
