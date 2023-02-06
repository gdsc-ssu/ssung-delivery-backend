FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80
 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]