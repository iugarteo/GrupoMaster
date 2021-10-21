FROM python:3.6-slim
ADD ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install requests
EXPOSE 8000
ENTRYPOINT gunicorn -b 0.0.0.0:8000 app:app