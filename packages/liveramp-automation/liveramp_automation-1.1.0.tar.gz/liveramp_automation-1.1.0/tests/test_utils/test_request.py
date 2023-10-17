from liveramp_automation.utils.request import request_post, request_get


def test_request_post():
    url = 'https://serviceaccounts.liveramp.com/authn/v1/oauth2/token'
    headers = {"Content-Type": 'application/x-www-form-urlencoded'}
    data = {
        "grant_type": "password",
        "scope": "openid",
        "client_id": "liveramp-api"
    }
    response = request_post(url, headers=headers, data=data)
    assert response.status_code == 400


def test_request_get():
    url = 'https://www.google.com/'
    headers = None
    response = request_get(url, headers=headers)
    assert response
    assert response.ok
