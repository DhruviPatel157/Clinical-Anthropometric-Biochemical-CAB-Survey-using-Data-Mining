import os
import dataClean

dir_list = ['MP']

for dir_name in dir_list:
    directory = os.fsencode(dir_name)
    for file in os.listdir(directory):
        input_file = os.fsdecode(file)
        if(input_file.endswith(".csv")):
            file_path = './' + dir_name
            output_dir_name = './' + dir_name + '/cleanedData/'
            dataClean.cleanData(input_file,file_path,output_dir_name)