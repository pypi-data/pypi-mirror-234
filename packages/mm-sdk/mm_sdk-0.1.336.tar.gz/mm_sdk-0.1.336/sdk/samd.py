import datetime

from enum import IntEnum
from typing import List, Optional

from pydantic import BaseModel

from .client import Empty, HttpUrl, SDKClient, SDKResponse


class OrderType(IntEnum):
    lmk = 0
    prof = 1
    lab = 2
    cert = 3


class AddPatientRequest(BaseModel):
    uuid: str
    fname: str
    mname: Optional[str]
    lname: str
    birth: datetime.date
    sex: str

    passport_type: Optional[str]
    passport_number: Optional[str]
    passport_series: Optional[str]
    passport_date: Optional[datetime.date]
    passport_department_code: Optional[str]

    snils: Optional[str]

    phone: Optional[str]
    email: Optional[str]

    quarter: Optional[str]
    building: Optional[str]
    city: Optional[str]
    street: Optional[str]

    registration_quarter: Optional[str]
    registration_building: Optional[str]
    registration_city: Optional[str]
    registration_street: Optional[str]

    @property
    def full_address(self):
        return " ".join(
            a
            for a in [
                self.city,
                self.street,
                self.building,
                self.quarter,
            ]
            if a
        )

    @property
    def registration_address(self):
        return " ".join(
            a
            for a in [
                self.registration_city,
                self.registration_street,
                self.registration_building,
                self.registration_quarter,
            ]
            if a
        )


class MedCenter(BaseModel):
    id: str
    license: str
    license_registration: Optional[str]
    ogrn: str
    okpo: str
    legalname: str
    phone: str  # TODO надо?
    # email: str  # TODO надо?
    legaladdress: str
    zip_code: str


class Order(BaseModel):
    number: str
    exams_start: datetime.datetime
    exams_done: datetime.datetime
    org_name: Optional[str]
    org_inn: Optional[str]
    post: str
    conclusion: str
    next_date: datetime.date
    factors: list


class Doctor(BaseModel):
    speciality: str
    post: str
    mis_id: str
    lname: str
    fname: str
    mname: Optional[str]
    snils: Optional[str]


class Exam(BaseModel):
    conclusion: str
    date: datetime.date
    doctor: Doctor
    id: str


class LabService(BaseModel):
    date: datetime.date
    result: str
    name: str
    id: str


class FuncDiag(BaseModel):
    date: datetime.date
    conclusion: str
    name: str
    id: str


class Vaccine(BaseModel):
    name: str
    step: str
    date: datetime.date


class AddMedRecordRequest(BaseModel):
    mis_id: str  # номер заявки
    order_type: OrderType
    creation_date: datetime.datetime  # lmk - order_time / prof - exams_start
    med_center: MedCenter
    patient: AddPatientRequest
    order: Order
    head_doctor: Optional[Doctor]
    exams: List[Exam]
    lab_services: List[LabService]
    functional_diagnostics: List[FuncDiag]
    vaccinations: List[Vaccine]


class SamdService:
    def __init__(self, client: SDKClient, url: HttpUrl):
        self._client = client
        self._url = url
        self.add_patient_url = self._url + "/api/add_patient/"
        self.add_med_record_url = self._url + "/api/add_med_record/"

    def add_patient(self, query: AddPatientRequest, timeout=3) -> SDKResponse[Empty]:
        return self._client.post(
            self.add_patient_url,
            Empty,
            data=query.json(),
            headers={"Content-Type": "application/json"},
            timeout=timeout,
        )

    def add_med_record(
        self, query: AddMedRecordRequest, timeout=3
    ) -> SDKResponse[Empty]:
        return self._client.post(
            self.add_med_record_url,
            Empty,
            data=query.json(),
            headers={"Content-Type": "application/json"},
            timeout=timeout,
        )


class SendDataStatusRequest(BaseModel):
    order_type: OrderType
    order_number: str
    time_send: Optional[datetime.datetime]
    error_msg: Optional[str]


class SamdServiceMis:
    def __init__(self, client: SDKClient, url: HttpUrl):
        self._client = client
        self._url = url
        self.callback = self._url + "/samd/callback/"

    def send_callback(
        self, query: SendDataStatusRequest, timeout=3
    ) -> SDKResponse[Empty]:
        return self._client.post(
            self.callback,
            Empty,
            data=query.json(),
            headers={"Content-Type": "application/json"},
            timeout=timeout,
        )
