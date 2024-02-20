import os
import re
import csv
import json
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

def process_with_all_files_report(root_directory, all_files_report, output_csv_path):
    content_handlers['gonogo'] = GoNoGoReportHandler(output_csv_path)
    data = {}
    try:
        if os.path.isfile(all_files_report):
            with open(all_files_report, mode='r', newline='', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    data[row['respondent_id']] = row
                    try:
                        day1_eeg = json.loads(row['day_1/gonogo']);
                        day2_eeg = json.loads(row['day_2/gonogo']);
                        if not day1_eeg:
                            day1_eeg = []
                        if not day2_eeg:
                            day2_eeg = []
                        for item in day1_eeg:
                            content_handlers['gonogo'].process(os.path.join(root_directory, item), 1, row['respondent_id'])
                        for item in day2_eeg:
                            content_handlers['gonogo'].process(os.path.join(root_directory, item), 2, row['respondent_id'])
                    except json.JSONDecodeError:
                        print("Ошибка при разборе JSON")    
    finally:
        content_handlers['gonogo'].close()            