#!/bin/bash

CONFIG_FILE="/home/fpp/media/config/plugin.fpp-oled_remote.json"
LOG_FILE="/home/fpp/media/logs/fpp-oled_remote.log"
CLEAR_SCRIPT="/home/fpp/media/plugins/fpp-oled_remote/clear_display.py"

# Skontroluj, či jq je dostupné
if ! command -v jq &> /dev/null; then
  echo "jq not found, cannot parse config." >> "$LOG_FILE"
  exit 1
fi

ENABLED=$(jq -r '.enabled // "0"' "$CONFIG_FILE")
SHOW_BATTERY=$(jq -r '.showBattery // "1"' "$CONFIG_FILE")

echo "Helper.sh: enabled=$ENABLED, showBattery=$SHOW_BATTERY" >> "$LOG_FILE"

# Nájdi PID Python skriptu
PID=$(pgrep -f "python3 /home/fpp/media/plugins/fpp-oled_remote/oled_remote.py")

if [ "$ENABLED" = "1" ]; then
  # Ak už beží, zabi a reštartuj (aby sa aplikovali nové nastavenia)
  if [ -n "$PID" ]; then
    kill "$PID"
    sleep 1
  fi
  /usr/bin/python3 /home/fpp/media/plugins/fpp-oled_remote/oled_remote.py >> "$LOG_FILE" 2>&1 &
  echo "OLED Remote script started." >> "$LOG_FILE"
else
  # Ak beží, zabi a vyčisti displej
  if [ -n "$PID" ]; then
    kill "$PID"
    sleep 1
    echo "OLED Remote script stopped, čistím displej." >> "$LOG_FILE"
    /usr/bin/python3 "$CLEAR_SCRIPT" >> "$LOG_FILE" 2>&1
  fi
fi
