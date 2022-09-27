import json
from logging import getLogger

from paho.mqtt.client import Client

logger = getLogger(__name__)


def setup_client(host: str, username: str, password: str) -> Client:
    def on_connect(*args, **kwargs):
        logger.info("Connected to broker")

    def on_disconnect(*args, **kwargs):
        logger.info("Disconnected from broker")

    def on_publish(*args, **kwargs):
        logger.info("Publish message")

    client = Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    client.enable_logger(logger)
    client.username_pw_set(username, password)
    client.connect(host)
    return client


def tear_down_client(client: Client):
    client.loop_write()
    client.disconnect()


def send_message(client: Client, topic: str, value: str):
    client.publish(topic, json.dumps(value))
    client.loop_write()
    client.disconnect()
