#!/bin/bash
set -e  # Zastav skript pri akejkoľvek chybe

# Log súbor pre inštaláciu
LOG_FILE="/home/fpp/media/logs/oled_remote_install.log"
echo "=== FPP OLED Remote Plugin Installation ===" > $LOG_FILE
echo "Started: $(date)" >> $LOG_FILE

# Inštalácia systémových závislostí pre Pillow, GPIO a I2C
echo "Installing system dependencies..." | tee -a $LOG_FILE
sudo apt-get update >> $LOG_FILE 2>&1
sudo apt-get install -y python3-pip python3-pil libjpeg-dev i2c-tools >> $LOG_FILE 2>&1

# Inštalácia potrebných Python balíčkov
echo "Installing Python packages..." | tee -a $LOG_FILE
pip3 install --break-system-packages requests Pillow gpiozero 2>&1 | tee -a $LOG_FILE

echo "Installation complete!" | tee -a $LOG_FILE
echo "Finished: $(date)" >> $LOG_FILE
