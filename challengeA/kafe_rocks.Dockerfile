FROM python:3

# Install cron package
RUN apt-get update && apt-get -y upgrade 
RUN apt-get -y install cron

# Add scripts to the container
COPY . /kafe-rocks-challenge
ENV PYTHONPATH="${PYTHONPATH}:/kafe-rocks-challenge"
WORKDIR /kafe-rocks-challenge
RUN pip install -r /kafe-rocks-challenge/requirements.txt
  
# Add cron jobs
ADD crontab /etc/cron.d/jobs
RUN chmod 0644 /etc/cron.d/jobs
RUN crontab /etc/cron.d/jobs

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Start processes
ENTRYPOINT cron start && tail -f /var/log/cron.log