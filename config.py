import esp32
import binascii

def save_config(config):
    if "mac" in config:
        esp32.nvs_set_str("euc_mac", binascii.hexlify(config["mac"]).decode())
    if "adapter" in config:
        esp32.nvs_set_str("euc_adapter", config["adapter"])
    if "password" in config:
        esp32.nvs_set_str("euc_password", config["password"])

def load_config():
    config = {}
    try:
        config["mac"] = binascii.unhexlify(esp32.nvs_get_str("euc_mac"))
        config["adapter"] = esp32.nvs_get_str("euc_adapter")
        config["password"] = esp32.nvs_get_str("euc_password")
    except:
        pass
    return config
