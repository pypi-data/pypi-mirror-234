import datetime

from typing import List, Optional, Any
from typing.io import BinaryIO

from pydantic import BaseModel, HttpUrl
from .client import SDKClient, SDKResponse


class SignRequest(BaseModel):
    thumbprint: str
    xml_file: Any


class SignResponse(BaseModel):
    signedContent: str
    filename: str


class CryptoProService:
    def __init__(self, client: SDKClient, url: HttpUrl):
        self._client = client
        self._url = url

    def sign(
        self, query: SignRequest, token: str, timeout=3
    ) -> SDKResponse[SignResponse]:
        return self._client.post(
            self._url + "signer",
            SignResponse,
            params={
                "thumbprint": query.thumbprint,
                "api-key": token
            },
            files={"file": query.xml_file},
            timeout=timeout,
        )
