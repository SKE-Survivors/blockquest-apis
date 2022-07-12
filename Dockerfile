FROM python:3.8-alpine

RUN pip install --upgrade pip

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "app/app.py"]