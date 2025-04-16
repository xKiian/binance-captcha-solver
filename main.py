from binance.session import BinanceCaptcha
import time

binance = BinanceCaptcha(
    biz_id="login",
    security_check_response_validate_id="7d1bf5349be4481c8b2de29cc24f8451"
)

start = time.time()
token = binance.solve()
end = time.time()

print(f"[Solved] {token} | Took {round(end - start, 2)} seconds")
