import csv, os 
from . import gonogo
from openmindlab.base.csv.base_writer import BaseWriter as CsvBaseWriter

class GoNoGoReportHandler(CsvBaseWriter):
    def __init__(self, output_file):
        super().__init__(output_file)
        self.writer = csv.DictWriter(self.file, fieldnames=['respondentID', 'day', 'times', 'response_time', 'accuracy', 'overall_score', 'attempt_num', 'score'])
        self.writer.writeheader()

    def process(self, file_path):
        combined_dict = {}
        extracted_info = gonogo.processing.extract_info_from_gonogo_filename(os.path.basename(file_path))
        file_info = gonogo.processing.extract_info_from_gonogo_file(file_path)
        gonogo_result = gonogo.processing.extract_and_validate_numbers(file_info)
        if isinstance(extracted_info, dict) and isinstance(gonogo_result, dict):
            combined_dict = {**extracted_info, **gonogo_result}
            super().handle(combined_dict)
            print(combined_dict)
        return combined_dict