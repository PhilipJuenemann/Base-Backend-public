FROM python:3.8.6-buster

COPY api /api
COPY requirements.txt /requirements.txt
COPY packagefunctions /packagefunctions

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -e ./packagefunctions
RUN spacy download en_core_web_sm

CMD uvicorn api.app:app --host 0.0.0.0 --port $PORT
