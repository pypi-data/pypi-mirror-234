from confluent_kafka import Consumer


class KafkaConsumer:
    def __init__(
        self,
        host,
        username,
        password,
        group_id,
        mechanism="PLAIN",
        security_protocol="SASL_SSL",
        auto_offset_reset="earliest",
    ):
        config = self._set_conn_config(
            host, group_id, username, password, mechanism, security_protocol, auto_offset_reset
        )
        self.consumer = Consumer(config)
        self.topics = []

    @staticmethod
    def _set_conn_config(host, group_id, username, password, mechanism, security_protocol, auto_offset_reset):
        """
        Method used to construct connection required attributes.
        This method handles configuration differently if the broker host is
        determined to be a local server.
        """
        config = {"bootstrap.servers": host, "group.id": group_id, "auto.offset.reset": auto_offset_reset}
        if not any(["localhost" in host, "172.0.0.1" in host]):
            config.update(
                {
                    "sasl.username": username,
                    "sasl.password": password,
                    "sasl.mechanism": mechanism,
                    "security.protocol": security_protocol,
                }
            )
        return config

    def subscribe_topic(self, topic_name):
        self.topics.append(topic_name)
        self.consumer.subscribe(self.topics)

    def listen(self, timeout, func, **kwargs):
        try:
            while True:
                msg = self.consumer.poll(timeout=float(timeout))
                if msg:
                    if msg.error():
                        print(msg.error())
                        print("ERROR: %s".format(msg.error()))
                    else:
                        func(msg.topic(), msg.key().decode("utf-8"), msg.value().decode("utf-8"), **kwargs)
        except KeyboardInterrupt:
            self.consumer.close()
