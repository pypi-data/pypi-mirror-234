import datetime
import os


KAFKA_HOST = os.environ.get("KAFKA_HOST")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
KAFKA_API_KEY = os.environ.get("KAFKA_API_KEY")
KAFKA_API_SECRET = os.environ.get("KAFKA_API_SECRET")


from important.kafka.producer import KafkaProducer


kakfa = KafkaProducer(host=KAFKA_HOST, topic_name=TOPIC_NAME, username=KAFKA_API_KEY, password=KAFKA_API_SECRET)


key = "test_channel_id:123"
value = str(datetime.datetime.utcnow())
kakfa.async_send(key=key, value=value)
