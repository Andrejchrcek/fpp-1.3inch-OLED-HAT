#!/bin/bash

PYTHON_SCRIPT="/home/fpp/media/plugins/fpp-oled_remote/oled_remote.py"
LOG_FILE="/home/fpp/media/logs/postStart.log"
CONFIG_FILE="/home/fpp/media/config/plugin.fpp-oled_remote.json"

echo "Kontrolujem auto_start (enabled): $(date)" >> "$LOG_FILE"

if [ -f "$CONFIG_FILE" ]; then
  ENABLED=$(jq -r '.enabled // "0"' "$CONFIG_FILE")
  if [ "$ENABLED" = "1" ]; then
    echo "Automatický štart povolený, spúšťam oled_remote.py" >> "$LOG_FILE"
    /usr/bin/python3 "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1 &
  else
    echo "Automatický štart vypnutý, preskakujem spustenie oled_remote.py" >> "$LOG_FILE"
  fi
else
  echo "Konfiguračný súbor neexistuje, spúšťam oled_remote.py (predvolené)" >> "$LOG_FILE"
  /usr/bin/python3 "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1 &
fi
