from .helper_variables import ROOT_DIR, UPLOAD_FOLDER_PATH

import time

def upload_file(file):

    file_ext = file.split('.')[1]

    unique_file_name = "file_" + str(time.time()).split('.')[0] + file_ext
    file_path = UPLOAD_FOLDER_PATH + "/" + unique_file_name
    
    print("Writing file to: " + file_path)
    
    try:
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    except:
        print("Something went wrong!")
    



