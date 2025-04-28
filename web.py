from microdot import Microdot, Response
import network
from euc import EucInterface
import esp32

app = Microdot()
wlan = network.WLAN(network.AP_IF)
euc = None

def start_web_server():
    wlan.active(True)
    wlan.config(essid="EUC-Lights", password="12345678")
    print("AP attivo:", wlan.ifconfig())

@app.route("/")
def index(req):
    with open("static/index.html") as f:
        return Response(f.read(), headers={"Content-Type": "text/html"})

@app.route("/scan")
def scan(req):
    global euc
    if not euc:
        euc = EucInterface(adapter="inmotion")
    devices = euc.scan()
    return {"devices": [{"name": d["name"], "addr": d["addr"].hex(), "rssi": d["rssi"]} for d in devices]}

@app.route("/connect", method="POST")
def connect(req):
    global euc
    data = req.json
    mac = bytes.fromhex(data["addr"])
    adapter = data.get("adapter", "inmotion")
    password = data.get("password")
    if not euc:
        euc = EucInterface(adapter=adapter)
    if euc.connect(mac, password):
        save_config({"mac": mac, "adapter": adapter, "password": password})
        return {"status": "success"}
    return {"status": "failed"}

@app.route("/settings", method="POST")
def settings(req):
    data = req.json
    esp32.nvs_set_str("use_imu", str(data.get("use_imu", False)))
    esp32.nvs_set_str("use_buzzer", str(data.get("use_buzzer", True)))
    esp32.nvs_set_str("use_brightness", str(data.get("use_brightness", True)))
    return {"status": "success"}

def run():
    app.run(port=80)
