# Created by Aleksey Gilenko
# December 2020

try:
    import datetime
    import json


except ImportError:
    dependencies = ["datetime", "json"]
    notimported=[]
    for library in dependencies:

        try:
            exec ("import "+str(library))
        except ImportError:
            notimported.append(library.split()[0])
        except Exception:
            print("Unknown error")

    if len(notimported)!=0:
        print("Issues with importing following libraries:\n")
        for i in notimported:
            print("    - "+i+"\n")
        print("Try download or reinstall them and again after")

class Writer:
    def __init__(self, data_file, log_file):
        self.data_file=str(data_file)
        self.log_file=str(log_file)
        self.write_message("Logwriter started")
    def write_message(self, message):
        self.file=open(self.log_file,  "a")
        self.file.write('<{}>: '.format(datetime.datetime.now())+message+'\n')
        self.file.close()
    def write_data(self, data):
        self.file=open(self.data_file, "a")
        json.dump(data, self.file)
        self.file.write("\n")
        self.file.close()