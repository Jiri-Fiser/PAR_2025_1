import sys
from multiprocessing.managers import BaseManager

from config import load_ini_to_dict


class QueueManager(BaseManager):
    pass

d = load_ini_to_dict("network.ini")
print(d, file=sys.stderr)

# Registrace metody pro získání fronty výsledků
QueueManager.register('get_result_queue')

# Připojení k manageru
manager = QueueManager(address=(d["ip"], d["port"]), authkey=d["password"].encode())
manager.connect()

result_queue = manager.get_result_queue()

print("Čekám na výsledky...")
while True:
    result = result_queue.get()
    print("Výsledek:", result)
