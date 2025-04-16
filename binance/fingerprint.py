import random, base64, json

from binance.biometrics import MouseMovement
from binance.slide import SlideSolver


class Fingerprint:
    def __init__(self, user_agent):
        self.user_agent = user_agent

    @staticmethod
    def _generate_unflagged():
        return int(random.random() * 32) * 2 + 1  # even = flagged | uneven = unflagged

    @staticmethod
    def generate_ev() -> dict:
        return {
            'wd': Fingerprint._generate_unflagged(),  # selenium check
            'im': Fingerprint._generate_unflagged(),  # mobile check
            'de': "",
            'prde': ",".join([str(Fingerprint._generate_unflagged()) for _ in range(4)]),  # 4 checks
            'brla': Fingerprint._generate_unflagged(),
            'pl': "Win32",  # platform
            'wiinhe': 945,  # innerHeight
            'wiouhe': '1032'  # outerHeight
        }

    @staticmethod
    def generate_data(url: str) -> dict:
        dist = SlideSolver(url).solve()
        return {
            "ev": Fingerprint.generate_ev(),
            "be": MouseMovement().generate_mouse_movement_slide(dist),
            "dist": dist,
            "imageWidth": "310"
        }

    def generate_device_id(self):
        device_id = {
            "screen_resolution": "1920,1080",
            "available_screen_resolution": "1920,1032",
            "system_version": "unknown",
            "brand_model": "unknown",
            "timezone": "",
            "web_timezone": "Europe/Berlin",
            "timezoneOffset": -120,
            "user_agent": self.user_agent,
            "list_plugin": "PDF Viewer,Chrome PDF Viewer,Chromium PDF Viewer,Microsoft Edge PDF Viewer,WebKit built-in PDF",
            "platform": "Win32",
            "webgl_vendor": "unknown",
            "webgl_renderer": "unknown"
        }

        return base64.b64encode(json.dumps(device_id, separators=(",", ":")).encode("utf-8")).decode("utf-8")
