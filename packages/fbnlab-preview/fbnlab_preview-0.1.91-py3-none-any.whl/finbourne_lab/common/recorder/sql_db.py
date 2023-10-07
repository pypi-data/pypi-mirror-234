import json
from typing import List, Literal, Tuple

import lumipy as lm
import pandas as pd
from lumipy.lumiflex import DType

from finbourne_lab.common.recorder.base import BaseRecorder

from lumipy.client import Client
from lumipy.lumiflex._atlas.atlas import Atlas
import datetime as dt


def create_db_providers(
        client: Client,
        application: str,
        columns: List[Tuple[str, DType]],
        action: Literal['create', 'recreate'] = 'create'
) -> pd.DataFrame:
    """Creates a Sql.Db provider for a given application's experiments + a writer

    Args:
        client (Client): the lumipy client to use in the build query.
        application (str): the name of the application the experiments are run for.
        columns (List[Tuple(str, DType)]): the columns and types present in the recorded data.
        action (Literal['create', 'recreate]): whether to create or recreate the provider (defaults to create and will
        error if it already exists)

    Returns:
        DataFrame: pandas df containing the creation query result. Should have no rows but all the specified columns
        + an args_json column.
    """

    c_names = [c[0] for c in columns] + ['args_json']
    c_types = [c[1] for c in columns] + [DType.Text]

    select_cols_str = ',\n\t'.join([f'{{{c} : {c}}}' for c in c_names])
    upsert_cols_str = ',\n\t'.join([f'{{{c} : "{c}" = excluded."{c}"}}' for c in c_names])

    def type_str(x):
        if x in [DType.DateTime, DType.Date]:
            return 'TIMESTAMP NULL'

        if x == DType.Text:
            return 'CITEXT'

        if x == DType.Boolean:
            return 'BOOLEAN NULL'

        return 'NUMERIC NULL'

    provider_name = SqlDbRecorder._make_name(application)
    table_name = provider_name.replace('.', '_')

    # use Sql.Db with @{tv.meta_.name}
    creation_sql = f'''

        @x = use Sql.Db 
        --type=PostgreSql
        --connection=HoneycombDataStore
        --writerConnection=HoneycombDataStoreReadWrite
        --provider={provider_name}
        --licenceCode=honeycomb-standard-access
        --writerLicenceCode=honeycomb-admin-access
        --withWriter
        --commitEvery=10000
        -----------------
        SELECT
            #distinct
            #select
                 {{
                 {select_cols_str}               
                 }}
             FROM DataStoreDynamic.{table_name}
             WHERE
                 #restrict
                 {{
                 {select_cols_str}
                 }}
        #limit
        -----------------
        --upsert statement, take note of all the " needed to have Postgres not treat all column names as lowercase.  
        --Without that the resulting provider would have all lower case columns returned!
        INSERT INTO DataStoreDynamic.{table_name} (#INSERT_COLUMN_NAMES)
        VALUES (#INSERT_COLUMN_VALUES)
        ON CONFLICT ("execution_id", "name")
            DO UPDATE SET
            #UPDATE_COLUMN_ASSIGNMENTS
            {{
                 {upsert_cols_str}               
            }}
        -----------------
        -- if you change the structure a few times while working things out you might want this DROP statement in

    '''

    create_cols_str = ',\n\t'.join([f'"{n}" {type_str(t)}' for n, t in zip(c_names, c_types)])
    if action == 'create':
        creation_sql += f"""

        CREATE TABLE IF NOT EXISTS DataStoreDynamic.{table_name} (
            {create_cols_str}
        );
        CREATE UNIQUE INDEX IF NOT EXISTS xxx_yyy ON DataStoreDynamic.{table_name} ("execution_id", "name");

        """
    elif action == 'recreate':
        creation_sql += f"""
        DROP TABLE IF EXISTS DataStoreDynamic.{table_name};
        CREATE TABLE IF NOT EXISTS DataStoreDynamic.{table_name} (
            {create_cols_str}
        );
        CREATE UNIQUE INDEX IF NOT EXISTS xxx_yyy ON DataStoreDynamic.{table_name} ("execution_id", "name");
        """
    else:
        options = ', '.join(['create', 'recreate'])
        raise ValueError(f'Unsupported action: {action}. Valid options are {options}.')

    creation_sql += """
        enduse;
        select * from @x           
    """
    return client.run(creation_sql)


def alt_serialiser(obj):
    if isinstance(obj, (dt.datetime, dt.date, pd.Timestamp)):
        return obj.isoformat()
    return str(obj)


# noinspection SqlNoDataSourceInspection
class SqlDbRecorder(BaseRecorder):
    """Recorder class for recording to a Sql.Db writer provider.

    """

    @staticmethod
    def _make_name(application):
        return f'sys.finbourne.lab.{application}'

    def __init__(self, atlas: Atlas, application: str, chunk_size=5):
        """

        Args:
            atlas (Atlas): atlas to use when writing.
            application (str): name of the application being recorded.
            chunk_size (int): size of the chunk of data that triggers a write (default = 5)
        """
        self.atlas = atlas
        self.provider_name = self._make_name(application)
        try:
            self.db = self.atlas[self.provider_name]
            self.db_writer = self.atlas[self.provider_name + '.writer']
        except AttributeError:
            ValueError(f'Atlas did not contain {self.provider_name}* sql.db providers. '
                       f'If they do not exist yet use the DbRecorder.create_db_providers method to create them.')

        super().__init__(chunk_size)

    def _send(self, name: str) -> None:

        def consolidate_args(data):

            args = [c for c in data.columns if c.startswith('arg')]
            non_args = [c for c in data.columns if not c.startswith('arg')]

            to_send = data[non_args].copy()

            def json_str(r):
                d = {k: v.name if isinstance(v, DType) else v for k, v in r.to_dict().items()}
                return json.dumps(d, default=alt_serialiser)

            to_send['args_json'] = data[args].apply(json_str, axis=1)

            return to_send

        df = consolidate_args(pd.DataFrame(self.staging[name]))
        df = df[~pd.isna(df.execution_id)]
        tv = lm.from_pandas(df)
        q = self.db_writer(to_write=tv).select('*').limit(1)
        q.go_async()

    def get_df(self, name: str) -> pd.DataFrame:
        """Get the data recorded for a given experiment.

        Args:
            name (str): the experiment's name.

        Returns:
            DataFrame: a pandas dataframe with the experiment's data.
        """
        db = self.db()
        q = db.select('*').where(db.name == name)
        return q.go(quiet=True)
