import os
import re
import csv
from . import gonogo

# Компилируем регулярные выражения для черного и белого списков
blacklist_regex = re.compile(r"pattern_to_exclude")
whitelist_regex = re.compile(r'^[^\\/:*?"<>|\r\n]+\.pdf$')

# Функции-обработчики
def handle_eeg(file_path):
    print(f"Обработка EEG файла: {file_path}")

def handle_gonogo(file_path):
  extracted_info = gonogo.processing.extract_info_from_gonogo_filename(os.path.basename(file_path))
  file_info = gonogo.processing.extract_info_from_gonogo_file(file_path)
  gonogo_result = gonogo.processing.extract_and_validate_numbers(file_info)
  combined_dict = {**extracted_info, **gonogo_result}
  print(combined_dict)
  return combined_dict

def handle_video(file_path):
    print(f"Обработка видео файла: {file_path}")

# Словарь сопоставления типов контента и хэндлеров
content_handlers = {
    'eeg': handle_eeg,
    'gonogo': handle_gonogo,
    'video': handle_video,
}

def process_files_in_directory(directory, handler):
    """Обработка файлов в директории с использованием заданного обработчика."""
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path) and whitelist_regex.search(file):
            handler(file_path)

def process_directory(root_directory, output_csv_path):
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=['respondentID', 'day', 'times', 'response_time', 'accuracy', 'overall_score', 'attempt_num', 'score'])
        csv_writer.writeheader()  # Запись заголовка
        for respondent_id in os.listdir(root_directory):
            respondent_path = os.path.join(root_directory, respondent_id)
            if not os.path.isdir(respondent_path):
                continue  # Пропускаем файлы на уровне root_directory
            for day in ['1day', '2day', 'day1', 'day2']:
                day_path = os.path.join(respondent_path, day)
                if not os.path.isdir(day_path):
                    continue  # Пропускаем, если директория дня отсутствует
                for content_type in content_handlers.keys():
                    content_path = os.path.join(day_path, content_type)
                    if os.path.isdir(content_path):
                        # Здесь можно добавить многопоточность или асинхронную обработку
                        data = process_files_in_directory(content_path, content_handlers[content_type])
                        csv_writer.writerow(data)
