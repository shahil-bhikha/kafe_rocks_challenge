Kafe Rocks Challenge


Build docker images
docker build --rm -f "kafe_rocks.Dockerfile" -t kafechallenge:latest .
docker build --rm -f "kafe_rocks_mysql.Dockerfile" -t kaferocksmysql:latest .


Get mysql ip address
docker inspect kafe-rocks-mysql

Run docker mysql container
docker run --detach --name=kaferocksmysql kaferocksmysql:latest

Run cron job container
docker run --rm -it --link kaferocksmysql:mysql kafechallenge:latest bash
