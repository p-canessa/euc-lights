from machine import Pin
from neopixel import NeoPixel
import utime
import esp32
from euc import EucInterface
from lights import update_lights
from config import save_config, load_config
from web import start_web_server
from mpu6050 import MPU6050
from bh1750 import BH1750

# Configurazione hardware
np = NeoPixel(Pin(8), 10)  # 10 LED su GPIO 8
left_pin = Pin(9, Pin.IN, Pin.PULL_UP)  # Commutatore sinistra
right_pin = Pin(10, Pin.IN, Pin.PULL_UP)  # Commutatore destra
connect_pin = Pin(7, Pin.IN, Pin.PULL_UP)  # Pulsante connessione
feedback_led = Pin(6, Pin.OUT)  # LED feedback
buzzer = Pin(11, Pin.OUT)  # Buzzer
mpu = MPU6050()  # MPU6050 su I2C (GPIO 4, 5)
bh1750 = BH1750()  # BH1750 su I2C (GPIO 4, 5)

# Stato
euc = None
v_previous = 0
stop_active = False
press_start = 0
connected = False
neutral_pitch = 0

# Configurazioni
def load_settings():
    return {
        "use_imu": esp32.nvs_get_str("use_imu") == "True",
        "use_buzzer": esp32.nvs_get_str("use_buzzer") != "False",
        "use_brightness": esp32.nvs_get_str("use_brightness") != "False"
    }

settings = load_settings()

# Funzioni helper
def calibrate_mpu():
    pitch_sum, count = 0, 0
    for _ in range(100):
        data = mpu.get_data()
        pitch_sum += data["pitch"]
        count += 1
        utime.sleep_ms(20)
    return pitch_sum / count

def read_turn_state():
    if not left_pin.value():
        return "left"
    if not right_pin.value():
        return "right"
    return "off"

def check_connect_press():
    global press_start
    if not connect_pin.value():
        if press_start == 0:
            press_start = utime.ticks_ms()
        elif utime.ticks_ms() - press_start > 5000:
            press_start = 0
            return True
    else:
        press_start = 0
    return False

def check_deceleration(data):
    global v_previous
    v_current = data.get("speed", 0)
    current = data.get("current", 0)
    delta_v = v_current - v_previous
    v_previous = v_current
    return delta_v < -0.5 and current < -0.1

def check_braking(mpu_data):
    pitch = mpu_data["pitch"] - neutral_pitch
    accel_z = mpu_data["accel_z"]
    return pitch < -5 or (pitch < -2 and accel_z < 9.0)

def is_riding(data):
    return data.get("speed", 0) > 5

# Main loop
def main():
    global euc, connected, stop_active, neutral_pitch
    # Calibra MPU6050
    if settings["use_imu"]:
        neutral_pitch = calibrate_mpu()

    # Avvia web server
    start_web_server()

    # Carica configurazione
    config = load_config()
    if config and config.get("mac"):
        adapter = config.get("adapter", "inmotion")
        euc = EucInterface(adapter=adapter)
        password = config.get("password")
        if euc.connect(config["mac"], password):
            connected = True
            feedback_led.value(1)
            utime.sleep_ms(3000)
            feedback_led.value(0)

    while True:
        # Gestione connessione iniziale
        if check_connect_press() and not connected:
            euc = EucInterface(adapter="inmotion")
            mac = euc.scan()
            if mac and euc.connect(mac, "000000"):
                save_config({"mac": mac, "adapter": "inmotion", "password": "000000"})
                connected = True
                feedback_led.value(1)
                utime.sleep_ms(3000)
                feedback_led.value(0)

        # Aggiornamento dati e luci
        if connected and euc:
            data = euc.get_data()
            if data:
                stop_active = check_deceleration(data)
                if settings["use_imu"] and is_riding(data):
                    mpu_data = mpu.get_data()
                    stop_active |= check_braking(mpu_data)
                turn_state = read_turn_state()
                update_lights(np, turn_state, stop_active, settings, bh1750)
        utime.sleep_ms(100)

if __name__ == "__main__":
    main()
