# pull base image
FROM python:3.13-alpine

# set env variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# work directory
WORKDIR /code

# install project dependency
COPY requirements.txt /code/
RUN python -m pip install -r requirements.txt

# copy project
COPY . .