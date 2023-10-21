import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config'))

import re
import logging

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_and_block_ips(log_file_path='2023-09-28.log', block_file_path="block.txt"):
    # Tworzenie regex do rozpoznawania linii logowania i wyodrębniania adresu IP
    failed_login_patterns = [
        re.compile(r"failed\. Error Code=incorrect password"),
        re.compile(r"rejected: too many failed logins")
    ]
    ip_pattern = re.compile(r"from \[(?P<ip>[\d\.]+)\]")

    # Zbieranie unikatowych adresów IP
    ips_to_block = set()

    try:
        # Otwieranie i analiza pliku logów
        logging.info(f"Opening log file: {log_file_path}")  # Logowanie informacji
        with open(log_file_path, "r") as log_file:
            for line in log_file:
                if any(pattern.search(line) for pattern in failed_login_patterns):
                    # Wyciąganie adresu IP
                    match = ip_pattern.search(line)
                    if match:
                        ip = match.group("ip")
                        logging.info(f"IP address found: {ip}")  # Logowanie informacji
                        ips_to_block.add(ip)
    except FileNotFoundError:
        logging.error(f"File {log_file_path} not found.")  # Logowanie błędu
        return

    # Zapisywanie adresów IP do blokowania do pliku
    logging.info(f"Writing IP addresses to block file: {block_file_path}")  # Logowanie informacji
    with open(block_file_path, "w") as block_file:
        for ip in ips_to_block:
            block_file.write(ip + "\n")

# Użycie funkcji
extract_and_block_ips()
