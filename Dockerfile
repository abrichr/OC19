FROM python:3.7
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt && pip install gunicorn
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#ENV DEBUG 1
CMD gunicorn -b 0.0.0.0:$PORT \
    #--access-logfile /var/log/gunicorn-access.log \
    #--error-logfile /var/log/gunicorn-error.log \
    app:app \
    --log-level DEBUG
