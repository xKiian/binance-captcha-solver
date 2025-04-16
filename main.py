from binance.session import BinanceCaptcha
import time

while True:
    binance = BinanceCaptcha()

    start = time.time()
    token = binance.solve()
    end = time.time()

    print(f"[Solved] {token[:50]} | Took {round(end - start, 2)} seconds")
    time.sleep(2)