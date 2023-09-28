#!/bin/bash

# Przenoszenie plików i katalogów

# Przenoszenie logów do katalogu logs
mv server.log logs/
mv mail_api/server.log logs/mail_api.log
mv telegram_api/server.log logs/telegram_api.log
mv wp_api/server.log logs/wp_api.log

# Usuwanie pustego katalogu models
rm -rf models

# Tworzenie katalogów, jeśli jeszcze nie istnieją
mkdir -p config docs scripts utils

# Informacja dla użytkownika
echo "Restructuring completed. Please review the changes and adjust as necessary."

