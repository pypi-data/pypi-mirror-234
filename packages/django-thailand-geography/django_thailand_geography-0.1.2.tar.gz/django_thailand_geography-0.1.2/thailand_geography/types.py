from typing import TypedDict


class LocationData(TypedDict):
    id: int
    provinceCode: int
    provinceNameEn: str
    provinceNameTh: str
    districtCode: int
    districtNameEn: str
    districtNameTh: str
    subdistrictCode: int
    subdistrictNameEn: str
    subdistrictNameTh: str
    postalCode: int
