import requests
import hashlib
import uuid

import prism
from ..._common.config import *
from ..._utils import _validate_args, _create_token, get, _delete_token
from ..._common import const

__all__ = ['login']


@_validate_args
def login(username: str = '', password: str = '', credential_file: str = ''):
    """
    Log in to PrismStudio.

    Parameters
    ----------
        username : str, default ''
            A string representing the username of the user.
        password : str, default ''
            A string representing the password of the user.
        credential_file : str, default ''
            | Provide credential text files.
            | The first line of the file should be username and the second line should be password.
            | Please provide either valid credential file or username and password pair.

    Returns
    -------
        str
            A string with a success message if the login is successful, or **None** if the login fails.
    """
    if (not (username and password)) and (not credential_file):
        print("Please provide valid credential!")
        return
    if credential_file:
        with open(credential_file, 'r') as f:
            username = f.readline().strip()
            password = f.readline().strip()
    password = hashlib.sha512(password.encode())
    password = password.hexdigest()
    query = {'username': username, 'password': password}
    req_id = str(uuid.uuid4())[:8]
    headers = {"client": "python", 'requestid': req_id}
    res = requests.post(url=URL_LOGIN, data=query, headers=headers)

    if res.ok:
        _create_token(res)
        smattributes = get(f'{URL_SM}/attributes')
        const.SMValues = {a['attributerepr']: a['attribute'] for a in smattributes}
        const.PreferenceType = get(f'{URL_PREFERENCES}/types')
        const.CategoryComponent = get(URL_CATEGORYCOMPONENTS)
        const.FunctionComponents = get(URL_FUNCTIONCOMPONENTS)
        const.DataComponents = get(URL_DATACOMPONENTS)
        prism.username = username
        result = f'Login success! Welcome {username}'
    else:
        _delete_token()
        print(f'\033[91mLogin Failed\033[0m: Please check your username and password')
        return

    return result
