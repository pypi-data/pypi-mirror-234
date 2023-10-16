import pytest

from sym.sdk.exceptions import PagerDutyError
from sym.sdk.integrations.pagerduty import is_on_call, users_on_call


class TestPagerdutyInterface:
    def test_is_on_call(self):
        user = {"username": "jon.doe@simi.org"}
        assert is_on_call(user) is None

    def test_users_on_call(self):
        assert users_on_call() is None

    def test_error_code(self):
        with pytest.raises(PagerDutyError) as error_info:
            raise PagerDutyError(name="UNKNOWN", message="foobar")

        assert error_info.value.error_code == "PagerDuty:UNKNOWN"
        assert error_info.value.message == "foobar"
