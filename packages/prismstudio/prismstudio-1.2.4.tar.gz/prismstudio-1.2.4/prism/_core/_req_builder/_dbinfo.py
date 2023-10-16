import json
import requests

import pandas as pd

from ..._common.config import *
from ..._common.const import *
from ..._utils import _validate_args, post, _authentication, _process_response


@_validate_args
def get_dbinfo(dbname: str):
    headers = _authentication()
    res = requests.get(url=URL_DBINFO + f'/{dbname}', headers=headers)
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(json.loads(res.content)['detail'])
    result = pd.DataFrame(list(json.loads(res['data']).items()), columns=['name', 'value'])
    return result


@_validate_args
def delete_dbinfo(dbname: str):
    headers = _authentication()
    query = {'dbname': dbname}
    """need revision res.ok?"""
    res = requests.delete(url=URL_DBINFO + f'/{dbname}', params=json.dumps(query), headers=headers,)
    return _process_response(res)


@_validate_args
def create_dbinfo(
    dbname: str,
    host: str,
    port: str,
    db: str,
    dbusername: str,
    dbpassword: str,
    dialect: str,
    vendor: str,
    priority: int,
):
    body = {
        'dbname': dbname,
        'host': host,
        'port': port,
        'db': db,
        'dbusername': dbusername,
        'dbpassword': dbpassword,
        'dialect': dialect,
        'vendor': vendor,
        'priority': priority,
    }
    return post(URL_DBINFO, None, body)


@_validate_args
def update_dbinfo(
    dbname: str = None,
    host: str = None,
    port: str = None,
    db: str = None,
    dbusername: str = None,
    dbpassword: str = None,
    dialect: str = None,
    vendor: str = None,
    priority: int = None,
):
    headers = _authentication()
    query = {
        'dbname': dbname,
        'host': host,
        'port': port,
        'db': db,
        'dbusername': dbusername,
        'dbpassword': dbpassword,
        'dialect': dialect,
        'vendor': vendor,
        'priority': priority,
    }
    res = requests.patch(url=URL_DBINFO + f'/{dbname}', data=json.dumps(query), headers=headers)
    return _process_response(res)
