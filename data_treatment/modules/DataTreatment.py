
import csv
from dbfread import DBF
import pandas as pd
import glob
import sys
sys.path.append('./data_treatment')

class DataTreatment:
    def __init__(self, source_folder_path, destination_folder_path, file_pattern = ''):
        '''
            file_pattern: regex of files that should be treated, without extension
        '''
        self.file_pattern = file_pattern
        self.source_folder_path = source_folder_path
        self.destination_folder_path = destination_folder_path
    
    def extract_filename_from_path(self, filepath):
        last_dot = filepath.rindex('.')
        filename = filepath[:last_dot]

        filename = filename.split('/')[-1]
        return filename

    def transform_xlsx_to_csv_and_copy_to_destination_folder(self):
        if self.file_pattern == '':
            file_pattern = '*.xlsx'
        else:
            file_pattern = self.file_pattern + '.xlsx'
        
        print(self.source_folder_path + file_pattern)

        for file_path in glob.glob(self.source_folder_path + file_pattern):
            print(file_path)

            filename = self.extract_filename_from_path(file_path)

            xls = pd.read_excel(file_path)

            file_path = self.destination_folder_path + filename + '.csv'
            
            xls.to_csv(file_path,encoding='utf-8',index=False)
        

    def transform_dbf_to_csv_and_copy_to_destination_folder(self): 
        '''
        Function uses the source and filename as the path to a dbf file
        and output a csv, with same name to the destination folder, except extension
        '''
        if self.file_pattern == '':
            file_pattern = '*.dbf'
        else:
            file_pattern = self.file_pattern + '.dbf'

        print(self.source_folder_path + file_pattern)

        for file_path in glob.glob(self.source_folder_path + file_pattern):
            print(file_path)

            filename = self.extract_filename_from_path(file_path)
        
            csv_fn = self.destination_folder_path + filename + ".csv" #Set the csv file name
            table = DBF(file_path) # table variable is a DBF object
            with open(csv_fn, 'w', newline = '') as f: # create a csv file, fill it with dbf content
                writer = csv.writer(f)
                writer.writerow(table.field_names) # write the column name
                for record in table: # write the rows
                    writer.writerow(list(record.values()))