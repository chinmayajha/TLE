FROM python:3.8-slim-buster

WORKDIR /app
RUN apt-get update && apt-get install tk-dev -y
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ARG PORT=5000
ENV PORT=$PORT
COPY . .
RUN chmod +x ./run.sh
CMD [ "./run.sh"]
