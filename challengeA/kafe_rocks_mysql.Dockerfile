FROM mysql:5

ENV MYSQL_ALLOW_EMPTY_PASSWORD=yes

COPY schema.sql /docker-entrypoint-initdb.d/ 