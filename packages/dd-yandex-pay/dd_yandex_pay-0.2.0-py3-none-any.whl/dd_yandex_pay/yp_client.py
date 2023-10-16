import urllib
import uuid
from typing import Final
from typing import List
from typing import Optional
from typing import Union

import requests

from dd_yandex_pay.constants import BASE_URL_PRODUCTION
from dd_yandex_pay.exceptions import YandexPayAPIError


class YandexPayClient:
    """
    Клиент обёртка для [Yandex Pay API][yandex_pay_api_docs].

    [yandex_pay_api_docs]: https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/
    """

    RESOURCE_ORDER_CREATE: Final[str] = "v1/orders"
    RESOURCE_ORDER_DETAILS: Final[str] = "v1/orders/{id}"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = BASE_URL_PRODUCTION,
        timeout: Optional[Union[float, int, tuple]] = (3, 10),
        deadline: Optional[int] = 10 * 1000,
    ):
        """
        Attributes:
            api_key: Ключи [Yandex Pay Merchant API](https://console.pay.yandex.ru/web/account/settings/online).
            base_url: Базовый адрес Yandex Pay API.
            timeout: Дефолтный таймаут запроса для [requests](https://requests.readthedocs.io/en/latest/user/advanced/#timeouts).
            deadline: Дефолтный таймаут запроса в миллисекундах для [яндекс](https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/).
        """

        self.api_key = api_key
        self.base_url = base_url
        self.default_timeout = timeout
        self.default_deadline = deadline

    # Helpers

    def get_headers(self, **custom: dict) -> dict:
        """
        Создаёт заголовки для запроса.

        Attributes:
            custom: Объект с дополнительными заголовками (так же с помощью этого объекта можно
                переопределить генерируемые заголовки).

        Returns:
            Объект с заголовками.
        """

        return {
            "Authorization": f"Api-Key {self.api_key}",
            "X-Request-Id": str(uuid.uuid4()),
            "X-Request-Timeout": str(self.default_deadline),
            # "X-Request-Attempt": 1, ???
            **custom,
        }

    def get_url(self, resourse: str) -> str:
        """
        Формирует адрес для запроса к API.

        Attributes:
            resourse: Ресурс к которому необходимо выполнить запрос.

        Returns:
            Адрес для запроса.
        """

        return urllib.parse.urljoin(self.base_url, resourse)

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[dict] = None,
        **kwargs: dict,
    ) -> requests.Response:
        """
        Метод для выполнения запросов к Yandex Pay API.

        Attributes:
            method: Метод запроса.
            url: Запрашиваемый ресурс.
            headers: Объект с заголовками.
            kwargs: Объект с кастомными заголовками.

        Returns:
            Полученый ответ.
        """

        kwargs.setdefault("timeout", self.default_timeout)
        kwargs["headers"] = self.get_headers(**(headers or {}))
        response = requests.request(method, url, **kwargs)
        return response

    def response_handler(
        self,
        response: requests.Response,
        check_data_availability: Optional[bool] = False,
    ) -> dict:
        """
        Обработчик данных ответа.

        Attributes:
            response: Ответ API Yandex Pay.
            check_data_availability: Флаг, указывающий на необходимость проверки на наличие
                параметра `data` в ответе.

        Returns:
            Данные ответа API.

        Raises:
            requests.exceptions.HTTPError: HTTP Errors.
            dd_yandex_pay.exceptions.YandexPayAPIError: API Errors.
        """

        response.raise_for_status()
        response_data = response.json()

        if response_data.get("status", "") != "success":
            msg = response_data.get("reason", "Unknown error")
            code = response_data.get("reasonCode", "unknown_error")
            raise YandexPayAPIError(response, msg, code)

        if check_data_availability and "data" not in response_data:
            msg = "Response has no data."
            code = "has_no_data"
            raise YandexPayAPIError(response, msg, code)

        return response_data

    # API

    def create_order(
        self,
        cart: dict,
        currencyCode: str,
        orderId: str,
        redirectUrls: dict,
        availablePaymentMethods: Optional[List[str]] = None,
        extensions: Optional[dict] = None,
        ttl: Optional[int] = None,
        **kwargs: dict,
    ) -> dict:
        """
        Запрос на создание ссылки на оплату заказа.

        Подбронее о данных и ответе в документации [яндекса](https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v1_orders-post).

        Attributes:
            cart: [Корзина](https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v1_orders-post#renderedcart).
            currencyCode: Трехбуквенный код валюты заказа (ISO 4217).
            orderId: Идентификатор заказа.
            redirectUrls: [Ссылки для переадресации](https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v1_orders-post#merchantredirecturls)
                пользователя с формы оплаты.
            availablePaymentMethods: Доступные методы оплаты на платежной форме Яндекс Пэй.
            extensions: [Дополнительные параметры](https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v1_orders-post#orderextensions)
                для оформления оффлайн заказа.
            ttl: Время жизни заказа (в секундах).
            kwargs: Прочие дополнительные параметры метода [request][requests.request] кроме method,
                url и json.

        Returns:
            Данные ответа на создание ссылки для оплаты.

        Raises:
            requests.exceptions.HTTPError: HTTP Errors.
            dd_yandex_pay.exceptions.YandexPayAPIError: API Errors.
        """

        json = {
            "cart": cart,
            "currencyCode": currencyCode,
            "orderId": orderId,
            "redirectUrls": redirectUrls,
        }

        if availablePaymentMethods:
            json["availablePaymentMethods"] = availablePaymentMethods

        if extensions:
            json["extensions"] = extensions

        if ttl:
            json["ttl"] = ttl

        response = self.request(
            "POST",
            self.get_url(self.RESOURCE_ORDER_CREATE),
            json=json,
            **kwargs,
        )

        response_data = self.response_handler(response, True)
        return response_data["data"]

    def get_order(self, order_id: str, **kwargs: dict) -> dict:
        """
        Запрос на получение деталей заказа.

        Подбронее о данных и ответе в документации [яндекса](https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v1_order-get).

        Attributes:
            order_id: Идентификатор заказа.
            kwargs: Прочие дополнительные параметры метода [request][requests.request] кроме method,
                url и json.

        Returns:
            Полученные данные заказа.

        Raises:
            requests.exceptions.HTTPError: HTTP Errors.
            dd_yandex_pay.exceptions.YandexPayAPIError: API Errors.
        """

        response = self.request(
            "GET",
            self.get_url(self.RESOURCE_ORDER_DETAILS.format(id=order_id)),
            **kwargs,
        )

        response_data = self.response_handler(response, True)
        return response_data["data"]
