import os
import re
import csv
from .file_handler import GoNoGoReportHandler

blacklist_regex = re.compile(r"pattern_to_exclude")
whitelist_regex = re.compile(r'^[^\\/:*?"<>|\r\n]+\.pdf$')

content_handlers = {
    'gonogo': None
}

def process_files_in_directory(directory, handler):
    """Обработка файлов в директории с использованием заданного обработчика."""
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path) and whitelist_regex.search(file):
            handler.process(file_path)

def process_directory(root_directory, output_csv_path):
    content_handlers['gonogo'] = GoNoGoReportHandler(output_csv_path)
    try:
        for respondent_id in os.listdir(root_directory):
            respondent_path = os.path.join(root_directory, respondent_id)
            if not os.path.isdir(respondent_path):
                continue  
            for day in ['1day', '2day']:
                day_path = os.path.join(respondent_path, day)
                if not os.path.isdir(day_path):
                    continue  
                for content_type in content_handlers.keys():
                    content_path = os.path.join(day_path, content_type)
                    if os.path.isdir(content_path):
                        process_files_in_directory(content_path, content_handlers[content_type])
    finally:
        content_handlers['gonogo'].close()
