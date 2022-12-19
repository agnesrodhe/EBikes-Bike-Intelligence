# # For more information, please refer to https://aka.ms/vscode-docker-python
# FROM python:3.8-slim

# # Keeps Python from generating .pyc files in the container
# ENV PYTHONDONTWRITEBYTECODE=1

# # Turns off buffering for easier container logging
# ENV PYTHONUNBUFFERED=1

# # Install pip requirements
# COPY requirements.txt .
# RUN python -m pip install -r requirements.txt

# WORKDIR /bike_intelligence
# COPY bike_simulation.py ./

# # # Creates a non-root user with an explicit UID and adds permission to access the /app folder
# # # For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# # RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# # USER appuser

# # During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["python", "bike_simulation.py"]

FROM debian:stretch-slim

RUN apt update
RUN apt install -y python3-pip

WORKDIR /src

COPY src/testing.py /src
COPY src/requirements.txt /src

RUN pip3 install -r requirements.txt

CMD [ "python3", "testing.py"]
