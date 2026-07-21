from typing import Any

import requests
from django.conf import settings


class EcontAPIError(Exception):
    """Грешка при комуникация с Econt API."""


def _post_to_econt(endpoint: str, payload: dict) -> dict[str, Any]:
    url = f"{settings.ECONT_API_BASE_URL}/{endpoint}"

    try:
        response = requests.post(
            url,
            json=payload,
            auth=(
                settings.ECONT_USERNAME,
                settings.ECONT_PASSWORD,
            ),
            timeout=15,
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        raise EcontAPIError(
            "Възникна проблем при свързването с Еконт."
        ) from error

    except ValueError as error:
        raise EcontAPIError(
            "Еконт върна невалиден отговор."
        ) from error


def get_cities() -> list[dict]:
    data = _post_to_econt(
        "Nomenclatures/NomenclaturesService.getCities.json",
        {
            "countryCode": "BGR",
        },
    )

    return data.get("cities", [])


def get_offices(city_id: int) -> list[dict]:
    data = _post_to_econt(
        "Nomenclatures/NomenclaturesService.getOffices.json",
        {
            "countryCode": "BGR",
            "cityID": city_id,
        },
    )

    return data.get("offices", [])