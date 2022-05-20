import os
from datetime import datetime
import shutil
import zipfile
import subprocess
import glob

class OryzaAPI(object):

    root = ''
    r_cmd = ''

    # Method construct
    def __init__(self, root, r_cmd):
        self.root = root
        self.r_cmd = r_cmd

    # Method that creates folder if they don't exist
    # (tuple) id,path: Id of process and Path for the workspace
    def mkdir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    # Method that creates an enviroment to execute the scripts of R
    # each time by separate space into of workspace
    # (string) return: Enviroment path
    def create_env(self):
        # Create workspace if it doesn't exist
        path = os.path.join(self.root,"workspace")
        self.mkdir(path)
        # Create folder date
        now = datetime.now()
        path = os.path.join(path,now.strftime("%Y%m%d"))
        self.mkdir(path)
        # Create folder for execution
        now = str(round(datetime.timestamp(now)))
        path = os.path.join(path,now)
        self.mkdir(path)
        return (now,path)

    # Method that executes R Scripts to generate Oryza Forecast
    # (stream) zip: All inputs compressed
    def generate_forecast(self, zip):
        # Creating space for
        (id,env) = self.create_env()
        print("Working in:",env)

        # Copy library to workspace
        shutil.copytree(os.path.join(self.root,"oryza_api"),os.path.join(env,"oryza_api"))

        # Uncomprssing zip
        print("Uncompressing inputs data",id)
        with zipfile.ZipFile(zip,"r") as zip_ref:
            zip_ref.extractall(os.path.join(env,"oryza_api"))

        # Executing R Script
        print("Executing Oryza API R Script")
        script = os.path.join(env,"oryza_api","00_run_oryza_aclimate.R")
        script = "source('" + script.replace("\\","/") + "')"
        outputs_cmd = subprocess.run([self.r_cmd, "-e", script],stdout=subprocess.DEVNULL)
        print("Getting output")
        outputs = os.path.join(env,"oryza_api","outputs","*.csv")
        outputs_files = glob.glob(outputs)

        # Always it takes the first and unique csv in this folder
        if len(outputs_files) > 0:
            return outputs_files[0]
        else:
            return None






