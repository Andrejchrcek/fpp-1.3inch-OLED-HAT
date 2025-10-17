#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
import subprocess
import socket
import os
import requests
import json
from PIL import Image, ImageDraw, ImageFont
from gpiozero import Button, OutputDevice

# Import lokálnych knižníc
import SH1106
import INA219

# --- Názov pluginu (musí sa zhodovať s adresárom) ---
PLUGIN_NAME = "fpp-oled_remote"

# --- Automatické zapnutie displeja ---
try
    display_power_pin = OutputDevice(25)
    display_power_pin.on()
    print("GPIO 25 pre displej úspešne zapnutý.")
    time.sleep(0.1)
except Exception as e:
    print(f"CHYBA: Nepodarilo sa nastaviť GPIO 25: {e}")

# --- Hardvérové objekty a konfigurácia ---
FPP_API_URL = "http://localhost/api/"
LIST_REFRESH_INTERVAL = 3
DEFAULT_BRIGHTNESS = 100
CONFIG_FILE_PATH = f"/home/fpp/media/config/plugin.{PLUGIN_NAME}.json"

# --- Globálne premenné ---
sequence_list = []
selected_index = 0
current_mode = "LIST"
needs_redraw = True
last_fpp_status = {}
settings = {}  # Sem sa uložia nastavenia z JSON súboru

joy_up = Button(6, pull_up=True, bounce_time=0.1)
joy_down = Button(19, pull_up=True, bounce_time=0.1)
key_play = Button(21, pull_up=True, bounce_time=0.1)
key_stop = Button(20, pull_up=True, bounce_time=0.1)
key_shutdown = Button(16, pull_up=True, hold_time=3, bounce_time=0.1)

disp = SH1106.SH1106()
image = Image.new('1', (disp.width, disp.height), "BLACK")
draw = ImageDraw.Draw(image)

try:
    battery_monitor = INA219.INA219(addr=0x43)
    battery_available = True
except Exception:
    battery_available = False

try:
    font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)
    font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 12)
    font_xl = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
except IOError:
    font_small = ImageFont.load_default()
    font_large = ImageFont.load_default()
    font_xl = ImageFont.load_default()

# --- Funkcie ---
def load_settings():
    """Načíta nastavenia z config súboru FPP."""
    global settings
    defaults = {'enabled': True, 'showBattery': True}
    try:
        with open(CONFIG_FILE_PATH, 'r') as f:
            loaded_settings = json.load(f)
            settings = {**defaults, **loaded_settings}
    except (FileNotFoundError, json.JSONDecodeError):
        print("Config file not found or invalid. Using default settings.")
        settings = defaults

