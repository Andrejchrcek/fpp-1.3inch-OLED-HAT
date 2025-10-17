#!/bin/bash

CONFIG_FILE="/home/fpp/media/config/plugin.fpp-oled_remote.json"

# Skontroluj, či jq je dostupné (štandard v FPP)
if ! command -v jq &> /dev/null; then
  echo "jq not found, cannot parse config."
  exit 1
fi

ENABLED=$(jq -r '.enabled // "0"' "$CONFIG_FILE")

# Nájdi PID Python skriptu
PID=$(pgrep -f "python3 /home/fpp/media/plugins/fpp-oled_remote/oled_remote.py")

if [ "$ENABLED" = "1" ]; then
  # Ak už beží, zabi a reštartuj
  if [ -n "$PID" ]; then
    kill "$PID"
    sleep 1
  fi
  /usr/bin/python3 /home/fpp/media/plugins/fpp-oled_remote/oled_remote.py &
  echo "OLED Remote script started."
else
  # Ak beží, zabi
  if [ -n "$PID" ]; then
    kill "$PID"
    echo "OLED Remote script stopped."
  fi
fi
