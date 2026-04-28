FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8989

ENTRYPOINT ["python", "app/hello.py"]