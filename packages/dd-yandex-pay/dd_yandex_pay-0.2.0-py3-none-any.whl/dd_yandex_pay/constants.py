from typing import Final


# Base URL's

BASE_URL_PRODUCTION: Final[str] = "https://pay.yandex.ru/api/merchant/"
"""Боевой сервер"""

BASE_URL_SANDBOX: Final[str] = "https://sandbox.pay.yandex.ru/api/merchant/"
"""Тестовая среда"""


# Payment Method's

PAYMENT_METHODS_CARD: Final[str] = "CARD"
"""Код метода оплаты Картой"""

PAYMENT_METHODS_SPLIT: Final[str] = "SPLIT"
"""Код методда оплаты Яндекс Сплитом"""
