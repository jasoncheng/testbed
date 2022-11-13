from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import kafka_errors
import traceback
import json
import os
import time
import logging

def producerDemo():
    print("producer start send message....")
    print("Producer {}:{}".format(hostProducer, port))
    producer = KafkaProducer(
        bootstrap_servers=[hostProducer+":"+port],
        key_serializer=lambda k: json.dumps(k).encode(),
        value_serializer=lambda v: json.dumps(v).encode(),
        api_version=(3, 3, 1),
        retries=10,
        request_timeout_ms=60000,
        max_block_ms=120000)
    
    for i in range(0, 240):
        _ = producer.send(
            topic,
            key='count_num',
            value=str(i),
        )
        print("send {}".format(str(i)))
        time.sleep(0.5)
            
def consumerDemo():
      print("consumer start serving....")
      print("consumer {}:{}".format(hostConsumer, port))
      consumer = KafkaConsumer(
          topic,
          bootstrap_servers=hostConsumer+":"+port,
        #   group_id=consumerGroup,
          api_version=(3, 3, 1),
          retry_backoff_ms=6000,
          session_timeout_ms=60000,
          consumer_timeout_ms = 1200000
      )
      
      for message in consumer:
          print("receive, offset: {}, key: {}, value: {}".format(
              message.offset,
              json.loads(message.key.decode()),
              json.loads(message.value.decode())
          ))
      consumer.close()

# Setup Env
hostProducer = os.environ['hostProducer']  if "hostProducer" in os.environ else 'bd1'
hostConsumer = os.environ['hostConsumer'] if 'hostConsumer' in os.environ else 'bd1'
consumerGroup = os.environ['group'] if 'group' in os.environ else 'group1'
debug = os.environ['debug'] if 'debug' in os.environ else ''
topic = "demo4"
port = "9092"

if debug != "":
    logging.basicConfig(level = logging.DEBUG)

if('TYPE' in os.environ and os.environ["TYPE"] == "c"):
    consumerDemo()
else:
    producerDemo()