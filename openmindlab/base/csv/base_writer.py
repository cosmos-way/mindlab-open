import csv, os 

class BaseWriter:
    def __init__(self, output_file):
        self.output_file = output_file
        self.file = open(output_file, 'w', newline='', encoding='utf-8')
        # self.writer = csv.writer(self.file)
    
    def handle(self, data):
        if isinstance(data, dict):
            self.writer.writerow(data)
            
    def process(self, file_path):
        pass
    
    def close(self):
        self.file.close()