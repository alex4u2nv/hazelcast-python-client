import threading
import random
import time
import logging
import sys

from os.path import dirname

sys.path.append(dirname(dirname(dirname(__file__))))

import hazelcast

THREAD_COUNT = 1
ENTRY_COUNT = 10 * 1000
VALUE_SIZE = 10000
GET_PERCENTAGE = 40
PUT_PERCENTAGE = 40

logging.basicConfig(format='%(asctime)s%(msecs)03d [%(name)s] %(levelname)s: %(message)s', datefmt="%H:%M%:%S,")
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger("main")

config = hazelcast.ClientConfig()
config.group_config.name = "dev"
config.group_config.password = "dev-pass"
config.network_config.addresses.append("127.0.0.1:5701")
client = hazelcast.HazelcastClient(config)
my_map = client.get_map("default")
for i in xrange(0, 1000):
    key = int(random.random() * ENTRY_COUNT)
    operation = int(random.random() * 100)
    if operation < GET_PERCENTAGE:
        my_map.get(key)
    elif operation < GET_PERCENTAGE + PUT_PERCENTAGE:
        my_map.put(key, "x" * VALUE_SIZE)
    else:
        my_map.remove(key)
