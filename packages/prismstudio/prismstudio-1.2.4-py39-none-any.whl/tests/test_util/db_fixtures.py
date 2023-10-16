import pytest


from tests.test_util.utils import get_secret
from sqlalchemy import create_engine


TEST_DB_NAME = "testcase"


@pytest.fixture(autouse=True)
def db_env():
    test_db = get_secret("testdb")
    test_db['dbname'] = TEST_DB_NAME
    url = 'postgresql://{}:{}@{}:{}/{}'.format(test_db['username'], test_db['password'], test_db['host'], test_db['port'], test_db['dbname'])
    engine = create_engine(url)

    yield engine

    engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def prism():
    import prism
    prism.login("superuser", "L:3v[5a:mv8,z3Cf")
    return prism
