import pytest

import refuel


@pytest.fixture
def refuel_client():
    options = {"api_key": "AXMfvufmROL8Qji9ZwOMTr94KTRkKVXuAb9ksipuYmu8c0esB8ZKRA"}
    return refuel.init(**options)
