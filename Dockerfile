FROM python:3.7
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt && pip install gunicorn
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#ENV DEBUG 1
CMD bash /app/run.sh
