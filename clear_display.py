#!/usr/bin/python3
# -*- coding: utf-8 -*-
import SH1106

# Inicializuj a vyčisti displej
try:
    disp = SH1106.SH1106()
    disp.Init()
    disp.clear()
    print("OLED displej vyčistený.")
except Exception as e:
    print(f"Chyba pri čistení displeja: {e}")
