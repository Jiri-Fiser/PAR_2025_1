import sys
from multiprocessing.managers import BaseManager
from queue import Queue
from config import load_ini_to_dict

d = load_ini_to_dict("network.ini")

# Vytvoření front pro příkazy a výsledky
command_queue = Queue()
result_queue = Queue()

class QueueManager(BaseManager):
    pass

# Registrace metod, které vrací naše fronty
QueueManager.register('get_command_queue', callable=lambda: command_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)

# Nastavení adresy a autentizačního klíče (můžete upravit dle potřeby)
manager = QueueManager(address=('', d["port"]), authkey=d["password"].encode())
print("Server běží na portu 50000...")
server = manager.get_server()
server.serve_forever()
