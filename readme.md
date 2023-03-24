# Aclimate Oryza

This repository contains a Web API which allows to run Oryza model.

## Requirements

The following steps are required to install the services

### R Packages
Before to start the service, the following packages should be installed

```
install.packages(c("foreach","parallel","iterators","doParallel","rebus","dplyr","purrr","readr","lubridate","stringr","lazyeval","magrittr","tictoc"))
```

### Python requirements
For installing the packages required, you should execute the following command

```
pip install -r requirements.txt
```

### Enviroment vars
The system requires set enviroments vars. For setting env vars you use:

```
set SECRET_KEY=Loc@lS3cr3t

```

* DEBUG: Set if you are debbuging or production enviroment
* SECRET_KEY: It is the secret key to chiper the password
* CURRENT_USER: Name of current user of the service
* CURRENT_PWD: User password
* ROOT_PATH: Path where the service is located
* PORT: Port in which services should be execute
* R_COMMAND: Path where R command is located

## Run

To execute in background

```
pip install waitress
pythonw api.py > log.txt 2>&1
```

To stop 

```
netstat -ano
taskkill /PID <PROCESS ID> /F
```
