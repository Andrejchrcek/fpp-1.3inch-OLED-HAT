#!/bin/bash

# Názov pluginu a skriptov
PLUGIN_NAME="fpp-oled_remote"
PYTHON_SCRIPT="oled_remote.py"

# Cesty
PLUGIN_DIR="/home/fpp/media/plugins/${PLUGIN_NAME}"
CONFIG_FILE="${PLUGIN_DIR}/config.json"
# Adresa pre API zostáva rovnaká
FPP_API_URL="http://localhost/api/settings"

# Zisti, či je plugin povolený v konfiguračnom súbore
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Creating default config file..."
    echo '{"enabled": false, "showBattery": true}' > "$CONFIG_FILE"
fi

ENABLED=$(jq -r '.enabled' "$CONFIG_FILE")

if [ "$ENABLED" == "true" ]; then
    echo "Enabling OLED-Remote startup script via API..."
    # --- TOTO JE KĽÚČOVÁ OPRAVA ---
    # Posielame POST na všeobecnú adresu /api/settings
    # a v dátach (-d) špecifikujeme, čo meníme
    curl -s -X POST -H "Content-Type: application/json" \
         -d '{"FPPStartScript": "'"${PYTHON_SCRIPT}"'"}' \
         "${FPP_API_URL}"
else
    echo "Disabling OLED-Remote startup script via API..."
    # Najprv zistíme, či je náš skript aktuálne nastavený (GET zostáva rovnaký)
    CURRENT_START_SCRIPT=$(curl -s "${FPP_API_URL}/FPPStartScript")
    
    if [ "$CURRENT_START_SCRIPT" == "\"${PYTHON_SCRIPT}\"" ]; then
        # --- AJ TU JE OPRAVA ---
        # Posielame POST na všeobecnú adresu s prázdnou hodnotou
        curl -s -X POST -H "Content-Type: application/json" \
             -d '{"FPPStartScript": ""}' \
             "${FPP_API_URL}"
    else
        echo "Startup script is not set to our script, doing nothing."
    fi
fi

echo "Helper script finished."
