import os

import pytest

from prism._utils.version import Version
from prism._common.config import StateSettings, ROOT_EXT_WEB_URL, URL


dotenv_settings = StateSettings()
_VERSION = dotenv_settings.VERSION # Version From DotEnv
_ENV_STATE = dotenv_settings.ENV_STATE

class TestVersion:
    version_instance = Version()
    env = os.environ.get('ENV_STATE', _ENV_STATE)

    def test_instance(self):
        assert self.version_instance is not None
        assert repr(self.version_instance) == f"<Version {_VERSION}-{self.env}>"

    def test_prism__version__(self):
        import prism
        assert "\n".join(
            [
                f"Version: {_VERSION}",
                f"Environment: {self.env}",
                f"API_URL: {URL}",
                f"GUI_URL: {ROOT_EXT_WEB_URL}",
            ]) == prism.__version__

    def test_version(self):
        assert _VERSION == self.version_instance.version

    def test_environment(self):
        assert self.version_instance.environment == self.env

    def test_environment_with_env(self, monkeypatch: pytest.MonkeyPatch):
        def test_load_setup(env):
            with monkeypatch.context() as monkey:
                monkey.setenv('ENV_STATE', env)
                _, loaded_env = self.version_instance.load_setup()
                return loaded_env

        for e in ['production', 'stg', 'dev']:
            assert e == test_load_setup(e)

        # production is converted to prod
        assert 'production' == test_load_setup('production')


    def test_urls(self):
        assert 'http' in self.version_instance.api_url
        assert 'http' in self.version_instance.gui_url
        assert URL == self.version_instance.api_url
        assert ROOT_EXT_WEB_URL == self.version_instance.gui_url