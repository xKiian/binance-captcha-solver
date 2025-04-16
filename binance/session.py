import time

from curl_cffi import requests
from binance.fingerprint import Fingerprint
from binance.crypto import BinanceCrypto
from json import dumps


class BinanceCaptcha:
    def __init__(self,
                 security_check_response_validate_id: str = "",  # from precheck request
                 biz_id: str = "register",  # from precheck request
                 user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
                 ):
        self.session = requests.Session(
            impersonate="chrome116",
            default_headers=0,
            akamai="1:65536;2:0;4:6291456;6:262144|15663105|0|m,a,s,p",
            extra_fp={
                "tls_signature_algorithms": [
                    "ecdsa_secp256r1_sha256",
                    "rsa_pss_rsae_sha256",
                    "rsa_pkcs1_sha256",
                    "ecdsa_secp384r1_sha384",
                    "rsa_pss_rsae_sha384",
                    "rsa_pkcs1_sha384",
                    "rsa_pss_rsae_sha512",
                    "rsa_pkcs1_sha512"
                ],
                "tls_grease": True,
                "tls_permute_extensions": True
            },
            verify=False
        )

        self.user_agent = user_agent
        self.security_check_response_validate_id = security_check_response_validate_id
        self.biz_id = biz_id
        self.device = Fingerprint(self.user_agent)
        self.sv = "20220906"  # should be static

    def _get_captcha(self) -> dict:
        payload = f"bizId={self.biz_id}&sv={self.sv}&lang=en&securityCheckResponseValidateId={self.security_check_response_validate_id}&clientType=web"

        self.session.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'bnc-uuid': 'xxx',
            'cache-control': 'no-cache',
            'captcha-sdk-version': '1.0.0',
            'clienttype': 'web',
            'content-type': 'text/plain; charset=UTF-8',
            'device-info': self.device.generate_device_id(),
            'fvideo-id': 'xxx',
            'origin': 'https://accounts.binance.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://accounts.binance.com/en/register?',
            # 'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'x-captcha-se': 'true',
        }

        response = self.session.post("https://accounts.binance.com/bapi/composite/v1/public/antibot/getCaptcha",
                                     data=payload)

        return response.json()

    def _validate_captcha(self, captcha_data: dict) -> str:
        data = self.device.generate_data("https://bin.bnbstatic.com" + captcha_data["path2"])
        data_encrypted = BinanceCrypto.encrypt(dumps(data, separators=(",", ":")), captcha_data["ek"])

        time.sleep(.5)

        payload = {
            'bizId': self.biz_id,
            'sv': self.sv,
            'lang': 'en',
            'securityCheckResponseValidateId': self.security_check_response_validate_id,
            'clientType': 'web',
            'data': data_encrypted,
            's': BinanceCrypto.calculate_s(
                self.biz_id + captcha_data["sig"] + data_encrypted + captcha_data.get("salt", "")),
            'sig': captcha_data["sig"],
        }

        response = requests.post(
            'https://accounts.binance.com/bapi/composite/v1/public/antibot/validateCaptcha',
            data=payload,
        )
        return response.json()["data"]["token"]

    def solve(self) -> str:
        captcha = self._get_captcha()
        if captcha["data"]["captchaType"] != "SLIDE":
            raise NotImplementedError(f"Captcha type {captcha['data']['captchaType']} is not supported")

        token = self._validate_captcha(captcha["data"])
        return token
