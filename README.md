# OnCOVID-19

This repo contains the code for the [oncovid19.com](http://oncovid19.com)
website.

In the below, replace 'dev' with 'prod' for production environments.

## Setup

```
pip install -r requirements
echo 'SQLALCHEMY_DATABASE_URI=<database_uri>' >> .env_dev
# for sending email confirmations
echo 'MAIL_PASSWORD' >> .env_dev
```

## Run

```
make dev
python manage.py runserver
```

## Troubleshooting

### Docker on Heroku

Set stack:

```
heroku stack:set container
```

### `SMTPAuthenticationError` during email verification

See:
- https://stackoverflow.com/a/27515883/95989
- https://stackoverflow.com/a/54625596/95989

## Acknowledgements

Based on https://github.com/MaxHalford/flask-boilerplate
