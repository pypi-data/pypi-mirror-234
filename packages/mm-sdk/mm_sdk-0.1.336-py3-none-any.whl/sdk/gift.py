import datetime

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl

from .client import SDKClient, SDKResponse


class ServiceCode(Enum):
    lmk = "lmk"
    lab = "lab"


class GiftCodesRequest(BaseModel):
    code: str = None
    not_expired: bool = True
    is_promo: bool = True


class GiftCodeRequest(BaseModel):
    code: str


class UseCode(BaseModel):
    code: str
    service: ServiceCode
    phone: Optional[str] = Field(description="Телефон клиента, применяющего промокод")
    object_id: Optional[str] = Field(
        description="Идентификатор заказа, к которому применяется промокод в системе источника"
    )
    order_id: Optional[str] = Field(
        description="Идентификатор заявки/предварительной записи связанной с заявкой. Без него промокод арендуется на краткое время"
    )
    source: str = Field(description="Источник, может быть любым текстом")
    cost: Optional[int] = Field(description="Цена без применения промокодов")
    visit_at: Optional[datetime.date] = Field(
        description="Нужна для проверки действителен, ли промокод на дату визита"
    )

    class Config:
        use_enum_values = True


class UnUseCode(BaseModel):
    code: str
    object_id: str

    class Config:
        use_enum_values = True


class GiftCodeResponse(BaseModel):
    code: str
    amount: int
    dc: datetime.datetime
    expired_date: datetime.datetime
    used_date: Optional[datetime.datetime]
    is_reusable: bool
    is_promo: bool
    is_first_time: bool
    min_cost: Optional[int]


class GiftError(BaseModel):
    code: str
    message: str


class GiftCodeCheckResponse(GiftCodeResponse):
    errors: List[GiftError]


class GiftService:
    def __init__(self, client: SDKClient, url: HttpUrl):
        self._client = client
        if not url.endswith("/"):
            url = f"{url}/"
        self._url = url

    def get_codes(
        self, query: GiftCodesRequest = GiftCodesRequest(), timeout=3
    ) -> SDKResponse[List[GiftCodeResponse]]:
        return self._client.get(
            self._url + "gifts/rest/",
            GiftCodeResponse,
            params=query.dict(exclude_none=True),
            timeout=timeout,
        )

    def get_code(
        self, query: GiftCodeRequest, timeout=3
    ) -> SDKResponse[GiftCodeResponse]:
        params = query.dict(exclude_none=True)
        code = params.pop("code")
        return self._client.get(
            self._url + f"gifts/rest/{code}/",
            GiftCodeResponse,
            params=params,
            timeout=timeout,
        )

    def use(self, query: UseCode, timeout: int = 3) -> SDKResponse[GiftCodeResponse]:
        params = query.dict(exclude_none=True)
        code = params.pop("code")
        return self._client.patch(
            self._url + f"gifts/rest/{code}/use/",
            GiftCodeResponse,
            data=params,
            timeout=timeout,
        )

    def un_use(
        self, query: UnUseCode, timeout: int = 3
    ) -> SDKResponse[GiftCodeResponse]:
        params = query.dict(exclude_none=True)
        code = params.pop("code")
        return self._client.patch(
            self._url + f"gifts/rest/{code}/un_use/",
            GiftCodeResponse,
            data=params,
            timeout=timeout,
        )

    def check(
        self, query: UseCode, timeout: int = 3
    ) -> SDKResponse[GiftCodeCheckResponse]:
        params = query.dict(exclude_none=True)
        code = params.pop("code")
        return self._client.get(
            self._url + f"gifts/rest/{code}/check/",
            GiftCodeCheckResponse,
            params=params,
            timeout=timeout,
        )
