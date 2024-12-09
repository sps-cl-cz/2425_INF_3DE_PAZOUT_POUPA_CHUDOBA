import argparse
import hashlib
import os
import json
from datetime import datetime

# Funkce pro výpočet SHA-1 hashe
def vypocti_sha1(soubor_cesta):
    sha1_hash = hashlib.sha1()
    with open(soubor_cesta, "rb") as f:
        for bajtovy_blok in iter(lambda: f.read(4096), b""):
            sha1_hash.update(bajtovy_blok)
    return sha1_hash.hexdigest()

# Inicializace sledování
def init():
    # Vytvoření prázdného souboru .check
    with open('.check', 'w') as f:
        json.dump({}, f)

# Přidání souboru ke sledování
def add(pathspec):
    # Načtení existujícího obsahu .check
    if os.path.exists('.check'):
        with open('.check', 'r') as f:
            data = json.load(f)
    else:
        data = {}

    # Vypočítání SHA-1 hashe souboru
    hash_souboru = vypocti_sha1(pathspec)
    # Přidání informací do dat
    data[pathspec] = {
        'hash': hash_souboru,
        'timestamp': datetime.now().isoformat()
    }

    # Uložení aktualizovaných dat do .check
    with open('.check', 'w') as f:
        json.dump(data, f)

# Odebrání souboru ze sledování
def remove(pathspec):
    if os.path.exists('.check'):
        with open('.check', 'r') as f:
            data = json.load(f)

        # Odebrání souboru, pokud existuje
        if pathspec in data:
            del data[pathspec]

        # Uložení aktualizovaných dat do .check
        with open('.check', 'w') as f:
            json.dump(data, f)

# Zobrazení stavu sledovaných souborů
def status():
    if os.path.exists('.check'):
        with open('.check', 'r') as f:
            data = json.load(f)

        for pathspec, info in data.items():
            if os.path.exists(pathspec):
                current_hash = vypocti_sha1(pathspec)
                if current_hash == info['hash']:
                    print(f"[OK] {current_hash} {pathspec}")
                else:
                    print(f"[CHANGE] {info['hash']} {pathspec}")
                    print(f"NEW HASH: {current_hash}")
            else:
                print(f"[ERROR] Soubor nebyl nalezen: {pathspec}")

        # Shrnutí stavu
        # ... (můžete přidat kód pro shrnutí počtu souborů podle stavu)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sledování změn v souborech pomocí kontrolních součtů.')
    parser.add_argument('command', choices=['init', 'add', 'remove', 'status'], help='Příkaz pro provedení')
    parser.add_argument('pathspec', nargs='?', help='Cesta k souboru')
    args = parser.parse_args()

    if args.command == 'init':
        init()
    elif args.command == 'add':
        if args.pathspec:
            add(args.pathspec)
    elif args.command == 'remove':
        if args.pathspec:
            remove(args.pathspec)
    elif args.command == 'status':
        status()
