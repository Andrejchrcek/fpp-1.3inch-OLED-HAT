#!/bin/bash

# Názov pluginu a skriptov
PLUGIN_NAME="fpp-oled_remote"
PYTHON_SCRIPT="oled_remote.py"

# Cesty
PLUGIN_DIR="/home/fpp/media/plugins/${PLUGIN_NAME}"
CONFIG_FILE="${PLUGIN_DIR}/config.json"
FPP_API_URL="http://localhost/api"

# Zisti, či je plugin povolený v konfiguračnom súbore
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Creating default config file..."
    echo '{"enabled": false, "showBattery": true}' > "$CONFIG_FILE"
fi

ENABLED=$(jq -r '.enabled' "$CONFIG_FILE")

if [ "$ENABLED" == "true" ]; then
    echo "Enabling OLED-Remote startup script via API..."
    # Použijeme API na nastavenie štartovacieho skriptu.
    # Hodnotu posielame v úvodzovkách, lebo API očakáva JSON string.
    curl -s -X POST -d "\"${PYTHON_SCRIPT}\"" "${FPP_API_URL}/setting/FPPStartScript"
else
    echo "Disabling OLED-Remote startup script via API..."
    # Najprv zistíme, či je náš skript aktuálne nastavený
    CURRENT_START_SCRIPT=$(curl -s "${FPP_API_URL}/setting/FPPStartScript")
    
    # Porovnáme ho s názvom nášho skriptu (vrátane úvodzoviek, ktoré vracia API)
    if [ "$CURRENT_START_SCRIPT" == "\"${PYTHON_SCRIPT}\"" ]; then
        # Ak áno, nastavíme prázdnu hodnotu, čím ho vymažeme
        curl -s -X POST -d '""' "${FPP_API_URL}/setting/FPPStartScript"
    else
        echo "Startup script is not set to our script, doing nothing."
    fi
fi

echo "Helper script finished."
