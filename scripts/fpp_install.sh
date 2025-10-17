#!/bin/bash
set -e

PLUGIN_NAME="fpp-oled_remote"
SCRIPT_NAME="oled_remote.py"
PLUGIN_DIR="/home/fpp/media/plugins/${PLUGIN_NAME}"
SCRIPTS_DIR="/home/fpp/media/scripts"
LOG_FILE="/home/fpp/media/logs/${PLUGIN_NAME}_install.log"

# --- Začiatok inštalácie ---
echo "=== ${PLUGIN_NAME} Installation Starting ===" > $LOG_FILE
echo "Started: $(date)" >> $LOG_FILE

# 1. Inštalácia systémových závislostí
echo "Installing system dependencies..." | tee -a $LOG_FILE
sudo apt-get update >> $LOG_FILE 2>&1
# Pridané 'dos2unix' pre opravu koncoviek riadkov
sudo apt-get install -y python3-pip python3-pil libjpeg-dev i2c-tools dos2unix >> $LOG_FILE 2>&1

echo "Installing Python packages..." | tee -a $LOG_FILE
pip3 install --break-system-packages requests Pillow gpiozero 2>&1 | tee -a $LOG_FILE

# 2. Príprava skriptov (oprava koncoviek riadkov)
echo "Fixing line endings for scripts..." | tee -a $LOG_FILE
# Toto je poistka proti chybe "command not found"
dos2unix "${PLUGIN_DIR}/helper.sh" >> $LOG_FILE 2>&1
dos2unix "${PLUGIN_DIR}/${SCRIPT_NAME}" >> $LOG_FILE 2>&1

# 3. Kopírovanie a nastavenie práv pre skripty
echo "Copying main script and setting permissions..." | tee -a $LOG_FILE
cp "${PLUGIN_DIR}/${SCRIPT_NAME}" "${SCRIPTS_DIR}/" >> $LOG_FILE 2>&1
# Príkaz chmod JE POTREBNÝ, aby bol skript spustiteľný
chmod +x "${SCRIPTS_DIR}/${SCRIPT_NAME}" >> $LOG_FILE 2>&1

echo "Making helper script executable..." | tee -a $LOG_FILE
# Príkaz chmod JE POTREBNÝ, aby bol skript spustiteľný
chmod +x "${PLUGIN_DIR}/helper.sh" >> $LOG_FILE 2>&1

# 4. Aplikácia počiatočných nastavení
echo "Applying initial settings..." | tee -a $LOG_FILE
sudo "${PLUGIN_DIR}/helper.sh" >> $LOG_FILE 2>&1

# --- Koniec inštalácie ---
echo "Installation complete!" | tee -a $LOG_FILE
echo "Please REBOOT FPP for changes to take effect." | tee -a $LOG_FILE
echo "Finished: $(date)" >> $LOG_FILE
