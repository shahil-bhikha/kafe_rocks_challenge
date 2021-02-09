# Kafe Rocks Challenge

## General

Given there is freedom to use any tooling to accomplish the task, I decided to keeps things as simple as possible in the interest of local development and  deployment. Python was used as the programming language of choice although I did consider using Golang as well. Mysql was chosen as the database for storage. If this was in production would consider a data warehouse instead.

## Challenge A : Automated Data Pipeline

Metroboard was chosen as the webservice to extract data from. Please go ahead and set up an account and create a test board of your choice. Once an account and board have been created, update `config.ini` with the username, password and the board name. For the time being a config file will suffice but ideally something like AWS ASM would be better to use.

This pipeline uses Docker to execute the ETL and provide the storage so make sure Docker is running. Looking closely at the code. A `metroretro` class was created which houses the logic to connect to the webservice and download the work board of your choice. The `db` class contains methods to connect to a mysql db and execute queries against it.

Cron is used to execute the `main.py` file. The `crontab` file can be updated to control when this ETL pipeline should be run. Its currently set to 5 mins.

### How to execute locally?

We'll first begin by running mysql. The `schema.sql` file contains the database and table to be created. This file gets injected into the mysql container and executed upon start up. No password is set for the mysql DB and the root user is used but this can be updated in the following file `kafe_rocks_mysql.Dockerfile`. Obviously this isn't good practice but okay for local development.

Execute:
Build mysql docker image and run.
```
docker build --rm -f "kafe_rocks_mysql.Dockerfile" -t kaferocksmysql:latest .
docker run --detach --name=kaferocksmysql kaferocksmysql:latest
```
Get the IP address of the container.
```
docker inspect kaferocksmysql | grep IPAddress
```
Head to the `config.ini` file and set the db_host to the IP address. 

Build kafe_rocks docker image and run.
```
docker build --rm -f "kafe_rocks.Dockerfile" -t kafechallenge:latest .
docker run --rm --name=kafechallenge --link kaferocksmysql:mysql kafechallenge:latest
```
When the container is run, StdOut is tailing the cron.log file.

## Challenge B : Automated Data Flow

In order for the reports to be generated, all files must be added to the following directory `Data_Engineer_Challenge_-_Data`. The directory can be updated in the `main.py` if the files are located elsewhere. Some helper functions have been added to the `util.py` file. These untility functions read in the files from the directory, sorts them according to type and converts them to dataframes. Data is cleaned, transformed, filtered and finally the reports are generated and saved.

### How to execute locally?

Execute:
```
python main.py -id=14
```

