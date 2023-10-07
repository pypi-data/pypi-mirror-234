from confluent_kafka import Producer


class KafkaProducer:
    def __init__(
        self,
        host,
        topic_name,
        username,
        password,
        mechanism="PLAIN",
        security_protocol="SASL_SSL",
        flushing_interval_secs=1.0,
        verbose=1.0,
    ):
        self.topic_name = topic_name
        self.flushing_interval_secs = flushing_interval_secs
        self.verbose = verbose

        config = self._set_conn_config(host, username, password, mechanism, security_protocol)

        self.producer = Producer(config)

    @staticmethod
    def _set_conn_config(host, username, password, mechanism, security_protocol):
        """
        Method used to construct connection required attributes.
        This method handles configuration differently if the broker host is
        determined to be a local server.
        """
        config = {"bootstrap.servers": host}
        print(host)
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

    @staticmethod
    def _delivery_callback(err, msg):
        if err:
            print("ERROR: Message failed delivery: {}".format(err))
        else:
            print(
                "Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
                    topic=msg.topic(), key=msg.key().decode("utf-8"), value=msg.value().decode("utf-8")
                )
            )

    def _add_msg_to_producer_buffer(self, key, value):
        cb = self._delivery_callback if self.verbose > 0 else None
        self.producer.produce(topic=self.topic_name, key=key, value=value, callback=cb)

    def send(self, key, value):
        self._add_msg_to_producer_buffer(key, value)
        self.producer.flush()

    def async_send(self, key, value):
        self._add_msg_to_producer_buffer(key, value)
        self.producer.poll(self.flushing_interval_secs)
