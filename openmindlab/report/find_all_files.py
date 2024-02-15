import os
import re
import csv
import json

"""
    Отчет для поиска всех файлов. Можно запускать несколько раз, файл-отчет правится.
    Главная функция для запуска логики "process(...)"
"""

headers = ['respondent_id', 'day_1', 'day_2', 'day_1/eeg', 'day_1/gonogo', 'day_1/video', 'day_2/eeg', 'day_2/gonogo', 'day_2/video']


def read_csv_data(csv_file_path):
    data = {}
    if os.path.isfile(csv_file_path):
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data[row['respondent_id']] = row
    return data

def write_to_csv(csv_file_path, all_data):
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for data in all_data.values():
            writer.writerow(data)

def update_data(respondent_id, category, value, existing_data):
    if respondent_id in existing_data:
        if existing_data[respondent_id][category] == '0':  # Если файл не был найден, можно перезаписать
            existing_data[respondent_id][category] = value
        elif existing_data[respondent_id][category] != value:  # Если информация отличается, вывести ошибку
            raise ValueError(f"Ошибка: Данные для respondent_id {respondent_id} в категории {category} уже существуют и отличаются.")
    else:
        existing_data[respondent_id] = {category: value}
    
def process_respondent_folders(root_path, existing_data):
    for respondent_id in os.listdir(root_path):
        respondent_path = os.path.join(root_path, respondent_id)
        if not os.path.isdir(respondent_path):
            continue
        else:
            data = {header: '0' for header in headers} 
            data['respondent_id'] = respondent_id
            existing_data[respondent_id] = data

        for day_num in [1,2]:
            day_folder_found = False
            for day_folder in [f'day{day_num}', f'{day_num}day']:
                day_path = os.path.join(respondent_path, day_folder)
                if os.path.exists(day_path):
                    day_folder_found = True
                    update_data(respondent_id, f'day_{day_num}', os.path.relpath(day_path, root_path), existing_data)
                    eeg_res = get_eeg_files(day_path, root_path)
                    if eeg_res:
                        update_data(respondent_id, f'day_{day_num}/eeg', eeg_res , existing_data)
                    else:
                        update_data(respondent_id, f'day_{day_num}/eeg', 0 , existing_data)

                    gonogo_res = get_gonogo_files(day_path, root_path)
                    if gonogo_res:
                        update_data(respondent_id, f'day_{day_num}/gonogo', gonogo_res , existing_data)
                    else:
                        update_data(respondent_id, f'day_{day_num}/gonogo', 0 , existing_data)
                    
                    video_res = get_video_files(day_path, root_path)
                    if video_res:
                        update_data(respondent_id, f'day_{day_num}/video', video_res , existing_data)
                    else:
                        update_data(respondent_id, f'day_{day_num}/video', 0 , existing_data)

                    break
        
            if not day_folder_found:
                update_data(respondent_id, f'day_{day_num}', 0, existing_data)            

def get_eeg_files(day_path, root_path):
    eeg_folder_path = os.path.join(day_path, 'eeg')
    eeg_files = []
    if not os.path.exists(eeg_folder_path):
        eeg_folder_path = day_path
    for file in os.listdir(eeg_folder_path):
        if re.match(r'.*\.md\.mc\.pm\.fe\.bp\.csv$', file):
            full_path = os.path.join(eeg_folder_path, file)
            relative_path = os.path.relpath(full_path, root_path)
            if full_path.startswith(root_path):
                eeg_files.append(relative_path)
            else:
                raise ValueError("Полный путь не находится внутри корневого пути")
            
    if len(eeg_files) == 1:
        return eeg_files[0]  
    elif len(eeg_files) > 1:
        return json.dumps(eeg_files)  
    else:
        return 0  

def get_gonogo_files(day_path, root_path):
    gonogo_folder_path = ''
    for gonogo_folder in ['gonogo', 'go_no_go']:
        if os.path.exists(os.path.join(day_path, gonogo_folder)):
            gonogo_folder_path = os.path.join(day_path, gonogo_folder)
    gonogo_files = []
    if not os.path.exists(gonogo_folder_path):
        gonogo_folder_path = day_path
    for file in os.listdir(gonogo_folder_path):
        if re.match(r'.*(_gonogo_).*\.pdf$|.*\.pdf$', file):
            full_path = os.path.join(gonogo_folder_path, file)
            relative_path = os.path.relpath(full_path, root_path)
            if full_path.startswith(root_path):
                gonogo_files.append(relative_path)
            else:
                raise ValueError("Полный путь не находится внутри корневого пути")
            
    if len(gonogo_files) == 1:
        return gonogo_files[0]  
    elif len(gonogo_files) > 1:
        return json.dumps(gonogo_files)  
    else:
        return 0  
    
def get_video_files(day_path, root_path):
    video_folder_path = ''
    for video_folder in ['video']:
        if os.path.exists(os.path.join(day_path, video_folder)):
            video_folder_path = os.path.join(day_path, video_folder)
    video_files = []
    if not os.path.exists(video_folder_path):
        video_folder_path = day_path
    for file in os.listdir(video_folder_path):
        if re.match(r'.*.mp4$', file):
            full_path = os.path.join(video_folder_path, file)
            relative_path = os.path.relpath(full_path, root_path)
            if full_path.startswith(root_path):
                video_files.append(relative_path)
            else:
                raise ValueError("Полный путь не находится внутри корневого пути")
            
    if len(video_files) == 1:
        return video_files[0]  
    elif len(video_files) > 1:
        return json.dumps(video_files)  
    else:
        return 0  

def process(root_path, csv_result):
    """
    Выполняет поиск всех искомых файлов исследования для каждого из респондентов. В итоге формируется (дополняется) CSV файл.
    Parameters:
        root_path (str): путь до репозитория с исследованиями.
        csv_result (str): путь до CSV файла, куда будут записаны все найденные файлы.
    """
    existing_data = read_csv_data(csv_result)
    try:
        process_respondent_folders(os.path.abspath(root_path), existing_data)
        write_to_csv(csv_result, existing_data)
    except ValueError as e:
        print(e)
