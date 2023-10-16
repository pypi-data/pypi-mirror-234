# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

import re
import boto3
import orjson
from sqlalchemy import select
from botocore.exceptions import ClientError

from tests.test_util.dq_model import PrismQuery
from tests.test_util.dq_table import dataqueries


def query_test(queries, engine):
    for k, v in queries.items():
        dq = engine.execute(select(dataqueries.c.dataquerybody).where(dataqueries.c.dataqueryname == k)).fetchone()
        cross_check(v._query, dq[0])


def get_secret(secret_name):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="ap-northeast-2"
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    return orjson.loads(secret)


def replace_nodeid(json_string):
    regex = ',[ ]?"nodeid":[ ]?"[^,]*"'
    replace = ''
    tmp = re.sub(regex, replace, json_string)
    regex = '"nodeid":[ ]?"[^\}\],]*",'
    tmp = re.sub(regex, replace, tmp)
    regex = ', "nodeid":[ ]?"[^\}\],]*"'
    tmp = re.sub(regex, replace, tmp)
    regex = ',[ ]?"nodeid":[ ]?null'
    return re.sub(regex, replace, tmp)


def cross_check(raw_ext_query, be_query):
    ext_query = orjson.loads(replace_nodeid(PrismQuery(**raw_ext_query).json()))
    be_query = orjson.loads(replace_nodeid(be_query))
    assert ext_query == be_query