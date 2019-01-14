FROM python:3

COPY . /app

WORKDIR /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

CMD [ "python", "./app.py" ]