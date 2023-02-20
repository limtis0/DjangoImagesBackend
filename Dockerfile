FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR .
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENV DJANGO_SUPERUSER_USERNAME="admin"
ENV DJANGO_SUPERUSER_EMAIL="admin@email.com"
ENV DJANGO_SUPERUSER_PASSWORD="DbUZ1Qe86qWcxWHJNsilmB"

RUN mkdir static
RUN python3 manage.py migrate
RUN python3 manage.py createsuperuser --noinput

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
