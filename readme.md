# Binance Captcha Solver

<div>
    <img src="https://wakatime.com/badge/user/839267df-3912-44c6-97f4-9e3f0425b716/project/06032300-f18e-4196-bb00-404af191bdce.svg" alt="wakatime">
</div>

---

## Example Usage

```python
from binance.session import BinanceCaptcha

binance = BinanceCaptcha(
    biz_id="login",
    security_check_response_validate_id="7d1bf5349be4481c8b2de29cc24f8451"
)

token = binance.solve()

print(token)
# token = captcha#e479223...416da2622fe0-pvazmct322p...NwVAngrDSLmfy
```

---

## Article

[https://blog.castle.io/what-a-binance-captcha-solver-tells-us-about-todays-bot-threats/](here)is an article i found about my repository. 
Not everything said there is true, but it's great if you don't understand my code.

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Star History

 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=xKiian/binance-captcha-solver&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=xKiian/binance-captcha-solver&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=xKiian/binance-captcha-solver&type=Date" />
 </picture>

---

## Disclaimer

This package is **unofficial** and not affiliated with **Binance© 2025**. Use it responsibly
and in accordance with their terms of service. Feel free to contact me if you want this taken down.