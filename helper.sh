#!/bin/bash

# Názov pluginu a skriptov
PLUGIN_NAME="OLED-Remote"
PYTHON_SCRIPT="oled_remote.py"

# Cesty
PLUGIN_DIR="/home/fpp/media/plugins/${PLUGIN_NAME}"
CONFIG_FILE="${PLUGIN_DIR}/config.json"
FPP_COMMAND="/opt/fpp/bin/fpp"

# Zisti, či je plugin povolený v konfiguračnom súbore
# Používame `jq` na čítanie JSON. FPP ho má predinštalovaný.
ENABLED=$(jq -r '.enabled' "$CONFIG_FILE")

if [ "$ENABLED" == "true" ]; then
    echo "Enabling OLED-Remote startup script..."
    # Pridá tvoj skript do FPP Start Script
    $FPP_COMMAND -S FPPStartScript "${PYTHON_SCRIPT}"
else
    echo "Disabling OLED-Remote startup script..."
    # Odstráni tvoj skript z FPP Start Script
    # Porovná, či je náš skript aktuálne nastavený, a ak áno, vymaže ho.
    CURRENT_START_SCRIPT=$($FPP_COMMAND -g FPPStartScript)
    if [ "$CURRENT_START_SCRIPT" == "\"${PYTHON_SCRIPT}\"" ]; then
        $FPP_COMMAND -S FPPStartScript ""
    fi
fi

echo "Helper script finished."
