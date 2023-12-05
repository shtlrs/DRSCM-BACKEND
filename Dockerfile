FROM python:3.11.7-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN \
    SECRET_KEY=dummy_value \
    DEBUG=1 \
    python manage.py collectstatic --noinput --clear

EXPOSE 8000

ENTRYPOINT ["python", "manage.py"]

CMD ["run"]
