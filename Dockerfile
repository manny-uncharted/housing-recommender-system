FROM codingforentrepreneurs/python:3.9-webapp-cassandra

COPY . /app

WORKDIR /app

RUN chmod +x entrypoint.sh
RUN chmod +x  setup.sh

EXPOSE 8501

RUN python3 -m venv /opt/venv && /opt/venv/bin/python -m pip install -r requirements.txt

RUN /opt/venv/bin/python -m pypyr /app/src/pipelines/dataset-download
RUN ./setup.sh


CMD [ "./entrypoint.sh" ]