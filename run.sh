echo "DEBUG=$DEBUG"
if [ "$DEBUG" = "1" ]; then
  echo "running make dev"
  make dev
else
  echo "running make prod"
  make prod;
fi
#cd app
    #--access-logfile /var/log/gunicorn-access.log \
    #--error-logfile /var/log/gunicorn-error.log \


# XXX remove

gunicorn -b 0.0.0.0:8080 \
    app:app \
    --log-level "$LOG_LEVEL"
