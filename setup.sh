#!/bin/bash

# Skrypt do dodawania plików __init__.py w katalogach projektu

# Lista katalogów, w których chcesz dodać plik __init__.py
DIRECTORIES=(
    "."
    "./database"
    "./database/graphql"
    "./database/models"
    "./mail_api"
    "./telegram_api"
    "./wp_api"
    # Dodaj więcej katalogów w razie potrzeby
)

# Pętla dodająca plik __init__.py w każdym katalogu z listy
for dir in "${DIRECTORIES[@]}"; do
    touch "$dir/__init__.py"
    echo "Dodano plik __init__.py w katalogu $dir"
done

echo "Operacja zakończona pomyślnie!"
