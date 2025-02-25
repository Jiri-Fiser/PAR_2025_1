import multiprocessing
import os

from zeta import zeta_slow

def worker(command_queue, result_queue):
    """Pracovník: načítá příkazy z command_queue, zpracovává je a výsledek posílá do result_queue."""
    idf = os.getpid()
    while True:
        cmd = command_queue.get()
        if cmd is None:  # Signál pro ukončení
            break
        # Příklad zpracování: zdvojnásobení hodnoty
        result = zeta_slow(cmd, iterations=1_000)
        result_queue.put((cmd, result, idf))

def result_listener(result_queue):
    """Proces pro čtení výsledků z result_queue a jejich výpis na stdout."""
    while True:
        res = result_queue.get()
        if res is None:  # Signál pro ukončení
            break
        print("Výsledek:", res)

if __name__ == '__main__':
    # Vytvoříme fronty pro příkazy a výsledky
    command_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    # Spustíme proces, který poslouží jako výpis výsledků
    listener = multiprocessing.Process(target=result_listener, args=(result_queue,))
    listener.start()

    # Nastavíme počet workerů na počet hardwarových vláken
    num_workers = multiprocessing.cpu_count()
    print("Numer workers:", num_workers)
    workers = []
    for _ in range(num_workers):
        p = multiprocessing.Process(target=worker, args=(command_queue, result_queue))
        p.start()
        workers.append(p)

    # Vložíme příkazy do command_queue (např. čísla 0 až 9)
    for i in range(1, 10):
        command_queue.put(float(i))

    # Pošleme signál ukončení workerům
    for _ in range(num_workers):
        command_queue.put(None)

    # Počkáme na dokončení všech workerů
    for p in workers:
        p.join()

    # Pošleme signál ukončení listeneru
    result_queue.put(None)
    listener.join()
