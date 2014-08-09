# https://docs.newrelic.com/docs/python/
# https://docs.newrelic.com/docs/python/python-agent-and-heroku

# Without NewRelic
#web: waitress-serve --port=$PORT {{ project_name }}.wsgi:application
web: python manage.py collectstatic --noinput ; gunicorn {{ project_name }}.wsgi:application 0.0.0.0:$PORT -w 1
#web: gunicorn {{ project_name }}.wsgi:application 0.0.0.0:$PORT -w 1
#web: python manage.py runserver 0.0.0.0:$PORT

# With NewRelic
#web: newrelic-admin run-program python manage.py runserver 0.0.0.0:$PORT
#web: newrelic-admin run-program gunicorn {{ project_name }}.wsgi:application 0.0.0.0:$PORT -w 1
#web: newrelic-admin run-program waitress-serve --port=$PORT {{ project_name }}.wsgi:application

# Worker
worker: python worker.py
