import time
import sys
sys.path.append('../../data_treatment')
sys.path.append('./data_treatment')
import os
from modules.DataTreatment import DataTreatment

start = time.time()

if 'WB' in os.getcwd():
    data_folder = '../../data/'
elif 'data_analysis' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'WB/PD_COMAP/matrices_time_distance/'
destination_folder_path = data_folder + 'WB/PD_COMAP/matrices_time_distance/'

dt = DataTreatment(source_folder_path, destination_folder_path)
dt.transform_xlsx_to_csv_and_copy_to_destination_folder()

source_folder_path = data_folder + 'WB/PD_COMAP/scenarios/'
destination_folder_path = data_folder + 'WB/PD_COMAP/scenarios/'

dt = DataTreatment(source_folder_path, destination_folder_path)
dt.transform_xlsx_to_csv_and_copy_to_destination_folder()

end = time.time()

print("Time to complete Data Treatment: ", end-start)