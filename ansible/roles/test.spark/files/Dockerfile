FROM openjdk:11-slim-buster

COPY . .

RUN apt-get update && apt-get -y install python3 python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm -fr requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*  && \
    apt-get remove --auto-remove -y python3-pip

RUN  python3 -m compileall -b / && \
    find . -name '*.py' -delete
    
ENV JAVA_HOME=/usr/local/openjdk-11 TARGET_HOST="{{ groups['namenode'][0] }}"

CMD ["python3", "spark.pyc"]