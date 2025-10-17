#!/bin/bash
set -e

PLUGIN_NAME="fpp-oled_remote"
PLUGIN_DIR="/home/fpp/media/plugins/${PLUGIN_NAME}"
LOG_FILE="/home/fpp/media/logs/${PLUGIN_NAME}_install.log"

echo "=== ${PLUGIN_NAME} Installation Starting ===" > $LOG_FILE
echo "Started: $(date)" >> $LOG_FILE

# 1. Inštalácia závislostí
echo "Installing dependencies..." | tee -a $LOG_FILE
sudo apt-get update >> $LOG_FILE 2>&1
sudo apt-get install -y python3-pip python3-pil libjpeg-dev i2c-tools dos2unix >> $LOG_... 2>&1
pip3 install --break-system-packages requests Pillow gpiozero 2>&1 | tee -a $LOG_FILE

# 2. Príprava skriptu (KĽÚČOVÁ ČASŤ)
echo "Preparing main script..." | tee -a $LOG_FILE
# Opraví konce riadkov pre istotu
dos2unix "${PLUGIN_DIR}/oled_remote.py" >> $LOG_FILE 2>&1
# Nastaví povolenie na spustenie priamo na súbore v adresári pluginu
chmod +x "${PLUGIN_DIR}/oled_remote.py" >> $LOG_FILE 2>&1

echo "Installation complete!" | tee -a $LOG_FILE
echo "A REBOOT is required to start the plugin." | tee -a $LOG_FILE
echo "Finished: $(date)" >> $LOG_FILE
