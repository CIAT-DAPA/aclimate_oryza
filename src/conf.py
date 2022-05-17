import os

config = {}

if os.getenv('DEBUG', "true").lower() == "true":
    config['SECRET_KEY']='Loc@lS3cr3t'
    config['CURRENT_USER']='forecast'
    config['CURRENT_PWD']='My11v3S3cret4'
    config['DEBUG']=True
    config['ROOT_PATH']="D:\\CIAT\\Code\\USAID\\aclimate_oryza"
    config['HOST']='localhost'
    config['PORT']=5000
    config['R_COMMAND']="C:\\Users\\hsotelo\\AppData\\Local\\Programs\\R\\R-4.2.0\\bin\\Rscript.exe"
else:
    config['SECRET_KEY']=os.getenv('SECRET_KEY')
    config['CURRENT_USER']=os.getenv('CURRENT_USER')
    config['CURRENT_PWD']=os.getenv('CURRENT_PWD')
    config['DEBUG']=False
    config['ROOT_PATH']=os.getenv('ROOT_PATH')
    config['HOST']='0.0.0.0'
    config['PORT']=os.getenv('PORT')
    config['R_COMMAND']=os.getenv('R_COMMAND')

