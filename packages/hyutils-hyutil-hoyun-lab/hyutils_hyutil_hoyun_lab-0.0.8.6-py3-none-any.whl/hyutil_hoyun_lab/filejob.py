import os

def make_new_file_name_by_number(class_name, number):
    if class_name is None or number is None or number < 0:
        return ''
    return class_name + '_' + str(number).rjust(6, '0')

def get_path_filename_ext(file_path):
    if file_path is None:
        return '', '', ''
    dir_name = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    filenames = os.path.splitext(filename)
    return dir_name, filenames[0], filenames[1]
