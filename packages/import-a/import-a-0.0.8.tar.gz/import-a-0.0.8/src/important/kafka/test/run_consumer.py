import os

from important.kafka.consumer import KafkaConsumer

KAFKA_HOST = os.environ.get("KAFKA_HOST")
KAFKA_API_KEY = os.environ.get("KAFKA_API_KEY")
KAFKA_API_SECRET = os.environ.get("KAFKA_API_SECRET")
GROUP_ID = os.environ.get("GROUP_ID")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
POLLING_TIMEOUT_SECS = os.environ.get("POLLING_TIMEOUT_SECS")


# We can use this as the control plane for the various kafka-based functionalities
# so the actual listener method stays simple and agnostic to the usecase
def kafka_consumer_controller(topic, msg_key, msg_value, **kwargs):
    if msg_key == "test_channel_id:123":
        print("123")
    else:
        print("abc")


# Create Consumer instance
consumer = KafkaConsumer(KAFKA_HOST, KAFKA_API_KEY, KAFKA_API_SECRET, GROUP_ID)
consumer.subscribe_topic(TOPIC_NAME)
consumer.listen(POLLING_TIMEOUT_SECS, kafka_consumer_controller)
