import time
import sys
sys.path.append('../../data_analysis')
sys.path.append('./data_analysis')
import os
from modules.DataTreatment import DataTreatment

start = time.time()

if 'data_analysis' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'ciclocidade_research/multimodal/'
destination_folder_path = data_folder + 'ciclocidade_research/multimodal/'

dt = DataTreatment(source_folder_path, destination_folder_path)
dt.transform_xlsx_to_csv_and_copy_to_destination_folder()

end = time.time()

print("Time to complete Data Treatment: ", end-start)