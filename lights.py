from machine import Pin
buzzer = Pin(11, Pin.OUT)

def get_brightness(bh1750, settings):
    if not settings["use_brightness"]:
        return 1.0
    lux = bh1750.luminance()
    if lux < 50:
        return 1.0
    elif lux < 200:
        return 0.6
    return 0.3

def update_lights(np, turn_state, stop_active, settings, bh1750):
    brightness = get_brightness(bh1750, settings)
    pos_color = (int(77 * brightness), 0, 0)
    stop_color = (int(255 * brightness), 0, 0)
    turn_color = (int(255 * brightness), int(255 * brightness), 0)
    np.fill(pos_color)
    buzzer.value(0)
    if stop_active:
        for i in range(3, 7):
            np[i] = stop_color
    elif turn_state == "left":
        for i in range(3):
            np[i] = turn_color if (utime.ticks_ms() % 1000 < 500) else (0, 0, 0)
        if settings["use_buzzer"]:
            buzzer.value(1 if utime.ticks_ms() % 1000 < 500 else 0)
    elif turn_state == "right":
        for i in range(7, 10):
            np[i] = turn_color if (utime.ticks_ms() % 1000 < 500) else (0, 0, 0)
        if settings["use_buzzer"]:
            buzzer.value(1 if utime.ticks_ms() % 1000 < 500 else 0)
    np.write()
