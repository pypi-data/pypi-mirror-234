
from tests.test_util.utils import query_test

def test_model_query(tcmodel_quries, db_env):
    query_test(tcmodel_quries, db_env)
