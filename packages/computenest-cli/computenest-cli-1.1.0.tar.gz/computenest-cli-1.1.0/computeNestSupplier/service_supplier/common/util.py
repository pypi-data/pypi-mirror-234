import re
import time
import yaml
import base64
import datetime
import subprocess


class Util:
    def __init__(self):
        pass

    @staticmethod
    def regular_expression(data):
        match = re.match(r'\$\{([\w\.]+)\}', data)
        if match:
            parts = match.group(1).split('.')
            return parts
        else:
            print("Invalid variable format")

    @staticmethod
    def add_timestamp_to_version_name(data=''):
        current_time = datetime.datetime.now()
        time_str = current_time.strftime("%Y%m%d%H%M%S")
        if data:
            new_version_name = str(data) + "_" + time_str
        else:
            new_version_name = time_str
        return new_version_name

    @staticmethod
    def lowercase_first_letter(data):
        if isinstance(data, dict):
            return {k[0].lower() + k[1:]: v for k, v in data.items()}
        elif isinstance(data, str):
            return data[0].lower() + data[1:]
        else:
            return data

    @staticmethod
    def run_cli_command(command, cwd):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=cwd)
        output, error = process.communicate()
        return output, error

    @staticmethod
    def measure_time(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"\nExecution time: {int(execution_time)}s\n")
            return result

        return wrapper

    @staticmethod
    def get_current_time():
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return current_time

    @staticmethod
    def decode_base64(encoded_data):
        decoded_bytes = base64.b64decode(encoded_data)
        decoded_text = decoded_bytes.decode("utf-8")
        return decoded_text

    @staticmethod
    def write_yaml_to_file(data, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, allow_unicode=True)
