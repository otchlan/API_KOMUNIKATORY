#!/bin/bash

# Utwórz folder flask_app
mkdir -p flask_app/templates

# Przenieś app.py do folderu flask_app
mv app.py flask_app/

# Przenieś index.html do folderu flask_app/templates
mv database/db_flask_test_app/templates/index.html flask_app/templates/

# Usuń niepotrzebny folder db_flask_test_app
rm -r database/db_flask_test_app/

echo "Struktura projektu została zmieniona."
