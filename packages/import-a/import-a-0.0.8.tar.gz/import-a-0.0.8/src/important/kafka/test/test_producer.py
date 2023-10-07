import unittest

from important.kafka.producer import KafkaProducer


class TestProducer(unittest.TestCase):

    def setUp(self):
        self.test_topic_name = 'test_topic'
        self.test_username = 'test_username'
        self.test_password = 'test_password'
        self.test_mechnism = 'PLAIN'
        self.test_security_protocol='SASL_SSL'

    def test_connection_config_local(self):
        # Given
        localhost = 'localhost:9092'

        # When
        actual_config = KafkaProducer(host=localhost,
                                      topic_name=self.test_topic_name,
                                      username=self.test_username,
                                      password=self.test_password,)\
            ._set_conn_config(host=localhost,
                              username=self.test_username,
                              password=self.test_password,
                              mechanism=self.test_mechnism,
                              security_protocol=self.test_security_protocol)

        expected_config = {'bootstrap.servers': localhost}

        # Then
        self.assertDictEqual(actual_config, expected_config)

    def test_connection_config_remote(self):
        # Given
        remotehost = 'abc.us-west-2.aws.confluent.cloud:9092'

        # When
        actual_config = KafkaProducer(host=remotehost,
                                      topic_name=self.test_topic_name,
                                      username=self.test_username,
                                      password=self.test_password,)\
            ._set_conn_config(host=remotehost,
                              username=self.test_username,
                              password=self.test_password,
                              mechanism=self.test_mechnism,
                              security_protocol=self.test_security_protocol)

        expected_config = {'bootstrap.servers': remotehost,
                           'sasl.username': self.test_username,
                           'sasl.password': self.test_password,
                           'sasl.mechanism': self.test_mechnism,
                           'security.protocol': self.test_security_protocol}

        # Then
        self.assertDictEqual(actual_config, expected_config)


if __name__ == '__main__':
    unittest.main()
