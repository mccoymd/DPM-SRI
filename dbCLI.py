import sys
import os
from os import listdir
from os.path import isfile, join
from app.utils import file_transform

def get_directory(args):
    try:
        return sys.argv[1]
    except:
        print("Please pass a directory")

def get_files(directory):
    dir_list = listdir(directory)
    results = []

    for f in dir_list:
        name = join(directory, f)
        if isfile(name):
            path = os.path.abspath(name)
            results.append(path)

    return results

def sort_files(files):
    id_dict = {}

    for f in files:
        split = os.path.splitext(f)
        extension = split[1]

        if (extension != ".txt") and (extension != ".csv"):
            print("Invalid file type, only csv and txt accepted but found: {0}".format(f))
            continue

        name_split = split[0].split("/")[-1].split("_")
        file_id = name_split[2]

        if file_id not in id_dict:
            id_dict[file_id] = {"dosage": None, "param": None, "pop": None, "stopt": None}

        files_dict = id_dict.get(file_id)
        file_type = name_split[0]

        if "param" in file_type:
            files_dict["param"] = f
        elif "stopt" in file_type:
            files_dict["stopt"] = f
        elif "dosage" in file_type:
            files_dict["dosage"] = f
        elif "pop" in file_type:
            files_dict["pop"] = f
        elif "strat" in file_type:
            file_transform.process_strategies_file(f)
        else:
            print("Invalid file name found: {0}".format(f))

    return id_dict

def convert_txt(f, directory):
    split = os.path.splitext(f)
    name = split[0]
    extension = split[1]

    if extension == ".txt":
        output = join(directory, name) + ".csv"
        file_transform.convert_txt(f, output)
        return output

    return f

def process_param_file(param_file, file_id, directory):
    result = convert_txt(param_file, directory)
    file_transform.process_param_file(result, file_id)

def process_stopt_file(stopt_file, directory):
    result = convert_txt(stopt_file, directory)
    file_transform.process_stopt_file(result)

def process_dosage_file(dosage_file, directory):
    result = convert_txt(dosage_file, directory)
    file_transform.process_dosage_file(result)

def process_pop_file(pop_file, directory):
    result = convert_txt(pop_file, directory)
    file_transform.process_pop_file(result)

def process_files(id_dict, directory):
    for file_id in id_dict.keys():
        files = id_dict[file_id]

        param_file = files["param"]
        pop_file = files["pop"]
        stopt_file = files["stopt"]
        dosage_file = files["dosage"]

        if param_file is not None: process_param_file(param_file, file_id, directory)

        if pop_file is not None: process_pop_file(pop_file, directory)

        if stopt_file is not None: process_stopt_file(stopt_file, directory)

        if dosage_file is not None: process_dosage_file(dosage_file, directory)



if __name__ == "__main__":
    directory = get_directory(sys.argv)
    files = get_files(directory)
    id_dict = sort_files(files)
    process_files(id_dict, directory)

