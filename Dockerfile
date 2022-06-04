FROM --platform=linux/amd64 amd64/python:latest

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD gunicorn --env DJANGO_SETTINGS_MODULE=root.settings -b 0.0.0.0:10000 core/root.wsgi