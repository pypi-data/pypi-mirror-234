from finbourne_lab.common.recorder.sql_db import create_db_providers
from lumipy.provider import DType
from lumipy.client import Client
from typing import Literal


def make_recorder_providers(client: Client, action: Literal['create', 'recreate'] = 'create'):

    cols = [
        ('download_finish', DType.DateTime),
        ('download_time', DType.Decimal),
        ('end', DType.DateTime),
        ('error_message', DType.Text),
        ('errored', DType.Boolean),
        ('execution_id', DType.Text),
        ('get', DType.DateTime),
        ('name', DType.Text),
        ('obs_cols', DType.Decimal),
        ('obs_rows', DType.Decimal),
        ('query_time', DType.Decimal),
        ('run_id', DType.Text),
        ('send', DType.DateTime),
        ('start', DType.DateTime),
        ('start_query_time', DType.Decimal),
        ('submitted', DType.DateTime),
        ('prep_time', DType.Double),
        ('providers_time', DType.Double),
        ('mergesql_time', DType.Double),
        ('filltable_time', DType.Double),
        ('total_time', DType.Double),
    ]

    return create_db_providers(client, 'luminesce', cols, action)
