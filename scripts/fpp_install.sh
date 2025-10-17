#!/bin/bash
set -e  # Zastav skript pri akejkoľvek chybe

# Premenné pre ľahšiu úpravu
PLUGIN_NAME="OLED-Remote" # Dôležité: Tento názov musí sedieť s názvom adresára pluginu!
SCRIPT_NAME="oled_remote.py"
PLUGIN_DIR="/home/fpp/media/plugins/${PLUGIN_NAME}"
SCRIPTS_DIR="/home/fpp/media/scripts"
LOG_FILE="/home/fpp/media/logs/${PLUGIN_NAME}_install.log"

# --- Začiatok inštalácie ---
echo "=== ${PLUGIN_NAME} Installation Starting ===" > $LOG_FILE
echo "Started: $(date)" >> $LOG_FILE

# 1. Inštalácia systémových a Python závislostí
echo "Installing system dependencies..." | tee -a $LOG_FILE
sudo apt-get update >> $LOG_FILE 2>&1
sudo apt-get install -y python3-pip python3-pil libjpeg-dev i2c-tools >> $LOG_FILE 2>&1

echo "Installing Python packages..." | tee -a $LOG_FILE
pip3 install --break-system-packages requests Pillow gpiozero 2>&1 | tee -a $LOG_FILE

# 2. Kopírovanie a nastavenie práv pre hlavný skript
echo "Copying ${SCRIPT_NAME} to scripts directory..." | tee -a $LOG_FILE
cp "${PLUGIN_DIR}/${SCRIPT_NAME}" "${SCRIPTS_DIR}/" >> $LOG_FILE 2>&1
chmod +x "${SCRIPTS_DIR}/${SCRIPT_NAME}" >> $LOG_FILE 2>&1

# 3. Príprava pomocných skriptov (TOTO JE DÔLEŽITÁ NOVÁ ČASŤ)
echo "Making helper script executable..." | tee -a $LOG_FILE
chmod +x "${PLUGIN_DIR}/helper.sh" >> $LOG_FILE 2>&1

# 4. Automatická registrácia skriptu ako FPP Start Script (ak je povolený)
echo "Setting up startup script based on config..." | tee -a $LOG_FILE
# Spustíme helper hneď po inštalácii, aby sa systém nastavil podľa defaultných hodnôt
sudo "${PLUGIN_DIR}/helper.sh" >> $LOG_FILE 2>&1

# --- Koniec inštalácie ---
echo "Installation complete!" | tee -a $LOG_FILE
echo "Please REBOOT FPP for changes to take effect." | tee -a $LOG_FILE
echo "Finished: $(date)" >> $LOG_FILE
