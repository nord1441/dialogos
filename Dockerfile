FROM ubuntu:24.04
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv nginx
ADD django-aichat /usr/local/bin/django-aichat
WORKDIR /usr/local/bin/django-aichat
RUN python3 -m venv venv
RUN venv/bin/pip3 install django openai django-bootstrap5 Pillow gunicorn google-genai notion-client pytz
RUN cp /usr/local/bin/django-aichat/nginx.conf /etc/nginx/nginx.conf
ENTRYPOINT /bin/sh -c "venv/bin/python manage.py makemigrations && venv/bin/python manage.py migrate && venv/bin/python manage.py createsuperuser --noinput || true && venv/bin/gunicorn -D mascot.wsgi:application -b 0.0.0.0:8000 && nginx && sleep infinity"
