from micropython.euc import EucInterface as BaseEucInterface
import ubluetooth

class EucInterface(BaseEucInterface):
    def __init__(self, adapter="inmotion"):
        super().__init__(adapter)
        self.ble = ubluetooth.BLE()
        self.ble.active(True)

    def scan(self):
        devices = []
        def callback(evt, data):
            if evt == 5:  # Scan result
                addr_type, addr, adv_type, rssi, adv_data = data
                name = adv_data.get("Complete local name", b"").decode()
                if name and ("V10" in name or "Sherman" in name or "Gotway" in name or "Begode" in name or "Kingsong" in name):
                    devices.append({"addr": addr, "name": name, "rssi": rssi})
        self.ble.irq(callback)
        self.ble.gap_scan(10000)
        utime.sleep_ms(10000)
        self.ble.gap_scan(0)
        return devices

    def connect(self, mac, password=None):
        try:
            if password and self.adapter == "inmotion":
                self._send_password(password)
            return super().connect(mac)
        except Exception as e:
            print("Connessione fallita:", e)
            return False

    def _send_password(self, password):
        # TODO: Implementare comando password per InMotion (es. per V10F)
        pass
