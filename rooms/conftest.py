import pytest
from model_bakery import baker


@pytest.fixture
def new_room():
    country = baker.make("common.Country", code="UZ")
    region = baker.make("common.Region", country=country)
    return baker.make("rooms.Room", region=region)