def run_api_command(command_path):
    try:
        url = f"{FPP_API_URL}{command_path}"
        requests.get(url, timeout=0.5)
        print(f"API Command '{url}' sent.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"API Command ERROR for '{url}': {e}")
        return False

def get_api_status(command_path):
    try:
        url = f"{FPP_API_URL}{command_path}"
        response = requests.get(url, timeout=1)
        response.raise_for_status()
        if 'application/json' in response.headers.get('Content-Type', ''):
            return response.json()
        return response.text.strip()
    except requests.exceptions.RequestException:
        return None

def get_sequences():
    global sequence_list
    path = '/home/fpp/media/sequences'
    try:
        if os.path.isdir(path):
            sequences = [f.replace('.fseq', '') for f in os.listdir(path) if f.endswith('.fseq')]
            sequence_list = sorted(sequences) if sequences else ["(No sequences found)"]
        else:
            sequence_list = ["(Directory not found)"]
    except Exception as e:
        sequence_list = [f"(Error: {e})"]

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(("8.8.8.8", 80)); ip = s.getsockname()[0]; s.close(); return ip
    except Exception: return "N/A"

def get_battery_status():
    if not battery_available: return -1
    try:
        percent = (battery_monitor.getBusVoltage_V() - 3.0) / 1.2 * 100
        return max(0, min(100, percent))
    except Exception: return -1

def format_time(seconds_str):
    try:
        seconds = int(float(seconds_str))
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"
    except (ValueError, TypeError): return "00:00"

def draw_message(message, delay=2):
    global needs_redraw
    draw.rectangle((0,0,disp.width,disp.height), 0, 0)
    lines = message.split('\n')
    y = (disp.height - (len(lines) * 14)) / 2
    for line in lines:
        w = draw.textlength(line, font=font_large)
        x = (disp.width - w) / 2
        draw.text((x, y), line, font=font_large, fill=1)
        y += 14
    disp.ShowImage(disp.getbuffer(image))
    time.sleep(delay)
    needs_redraw = True

def draw_ui():
    global needs_redraw
    if not needs_redraw: return
    draw.rectangle((0,0,disp.width,disp.height), 0, 0)

    if current_mode == "LIST":
        ip = get_ip_address()
        draw.text((2, 0), ip, font=font_small, fill=1)
        
        if settings.get('showBattery', True):
            batt = get_battery_status()
            batt_text = f"{int(batt)}%" if batt != -1 else "N/A"
            draw.text((disp.width - 38, 0), batt_text, font=font_small, fill=1)

        draw.line([(0, 12), (disp.width, 12)], fill=1, width=1)
        draw.text((92, 18), "PLAY", font=font_large, fill=1)
        draw.text((92, 33), "STOP", font=font_large, fill=1)
        draw.text((92, 48), "OFF", font=font_large, fill=1)
        draw.line([(88, 12), (88, disp.height)], fill=1, width=1)

        y_pos = 14
        start_index = 0
        if len(sequence_list) > 4 and selected_index >= 3:
            start_index = selected_index - 2
        for i, item in enumerate(sequence_list[start_index:start_index + 4]):
            index = i + start_index
            if index == selected_index:
                draw.rectangle((0, y_pos, 87, y_pos + 12), 1, 1)
                draw.text((2, y_pos), item[:12], font=font_small, fill=0)
            else:
                draw.text((2, y_pos), item[:12], font=font_small, fill=1)
            y_pos += 12

    elif current_mode == "PLAYING":
        seq_name = last_fpp_status.get('current_sequence', '').replace('.fseq', '')
        elapsed = format_time(last_fpp_status.get('seconds_elapsed', '0'))
        
        try:
            total_seconds = float(last_fpp_status.get('seconds_elapsed', 0)) + float(last_fpp_status.get('seconds_remaining', 0))
            total_formatted = format_time(total_seconds)
            progress = float(last_fpp_status.get('seconds_elapsed', 0)) / total_seconds if total_seconds > 0 else 0
        except (ValueError, TypeError):
            total_formatted = "??:??"
            progress = 0

        draw.text((2, 0), seq_name[:20], font=font_small, fill=1)
        draw.line([(0, 12), (disp.width, 12)], fill=1, width=1)
        
        time_text = f"{elapsed} / {total_formatted}"
        w = draw.textlength(time_text, font=font_xl)
        draw.text(((disp.width - w) / 2, 20), time_text, font=font_xl, fill=1)

        bar_y = 45
        bar_width = int(disp.width * progress)
        draw.rectangle((0, bar_y, disp.width - 1, bar_y + 10), outline=1, fill=0)
        if bar_width > 0:
            draw.rectangle((1, bar_y + 1, bar_width -1, bar_y + 9), outline=1, fill=1)
        draw.text((2, 55), "Press STOP to exit", font=font_small, fill=1)

    disp.ShowImage(disp.getbuffer(image))
    needs_redraw = False

# --- Handlery pre Tlačidlá ---
def handle_up():
    global selected_index, needs_redraw
    if current_mode == "LIST" and len(sequence_list) > 0:
        selected_index = (selected_index - 1 + len(sequence_list)) % len(sequence_list)
        needs_redraw = True

def handle_down():
    global selected_index, needs_redraw
    if current_mode == "LIST" and len(sequence_list) > 0:
        selected_index = (selected_index + 1) % len(sequence_list)
        needs_redraw = True

def handle_play():
    if current_mode != "LIST" or not sequence_list or selected_index >= len(sequence_list): return
    seq_to_play = sequence_list[selected_index]
    if "(No" in seq_to_play or "(Error" in seq_to_play: return
    run_api_command(f"command/Start%20Playlist/{seq_to_play}.fseq/1/false")

def handle_stop():
    run_api_command("command/Stop%20Now")

def handle_shutdown():
    draw_message("Shutting Down...", delay=3)
    run_api_command("command/Stop%20Gracefully")
    time.sleep(1)
    subprocess.run("/sbin/shutdown -h now", shell=True)

# --- Hlavná Slučka ---
def main():
    global current_mode, needs_redraw, last_fpp_status
    if os.geteuid() != 0:
        print("Warning: This script should ideally run with 'sudo' for full hardware access.")
    
    # Načítaj nastavenia pluginu hneď na začiatku
    load_settings()

    disp.Init()
    disp.set_contrast(DEFAULT_BRIGHTNESS)
    
    draw_message("Loading...")
    get_sequences()
    
    joy_up.when_pressed = handle_up
    joy_down.when_pressed = handle_down
    key_play.when_pressed = handle_play
    key_stop.when_pressed = handle_stop
    key_shutdown.when_held = handle_shutdown
    
    last_status_check = 0
    last_list_refresh = 0
    
    while True:
        if time.time() - last_status_check > 0.5:
            new_status = get_api_status("fppd/status")
            if new_status:
                last_fpp_status = new_status
                is_playing = last_fpp_status.get('status_name') == 'playing'
                
                if is_playing and current_mode != "PLAYING":
                    current_mode = "PLAYING"
                    needs_redraw = True
                elif not is_playing and current_mode == "PLAYING":
                    current_mode = "LIST"
                    needs_redraw = True
                
                if current_mode == "PLAYING":
                    needs_redraw = True
            last_status_check = time.time()

        if current_mode == "LIST" and time.time() - last_list_refresh > LIST_REFRESH_INTERVAL:
            get_sequences()
            needs_redraw = True
            last_list_refresh = time.time()

        draw_ui()
        time.sleep(0.05)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting script.")
        disp.clear()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        with open(f"/home/fpp/media/logs/{PLUGIN_NAME}.log", "a") as log_file:
            log_file.write(f"FATAL ERROR: {e}\n")
        disp.clear()
