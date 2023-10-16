import traceback
import pika
import threading
import logging
from pika.exceptions import StreamLostError, ChannelWrongStateError
import json
import time


class RabbitMQManager:
    def __new__(cls, host, port, vhost, user, passwd, exchange, queue_name, error_exchange=None):
        if not hasattr(cls, "instance"):
            cls.instance = super(RabbitMQManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, host, port, vhost, user, passwd, exchange, queue_name, error_exchange=None):
        self.host = host
        self.port = port
        self.vhost = vhost
        self.credential = pika.PlainCredentials(user, passwd)
        self.exchange = exchange
        self.queue_name = queue_name
        self.error_exchange = error_exchange
        self.consumer_channel = None
        self.producer_channel = None
        self.is_stopped = False
        self.is_retry_producer_connection = False

    def init_args(self):
        self.consumer_channel = None
        self.producer_channel = None
        self.is_stopped = False
        self.is_retry_producer_connection = False

    def init_producer_channel(self, retry=0):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port, virtual_host=self.vhost, credentials=self.credential))
            self.producer_channel = connection.channel()
            self.is_retry_producer_connection = False
            logging.info(f"init_producer_channel: {retry}")
        except Exception:
            self.is_retry_producer_connection = True
            time.sleep(30)
            retry += 1
            logging.info(f"init retry count: {retry}")
            threading.Thread(target=self.init_producer_channel, kwargs={"retry": retry}).start()

    def error_stack_rabbitmq(self, message=None, retry=0, error_location=None):
        try:
            json_msg = json.dumps(message.decode())
            if self.error_exchange:
                properties = pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
                self.producer_channel.basic_publish(self.error_exchange, "", json_msg, properties=properties)
            logging.warn(f"error message stack to rabbitmq: {json_msg}")
        except Exception:
            logging.error(traceback.format_exc())

            retry += 1
            if self.is_retry_producer_connection == False:
                self.is_retry_producer_connection = True
                if self.producer_channel.is_open:
                    self.producer_channel.close()
                threading.Thread(target=self.init_producer_channel).start()

            time.sleep(30)
            threading.Thread(target=self.error_stack_rabbitmq, kwargs={"message": message, "retry": retry, "error_location": error_location}).start()

    def start_subscription(self, callback=None):
        self.stop_subscription()
        self.init_producer_channel()
        threading.Thread(target=self.subscription, kwargs={"callback": callback}).start()

    def subscription(self, callback=None, retry=0):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port, virtual_host=self.vhost, credentials=self.credential))
            self.consumer_channel = connection.channel()

            self.consumer_channel.queue_bind(exchange=self.exchange, routing_key="", queue=self.queue_name)
            self.consumer_channel.basic_consume(self.queue_name, callback)
            logging.info(f"start rabbitmq consuming: retry: {retry}")
            self.consumer_channel.start_consuming()
        except Exception:
            if self.is_stopped == True:
                logging.info("end of rabbitmq consuming")
            else:
                logging.info(f"reconnect rabbitmq consuming: {retry}")
                if self.consumer_channel.is_open:
                    self.consumer_channel.close()
                time.sleep(30)
                threading.Thread(target=self.subscription, kwargs={"callback": callback, "retry": retry}).start()

    def stop_subscription(self):
        if self.consumer_channel is not None:
            self.is_stopped = True
            logging.info("stop rabbitmq consuming")
            try:
                self.consumer_channel.stop_consuming()
            except StreamLostError:
                logging.info("stopped of rabbitmq consuming")
