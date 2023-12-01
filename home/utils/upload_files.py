from .helper_variables import ROOT_DIR, UPLOAD_FOLDER_PATH

import time

def upload_file(file):
    unique_file_name = "file_" + str(time.time()).split('.')[0] + ".txt"
    file_path = UPLOAD_FOLDER_PATH + "/" + unique_file_name
    print(file_path)
    with open(file_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)



