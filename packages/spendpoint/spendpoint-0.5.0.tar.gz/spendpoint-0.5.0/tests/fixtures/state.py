import pytest


@pytest.fixture(params=["http://localhost:8000"])
def test_data(request):
    return request.params
