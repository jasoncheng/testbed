FROM python

COPY . .

RUN pip install --no-cache-dir -r requirements.txt && \
    rm -fr requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ENV TARGET_HOST=52.194.183.51
CMD ["python3", "./hbase.py"]