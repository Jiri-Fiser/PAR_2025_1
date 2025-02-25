import multiprocessing
import sys
from multiprocessing.managers import BaseManager
import socket
import os
import time
from zeta import zeta_slow

from config import load_ini_to_dict

d = load_ini_to_dict("network.ini")
print(d, file=sys.stderr)

class QueueManager(BaseManager):
    pass

# Registrace metod pro získání obou front
QueueManager.register('get_command_queue')
QueueManager.register('get_result_queue')

# Připojení k manageru (upravte IP adresu, pokud spouštíte na jiném stroji)
manager = QueueManager(address=(d["ip"], d["port"]), authkey=d["password"].encode())
manager.connect()

command_queue = manager.get_command_queue()
result_queue = manager.get_result_queue()

def worker_func():
    # Získání IP adresy počítače a PID aktuálního procesu
    ip_addr = socket.gethostbyname(socket.gethostname())
    pid = os.getpid()
    while True:
        try:
            # Čtení čísla z příkazové fronty s timeoutem, aby se worker nezablokoval věčně
            x = command_queue.get(timeout=5)
        except Exception:
            break  # Pokud fronta není aktivní, ukončíme smyčku
        y = zeta_slow(x, iterations=1_000)
        # Vložení výsledku do fronty: (vstup, výsledek, (ip, pid))
        result_queue.put((x, y, (ip_addr, pid)))

if __name__ == '__main__':
    # Počet workerů odpovídá počtu HW vláken
    num_workers = multiprocessing.cpu_count()
    processes = []
    for _ in range(num_workers):
        p = multiprocessing.Process(target=worker_func)
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
