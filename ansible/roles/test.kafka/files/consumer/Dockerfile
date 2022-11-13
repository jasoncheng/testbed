FROM python:3.8-slim
COPY . /
RUN pip install -r requirements.txt
ENV TYPE=c
ENV hostConsumer=bd2
CMD [ "python3", "./main.py" ]
