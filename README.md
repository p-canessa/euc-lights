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


## Installazione
1. Clona il repository: `git clone https://github.com/your-username/euc-lights`.
2. Carica MicroPython v1.23 su ESP32-C3 (`esptool.py`).
3. Copia file su ESP32 con Thonny o rshell.
4. Installa Microdot:
   - `pip install microdot` su PC.
   - Copia `microdot.py` da `site-packages/microdot.py`.
5. Scarica librerie:
   - EUC: [p-canessa/EUC](https://github.com/p-canessa/EUC).
   - MPU6050: [micropython-mpu6050](https://github.com/micropython-IMU/micropython-mpu6050).
   - BH1750: [micropython-bh1750](https://github.com/PeterDHabermehl/micropython-bh1750).
6. Copia `mpu6050.py`, `bh1750.py`, `microdot.py`, e `wheellog_euc_micropython` su ESP32.

## Utilizzo
1. Accendi il sistema (interruttore on/off).
2. Connetti via pulsante (premuta lunga 5s) o Wi-Fi:
   - Connetti a SSID "EUC-Lights" (password: "12345678").
   - Apri `http://192.168.4.1` su browser.
   - Scansiona, seleziona dispositivo (es. V10F con password "000000", Sherman Max senza password).
   - Configura IMU (opzionale), buzzer (attivo), luminosità (attiva).
3. Usa commutatore per frecce, luci di stop si attivano automaticamente su decelerazione.

## Test
- **Connessione BLE**: Verifica con V10F (password "000000") e Sherman Max (no password).
- **Luci**:
  - Posizione: Rosso 30%-100% (con BH1750).
  - Frecce: Giallo lampeggiante con beep (se buzzer attivo).
  - Stop: Rosso 100% su decelerazione (dati EUC o MPU6050).
- **MPU6050**: Calibra (busto eretto, 3s), testa frenate graduali/emergenza.
- **BH1750**: Verifica luminosità in notte (<50 lux), crepuscolo (50-200 lux), giorno (>200 lux).
- **Wi-Fi**: Connetti a "EUC-Lights", configura via `http://192.168.4.1`.

## Note
- La funzione `_send_password` in `euc.py` è un placeholder. Testa con V10F per implementare il comando password corretto.
- Calibra soglie decelerazione (`delta_v < -0.5`, `current < -0.1`) e MPU6050 (`pitch < -5`) con EUC reale.
- Disattiva Wi-Fi dopo configurazione per ridurre consumi (~50 mA).

## Licenza
MIT
