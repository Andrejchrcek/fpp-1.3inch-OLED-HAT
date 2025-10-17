#!/bin/bash

# Názov pluginu a skriptov
PLUGIN_NAME="fpp-oled_remote"
PYTHON_SCRIPT="oled_remote.py"

# Cesty
PLUGIN_DIR="/home/fpp/media/plugins/${PLUGIN_NAME}"
CONFIG_FILE="${PLUGIN_DIR}/config.json"
# TOTO JE OPRAVENÁ CESTA
FPP_COMMAND="/opt/fpp/bin.pi/fpp" 

# Zisti, či je plugin povolený v konfiguračnom súbore
if [ ! -f "$CONFIG_FILE" ]; then
    # Ak config súbor neexistuje, vytvoríme ho s predvolenými hodnotami
    echo "Creating default config file..."
    echo '{"enabled": false, "showBattery": true}' > "$CONFIG_FILE"
fi

ENABLED=$(jq -r '.enabled' "$CONFIG_FILE")

if [ "$ENABLED" == "true" ]; then
    echo "Enabling OLED-Remote startup script..."
    # Pridá tvoj skript do FPP Start Script
    $FPP_COMMAND -S FPPStartScript "${PYTHON_SCRIPT}"
else
    echo "Disabling OLED-Remote startup script..."
    # Odstráni tvoj skript z FPP Start Script
    CURRENT_START_SCRIPT=$($FPP_COMMAND -g FPPStartScript)
    if [ "$CURRENT_START_SCRIPT" == "\"${PYTHON_SCRIPT}\"" ]; then
        $FPP_COMMAND -S FPPStartScript ""
    fi
fi

echo "Helper script finished."
