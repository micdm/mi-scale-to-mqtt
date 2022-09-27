from decimal import Decimal
from typing import Optional

import environ
from dotenv import load_dotenv

from .config import Config
from .mqtt import setup_client, send_message, tear_down_client
from .scale import watch_for_scale


def on_measure(weight: Decimal):
    user_name = get_user_name(weight)
    if user_name is None:
        return
    client = setup_client(config.mqtt.host, config.mqtt.username, config.mqtt.password)
    send_message(client, f"{config.mqtt.topic_prefix}/{user_name}", str(weight))
    tear_down_client(client)


def get_user_name(weight: Decimal) -> Optional[str]:
    for i in range(1, 4):
        user = getattr(config, f"user{i}")
        print(user)
        if user is None:
            continue
        if user.min_weight <= weight and user.max_weight >= weight:
            return user.name
    return None


load_dotenv()
config = environ.to_config(Config)
watch_for_scale(config.scale_mac_address, on_measure)
