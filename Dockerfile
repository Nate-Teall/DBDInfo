# Use the python image
FROM python:3.12

# Specify the working directory
WORKDIR /usr/local/DBDInfo

# Copy all files from my host PC to the WorkDir of the container
COPY . .

# Run this to install flask
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# This is the command that will be used to run the app
#CMD ["echo", "'Container Started'"]