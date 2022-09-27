from decimal import Decimal

import environ


@environ.config(prefix="")
class Config:

    @environ.config(prefix="MQTT")
    class Mqtt:
        host = environ.var()
        username = environ.var()
        password = environ.var()
        topic_prefix = environ.var()

    @environ.config(prefix="USER1")
    class User1:
        min_weight = environ.var(converter=Decimal)
        max_weight = environ.var(converter=Decimal)
        name = environ.var()

    @environ.config(prefix="USER2")
    class User2:
        min_weight = environ.var(converter=Decimal)
        max_weight = environ.var(converter=Decimal)
        name = environ.var()

    @environ.config(prefix="USER3")
    class User3:
        min_weight = environ.var(converter=Decimal)
        max_weight = environ.var(converter=Decimal)
        name = environ.var()

    scale_mac_address = environ.var()
    mqtt = environ.group(Mqtt)
    user1 = environ.group(User1)
    user2 = environ.group(User2, optional=True)
    user3 = environ.group(User3, optional=True)
