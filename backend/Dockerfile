FROM python:3.8-slim

LABEL author="Pavel Lyutichenko" email="motry@yandex.ru"

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip 
RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000" ]
