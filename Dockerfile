# Use the official Python 3.9 image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code
COPY . /app

# Install cron and setup cron job
RUN apt-get update && apt-get -y install cron \
    && echo "*/30 * * * * (/usr/local/bin/python /app/main.py | tee -a /var/log/cron.log) 2>&1" | crontab -

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Add alias to run rate.py
RUN echo "alias rate='/usr/local/bin/python /app/rate.py'" >> ~/.bashrc

# Run the command on container startup
CMD ["/bin/bash", "-c", "printenv > /etc/environment && cron -f"]