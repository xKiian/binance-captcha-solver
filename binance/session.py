from curl_cffi import requests


class BinanceCaptcha:
    def __init__(self):
        self.http_session = requests.Session(
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

    #todo
    def _sort_headers(self, input_headers: dict) -> dict:
        key_order: list[str] = [
            "Host",
            "Cookie",
            "Content-Length",
            "sec-ch-ua-platform",
            "Cache-Control",
            "x-ark-esync-value",
            "Accept-Language",
            # "sec-ch-ua",
            "sec-ch-ua-mobile",
            "Upgrade-Insecure-Requests",
            "User-Agent",
            "X-NewRelic-Timestamp",
            "X-Requested-ID",
            "X-Requested-With",
            "Accept",
            "Content-Type",
            "Origin",
            "Sec-Fetch-Site",
            "Sec-Fetch-Mode",
            "Sec-Fetch-Dest",
            "Referer",
            "Accept-Encoding",
            "Connection",
            "Priority"
        ]
        order_index = {
            header: i for i, header in enumerate(key_order)
        }

        def sort_key(header_pair) -> int:
            header_name, _ = header_pair
            return order_index.get(header_name, len(key_order))

        sorted_headers = dict(
            sorted(input_headers.items(), key=sort_key)
        )

        return sorted_headers

    def _precheck(self):
        url = "https://accounts.binance.com/bapi/accounts/v1/public/account/security/request/precheck"

        payload = {
            "bizType": "register",
            "email": "clementina40012@rrbe.underseagolf.com",
            "deviceInfo": "eyJzY3JlZW5fcmVzb2x1dGlvbiI6IjE5MjAsMTA4MCIsImF2YWlsYWJsZV9zY3JlZW5fcmVzb2x1dGlvbiI6IjE5MjAsMTAzMiIsInN5c3RlbV92ZXJzaW9uIjoiV2luZG93cyAxMCIsImJyYW5kX21vZGVsIjoidW5rbm93biIsInN5c3RlbV9sYW5nIjoiZW4tVVMiLCJ0aW1lem9uZSI6IkdNVCswMjowMCIsInRpbWV6b25lT2Zmc2V0IjotMTIwLCJ1c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzNS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwibGlzdF9wbHVnaW4iOiJQREYgVmlld2VyLENocm9tZSBQREYgVmlld2VyLENocm9taXVtIFBERiBWaWV3ZXIsTWljcm9zb2Z0IEVkZ2UgUERGIFZpZXdlcixXZWJLaXQgYnVpbHQtaW4gUERGIiwiY2FudmFzX2NvZGUiOiIzNmNiYTNkZCIsIndlYmdsX3ZlbmRvciI6Ikdvb2dsZSBJbmMuIChBTUQpIiwid2ViZ2xfcmVuZGVyZXIiOiJBTkdMRSAoQU1ELCBBTUQgUmFkZW9uIFJYIDU3MDAgKDB4MDAwMDczMUYpIERpcmVjdDNEMTEgdnNfNV8wIHBzXzVfMCwgRDNEMTEpIiwiYXVkaW8iOiIxMjQuMDQzNDc1Mjc1MTYwNzQiLCJwbGF0Zm9ybSI6IldpbjMyIiwid2ViX3RpbWV6b25lIjoiRXVyb3BlL0JlcmxpbiIsImRldmljZV9uYW1lIjoiQ2hyb21lIFYxMzUuMC4wLjAgKFdpbmRvd3MpIiwiZmluZ2VycHJpbnQiOiJlNDJmMTAzMjBkODAyNDVlZTFhNTRhZjYxZjJmNTA2YyIsImRldmljZV9pZCI6IiIsInJlbGF0ZWRfZGV2aWNlX2lkcyI6IiJ9",
            "registerationMethod": "EMAIL"
        }
        headers = {
            "host": "accounts.binance.com",
            "connection": "keep-alive",
            "sec-ch-ua-platform": "\"Windows\"",
            "csrftoken": "d41d8cd98f00b204e9800998ecf8427e",
            "lang": "en",
            "x-se-rd": "gIDFgAFkBGIVBUU5UWgwwZZBhAA5TESV1RRVfUUVlVRVQEFNWVEF1",
            "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
            "sec-ch-ua-mobile": "?0",
            "fvideo-id": "330fdc5f1427ac68add27a8974dca45b4ffff45e",
            "bnc-uuid": "e215b3ff-88d5-4644-9252-bf3b88e9cebb",
            "x-passthrough-token": "",
            "x-se-gsd": "",
            "content-type": "application/json",
            "x-se-pd": "AcMDlRgdUQSGVwXkRDA9QZZBQDltUETUVUNVfUk9lVRVQF1NWVYO1",
            "fvideo-token": "GQTHSd1jVziFWMpLCHKMxOlhMPlivOUkS5cRZgi01NQHAysMEaTkdurlo9GbHvTjLZhqInRJUA0InYmYNwCJysd8gNb/4hedwSYn9P3ZchHBTUBmvFPnPiYmjrw8ZppPpFapI8CAeCJXSV2/PNCRzRAoNvG19BMopXz9eiVvf9oxgHXpORz4ZG7uT8fMPdh7o=29",
            "x-se-bh": "TlVYVk1XVgcUD0NMVVpRSFBXUR4MXU4AUVRbUldTGAlWT1ZbVkhQAlgeGlZPVF1cT1FUUh0JVBpfW05NUVZVGA5QUE9ZVFMbW1dGHQ9SVElbUlFOUlFRSwBQVltSV1EYCVJQTFVZUU8EXVALDFdOU1xWTlJXUBgOAkVVT1dOUFFVHw9UT1ZcVBtbV0YdD1tJU1tbTVFUVB9aXk9AWFNPV1FTHgxVTFNaBERRQlEeDlVUU1FOUlRQGA4PRVVAVU5QUVwfD1dPVlNUG1tXQB0PVElTVFtNUVRRH1pfT0BZUk9XUVceDFVMU1sGRFFCUh4OU0lUWlNOUlFRSwVTR0xVW1dIUFdTHgxQTgQCXk5EVlEfCVVOVVRVTVdUBBQPQUxVVlxIUFVTHgxTTgBeUltSVVIYCVRPVlRTSFABUR4aVk9UUlFPUVdVHQlUGl9UQE1RVVEYDlVMVVZUTwReUQsMVU5TCEZZQARTVlBXAl5QQFNbWlZdTlVUUE1XVAQUD0dMVVZWSFBVUh4EV1EPRVVCUk5QU1cfD1FPVlFQG1tVRB0PVUlTVlZNUVZXH1pQUFpWV1ZIV1RRHQ9ZSVFOQ1NDXkFVNwACPk9SVFdPUFNATUZRFVJAFT4RFjtJUFZSTlVcQUpEQAQGQFlGDxASUQ0WCQVSDkBbQxZBXlVUVlVXV1ZUBFpRQlZOQRcNQVhXUhw=GkAGSgcUQ1gYRgFBWFNOQwlBDVlXQ01AB0ZeUE5DF0NeUBtKCVVbUE9GB0FYUB9NRg5DSlgMQ1JBXkYKPRUHPgYNGg4NBQwrFwEJTgAmA1g3F2QxT0VYUU9RVEQIU1NbHQBXBFhPT1BRT1dRV09TV01VUksdVEFMWlJXSFBXVR4CVk4PWVFbUldXSVZWTlBTHVYHAlxSWllUUEhQUFFMVVRIUQUUUAJQUlFJXFVWTVZSUEEbBFtbCwxVTlxWUk5SUVcYDgBFWkVUTlBXVh9SDFpMXFEORFFFVh5TCVJOWlJRTVdRBBRSE1ZWTlxRUE5SUlJJVgNEUEIdUhZcXU5aVFFNV1MEFFIcU1ZbGFhXVlAdD1dJWwdaTkRUUB8JUE5aUVFNV1YGFA9ATFpTUUhQV1EeDFNOD1hVW1JWWhgJVU9ZUlhIUANfHhpWT1tVVU9RVVQdCVQaUFNDTVFXVxgOVUxaUFxPVaWllSUk",
            "x-trace-id": "bb63a391-73d5-46fd-8c59-34faba0ba72b",
            "x-ui-request-trace": "bb63a391-73d5-46fd-8c59-34faba0ba72b",
            "bnc-time-zone": "Europe/Berlin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "clienttype": "web",
            "bnc-location": "",
            "device-info": "eyJzY3JlZW5fcmVzb2x1dGlvbiI6IjE5MjAsMTA4MCIsImF2YWlsYWJsZV9zY3JlZW5fcmVzb2x1dGlvbiI6IjE5MjAsMTAzMiIsInN5c3RlbV92ZXJzaW9uIjoiV2luZG93cyAxMCIsImJyYW5kX21vZGVsIjoidW5rbm93biIsInN5c3RlbV9sYW5nIjoiZW4tVVMiLCJ0aW1lem9uZSI6IkdNVCswMjowMCIsInRpbWV6b25lT2Zmc2V0IjotMTIwLCJ1c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzNS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwibGlzdF9wbHVnaW4iOiJQREYgVmlld2VyLENocm9tZSBQREYgVmlld2VyLENocm9taXVtIFBERiBWaWV3ZXIsTWljcm9zb2Z0IEVkZ2UgUERGIFZpZXdlcixXZWJLaXQgYnVpbHQtaW4gUERGIiwiY2FudmFzX2NvZGUiOiIzNmNiYTNkZCIsIndlYmdsX3ZlbmRvciI6Ikdvb2dsZSBJbmMuIChBTUQpIiwid2ViZ2xfcmVuZGVyZXIiOiJBTkdMRSAoQU1ELCBBTUQgUmFkZW9uIFJYIDU3MDAgKDB4MDAwMDczMUYpIERpcmVjdDNEMTEgdnNfNV8wIHBzXzVfMCwgRDNEMTEpIiwiYXVkaW8iOiIxMjQuMDQzNDc1Mjc1MTYwNzQiLCJwbGF0Zm9ybSI6IldpbjMyIiwid2ViX3RpbWV6b25lIjoiRXVyb3BlL0JlcmxpbiIsImRldmljZV9uYW1lIjoiQ2hyb21lIFYxMzUuMC4wLjAgKFdpbmRvd3MpIiwiZmluZ2VycHJpbnQiOiJlNDJmMTAzMjBkODAyNDVlZTFhNTRhZjYxZjJmNTA2YyIsImRldmljZV9pZCI6IiIsInJlbGF0ZWRfZGV2aWNlX2lkcyI6IiJ9",
            "accept": "*/*",
            "origin": "https://accounts.binance.com",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://accounts.binance.com/en/register/",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "cookie": "aws-waf-token=52f8ae94-56b1-4940-8bb3-c52ec8e77034:CQoAev11fZZEAAAA:KzMUY0812XcC6kQHsRDtqvCZYQgjggwQOeXmHznAc4hOSyZuARxjGn5KIYNtMyeOSQMElzqK/x4DHekAMvnXS+VFW7SiC4q2kKGO4FM4noGM5+84THXB/mOv40cObWYTkRVXWYj1SNRLdtdFmMI/PtRkFW54pDFQn0ZngBs35IC5Zi9PWRw7KF9M8xvfgfkZBPKL9Kb4Ow==; bnc-uuid=e215b3ff-88d5-4644-9252-bf3b88e9cebb; lang=en; language=en; se_sd=Q8RBQBBFVEFUhIRgaCRcgZZHQFBMTETUVpdVfUk9lVRVQBlNWVUe1; se_gd=RsSDBXl8TRXBF1QZRFllgZZF1FhQTBTUVpVVfUk9lVRVQCVNWV5X1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22196300a606ea1c-01943129c9eba1e-26011c51-2073600-196300a606f1cf0%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk2MzAwYTYwNmVhMWMtMDE5NDMxMjljOWViYTFlLTI2MDExYzUxLTIwNzM2MDAtMTk2MzAwYTYwNmYxY2YwIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D; sajssdk_2015_cross_new_user=1; se_gsd=aDAlK0NmNjojDVo3JiY7MBA2AgsGBgQLUVpAVVZVV1VXCVNT1; BNC_FV_KEY=330fdc5f1427ac68add27a8974dca45b4ffff45e; BNC_FV_KEY_T=101-EegHrrX1xVvWM5KNfMOjWvkAW3mlx6Iowl3pZSvYGWWQULgZI3ggoIWuTEg1Yxyyac1az%2FGboCp59GYHU%2Fnj5Q%3D%3D-oKOeirGIsMR3xfFlJLVAng%3D%3D-09; BNC_FV_KEY_EXPIRE=1744584314961; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Apr+13+2025+18%3A45%3A15+GMT%2B0200+(Central+European+Summer+Time)&version=202411.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=5b6b1750-7b54-4300-b6f7-eacf4cde62a9&interactionCount=0&isAnonUser=1&landingPath=https%3A%2F%2Faccounts.binance.com%2Fen%2Fregister%2F&groups=C0001%3A1%2CC0003%3A0%2CC0004%3A0%2CC0002%3A0"
        }

        response = requests.post(url, json=payload, headers=headers)

        print(response.text)