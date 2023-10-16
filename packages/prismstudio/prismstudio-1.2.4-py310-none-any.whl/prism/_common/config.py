import pathlib
from enum import Enum
from pydantic import BaseSettings


class EnvironmentState(str, Enum):
    LOCAL = "local"
    DEVELOPMENT = "dev"
    STAGING = "stg"
    PRODUCTION = "production"
    DEMO = "demo"


class StateSettings(BaseSettings):
    ENV_STATE: str = 'production'
    VERSION: str
    URL_STABLE: str = 'https://api.prism39.com'
    URL_DEV: str = 'https://ops.prism39.com'
    dev: str = ':30495'
    stg: str = ':30496'
    demo: str = ':40452'

    class Config:
        p = pathlib.Path(__file__).parent.resolve()
        env_file = str(p) + '/.env'


class FactorySettings:
    @staticmethod
    def load():
        state = StateSettings()
        doc_url = 'help.prism39.com'
        ext_url = 'studio.prism39.com'
        if state.ENV_STATE == EnvironmentState.LOCAL:
            URL = "http://localhost:8000"
            doc_url = 'http://localhost:5500/doc/build'
            ext_url = "https://localhost:3000/ext"
        elif state.ENV_STATE == EnvironmentState.DEMO:
            URL = state.URL_STABLE + getattr(state, state.ENV_STATE)
            doc_url = f"https://{state.ENV_STATE}-help.prism39.com"
            ext_url = f"https://{state.ENV_STATE}-studio.prism39.com/ext"
        elif state.ENV_STATE in (EnvironmentState.DEVELOPMENT, EnvironmentState.STAGING):
            URL = state.URL_DEV + getattr(state, state.ENV_STATE)
            doc_url = f"https://{state.ENV_STATE}-help.prism39.com"
            ext_url = f"https://{state.ENV_STATE}-studio.prism39.com/ext"
        elif state.ENV_STATE == EnvironmentState.PRODUCTION:
            URL = state.URL_STABLE
            doc_url = "https://help.prism39.com"
            ext_url = "https://studio.prism39.com/ext"
        return URL, doc_url, ext_url


settings = FactorySettings.load()


__all__ = [
    'HEADERS',
    'URL_SERVICE',
    'URL_CATEGORYCOMPONENTS',
    'URL_DATACOMPONENTS',
    'URL_DATAQUERIES',
    'URL_TASKQUERIES',
    'URL_JOBS',
    'URL_PREFERENCES',
    'URL_PORTFOLIOS',
    'URL_UNIVERSES',
    'URL_DATAITEMS',
    'URL_FUNCTIONCOMPONENTS',
    'URL_PACKAGES',
    'URL_LOGIN',
    'URL_REFRESH',
    'URL_DBINFO',
    'URL_UPDATE',
    'URL_STATUS',
    'URL_TASK',
    'URL_VALIDATE',
    'URL_SM',
    'URL_WEB_AUTH',
    'URL_DOC_AUTH',
    'URL_STATIC',
    'URL_DATA_FILES',
    'ROOT_EXT_WEB_URL',
    'ROOT_DOCUMENT_URL',
    'URL_UPLOAD',
    "URL_IDS",
]

URL, ROOT_DOCUMENT_URL, ROOT_EXT_WEB_URL = settings

HEADERS = {'Content-Type': 'application/json; charset=utf-8', 'client': 'python'}

URL_SERVICE = URL + '/service'
URL_CATEGORYCOMPONENTS = URL + '/categorycomponents'
URL_DATAQUERIES = URL + '/dataqueries'
URL_DATACOMPONENTS = URL + '/datacomponents'
URL_TASKQUERIES = URL + '/taskqueries'
URL_JOBS = URL + '/jobs'
URL_PREFERENCES = URL + '/preference'
URL_UNIVERSES = URL + '/universes'
URL_PORTFOLIOS = URL + '/portfolios'
URL_IDS = URL + "/datacategorycomponentid"
URL_DATAITEMS = URL + '/dataitems'
URL_FUNCTIONCOMPONENTS = URL + '/functioncomponents'
URL_PACKAGES = URL + '/packages'
URL_LOGIN = URL + '/auth/login'
URL_REFRESH = URL + '/refresh_token'
URL_DBINFO = URL + '/dbinfo'
URL_UPDATE = URL + '/update'
URL_STATUS = URL + '/status'
URL_TASK = URL + '/task'
URL_VALIDATE = URL + '/validate'
URL_SM = URL + '/securitymaster'
URL_WEB_AUTH = URL + '/auth/web'
URL_DOC_AUTH = URL + '/auth/doc_web'
URL_STATIC = URL + '/static'
URL_UPLOAD = URL + '/upload'
URL_DATA_FILES = URL + '/datafiles'

_username = ''
# URL = 'https://api.prism39.com'
