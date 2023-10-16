"""Test the authentication process."""

import pytest

from elmax_api.exceptions import ElmaxBadLoginError
from elmax_api.http import ElmaxLocal, Elmax
from tests import client, LOCAL_TEST, LOCAL_API_URL, PANEL_PIN

BAD_USERNAME = "thisIsWrong@gmail.com"
BAD_PASSWORD = "fakePassword"


@pytest.mark.asyncio
async def test_wrong_credentials():
    client = Elmax(username=BAD_USERNAME, password=BAD_PASSWORD) if LOCAL_TEST != "true" else ElmaxLocal(
        panel_api_url=LOCAL_API_URL, panel_code=PANEL_PIN)
    with pytest.raises(ElmaxBadLoginError):
        await client.login()


@pytest.mark.asyncio
async def test_good_credentials():
    jwt_data = await client.login()
    assert isinstance(jwt_data, dict)

    username = client.get_authenticated_username()
    # TODO: parametrize the following control
    #assert username == USERNAME
