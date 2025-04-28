# EUC Lights

Sistema di luci posteriori indossabile per monoruota elettrico (EUC), per sicurezza notturna in ambito urbano.

## Funzionalità
- Luci di posizione (rosso, 30%-100% con luminosità adattiva).
- Frecce direzionali (giallo, lampeggiante, con buzzer opzionale).
- Luci di stop (rosso, 100%) su decelerazione (dati EUC o MPU6050).
- Connessione BLE a monoruota (es. InMotion V10F, Veteran Sherman Max) con libreria EUC.
- Configurazione via Wi-Fi: Scansione BLE, selezione dispositivo, impostazione password, toggle IMU/buzzer/luminosità.
- Salvataggio MAC address per riconnessione automatica.

## Hardware
- ESP32-C3 Super Mini (BLE 5.0, Wi-Fi).
- Striscia LED WS2812B (10 LED).
- Powerbank (10.000 mAh, ≥20W, 2+ porte USB).
- Commutatore a 3 vie (sinistra/off/destra).
- Interruttore on/off.
- Pulsante per connessione iniziale.
- LED feedback.
- Buzzer (feedback frecce).
- MPU6050 (rilevazione frenate opzionale).
- BH1750 (luminosità adattiva).

## Schema Elettrico

Powerbank (5V, ≥3A)
├── USB-C → ESP32-C3 Super Mini (5V, GND)
├── 5V, GND → Striscia LED WS2812B (10 LED)
│   └── Dati → GPIO 8
├── Commutatore 3 vie → GPIO 9 (sinistra), GPIO 10 (destra)
├── Pulsante connessione → GPIO 7 (pull-up)
├── LED feedback → GPIO 6
├── Buzzer → GPIO 11
├── MPU6050 → SCL: GPIO 5, SDA: GPIO 4, VCC: 3.3V, GND
└── BH1750 → SCL: GPIO 5, SDA: GPIO 4, VCC: 3.3V, GND
