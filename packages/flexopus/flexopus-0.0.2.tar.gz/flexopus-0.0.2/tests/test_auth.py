from flexopus import FlexopusApi
import pytest

def test_create_tenant_url_none():
    with pytest.raises(AttributeError):
        FlexopusApi(None, None)

def test_create_access_token_none():
    with pytest.raises(AttributeError):
        FlexopusApi('https://demo.flexopus.com', None)

def test_create_ok():
    cases = [
        (
            'https://demo.flexopus.com',
            'dummy-token',
            'https://demo.flexopus.com/api/v1',
            {
                "Accept": "application/json",
                "Authorization": "Bearer dummy-token",
            }
        ),
        (
            '    https://demo.flexopus.com    ',
            'dummy-token-2',
            'https://demo.flexopus.com/api/v1',
            {
                "Accept": "application/json",
                "Authorization": "Bearer dummy-token-2",
            }
        ),
    ]
    for (tenant_url, access_token, exp_base_url, exp_headers) in cases:
        api = FlexopusApi(tenant_url, access_token)
        assert api._base_url == exp_base_url
        assert api._access_token == access_token
        assert api._headers == exp_headers