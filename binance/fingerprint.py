import random


class Fingerprint:
    def __init__(self):
        ...

    @staticmethod
    def _generate_unflagged():
        return int(random.random() * 32) * 2 + 1  # "+1" means unflagged

    def generate_fingerprint(self):
        return {
            'wd': Fingerprint._generate_unflagged(),  # selenium check
            'im': Fingerprint._generate_unflagged(),  # mobile check
            'de': "",
            'prde': ",".join([str(Fingerprint._generate_unflagged()) for i in range(4)]),  # 4 checks
            'brla': Fingerprint._generate_unflagged(),
            'pl': "Win32",  # platform
            'wiinhe': 945,  # innerHeight
            'wiouhe': '1032'  # outerHeight
        }
