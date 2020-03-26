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


gunicorn -b 0.0.0.0:$PORT \
    app:app \
    --log-level "$LOG_LEVEL"
