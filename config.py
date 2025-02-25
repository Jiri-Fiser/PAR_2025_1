import configparser


def load_ini_to_dict(file_path):
    # Načtení obsahu souboru
    with open(file_path, 'r') as f:
        content = f.read()
    # Pokud soubor nezačíná sekcí, přidáme [DEFAULT]
    if not content.strip().startswith('['):
        content = '[DEFAULT]\n' + content
    # Načtení konfigurace
    config = configparser.ConfigParser()
    config.read_string(content)
    data = dict(config['DEFAULT'])
    # Převod portu na číslo, pokud je potřeba
    if 'port' in data:
        data['port'] = int(data['port'])
    return data