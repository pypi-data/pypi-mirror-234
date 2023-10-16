import os
import errno
import sys
import requests
import time
import uuid

from prism._utils.exceptions import PrismAuthError

from .._common.config import URL_WEB_AUTH, URL_DOC_AUTH, HEADERS, URL_REFRESH

def _authentication():
    global auth_token, refresh_token, access_token_time
    try:
        current_time = time.time()
        if globals().get('access_token_time') is None:
            raise PrismAuthError("Please Login First")
        if current_time - access_token_time > 1200:
            res = requests.post(url=URL_REFRESH, cookies={"refresh_token": refresh_token})
            _create_token(res)
        headers = HEADERS.copy()
        if 'auth_token' not in globals():
            raise PrismAuthError(f"Please Login First")
        token = auth_token
        headers.update({"Authorization": "Bearer {}".format(token)})
        req_id = str(uuid.uuid4())[:8]
        headers.update({"requestid": req_id})
    except FileNotFoundError:
        raise PrismAuthError(f"Please Login First")
    return headers


def _delete_token():
    global auth_token, refresh_token
    auth_token = ''
    refresh_token = ''


def _create_token(response: requests.models.Response):
    global auth_token, refresh_token, access_token_time
    token = response.json()["access_token"]
    ref_token = response.cookies.get("refresh_token")
    auth_token = token
    refresh_token = ref_token
    access_token_time = time.time()


def _find_file_path(file_name: str):
    sys.path.append(os.getcwd())
    for path in sys.path:
        if os.path.exists(path + "/" + file_name):
            return path + "/" + file_name
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_name)


class TokenDoesNotExistError(Exception):
    def __init__(self):
        super().__init__("You should first login to create a token")


def _get_web_authentication_token():
    headers = _authentication()
    res = requests.post(URL_WEB_AUTH, headers=headers)
    web_auth_token = res.json().get("access_token")
    return web_auth_token

def _get_document_authentication_token():
    headers = _authentication()
    res = requests.post(URL_DOC_AUTH, headers=headers)
    web_auth_token = res.json().get("access_token")
    return web_auth_token
