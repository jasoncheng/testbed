FROM python:3.8-slim
COPY . /
RUN pip install -r requirements.txt
ENV TYPE=p
ENV hostProducer=bd1
CMD [ "python", "./main.py" ]