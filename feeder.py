import sys
import time
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
    pass

from config import load_ini_to_dict

d = load_ini_to_dict("network.ini")
print(d, file=sys.stderr)

# Registrace metody pro získání příkazové fronty
QueueManager.register('get_command_queue')

# Připojení k manageru (upravte IP adresu, pokud spouštíte na jiném stroji)
manager = QueueManager(address=(d["ip"], d["port"]), authkey=d["password"].encode())
manager.connect()

command_queue = manager.get_command_queue()

# Poslání čísel od 1.0 do 9.0 do fronty
for i in range(2, 100):
    x = float(i)/10
    command_queue.put(x)
    print(f"Vloženo do příkazové fronty: {x}")
print("Feeder finished")
