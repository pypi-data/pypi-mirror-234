from finbourne_lab.luminesce import make_shopper, make_recorder_providers
from finbourne_lab import Convener, FileRecorder, DriveRecorder, SqlDbRecorder
import lumipy as lm
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='description')

    parser.add_argument(
        '--secrets_path',
        dest='secrets_path',
        default=None,
        help='The path to your luminesce secrets json file. Optional, but if not used auth will fall back on env vars'
    )
    parser.add_argument(
        '--record_to',
        dest='record_to',
        default='sql.db',
        help='''
        The place to record data to. If equal to "none", no data is recorded. If equal to "sql.db" then data are recorded
        to sys.finbourne.lab.luminesce (default). Otherwise, if it's a path starting with "drive:" it will record to a location
        in lusid drive if not it will record to a local directory. 
        '''
    )
    parser.add_argument(
        '--n_parallel',
        dest='n_parallel',
        default=1,
        help='The number of parallel shoppers to run at once. Defaults to one.',
        type=int
    )
    parser.add_argument(
        '--run_time',
        dest='run_time',
        default=None,
        help='The time to run for in seconds, if None it will run forever. Defaults to None.',
        type=int
    )
    parser.add_argument(
        '--ensure_sql_db',
        dest='ensure_sql_db',
        action='store_true',
        help='Whether to ensure the lumishopper sql db exists.',
    )

    args = parser.parse_args()

    client = lm.get_client(api_secrets_filename=args.secrets_path)
    token = client.get_token()
    api_url = client._factory.api_client.configuration._base_path
    atlas = lm.get_atlas(token=token, api_url=api_url, app_name='lumishopper')

    if args.ensure_sql_db:
        if hasattr(atlas, 'sys_finbourne_lab_luminesce_writer') and hasattr(atlas, 'sys_finbourne_lab_luminesce'):
            print('Sql.Db providers already set up.')
        else:
            print('Setting up Sql.Db providers')
            make_recorder_providers(client)

    print('Starting lumishopper')
    record_to = args.record_to
    print(f'Recording to {record_to}')
    if record_to.lower() == 'none':
        recorder = None
    elif record_to.lower() == 'sql.db':
        recorder = SqlDbRecorder(atlas, 'luminesce')
    elif record_to.lower().startswith('drive:'):
        recorder = DriveRecorder(atlas, record_to.replace('drive:', '').replace('Drive:', ''))
    else:
        recorder = FileRecorder(record_to)

    print('Creating lumishopper instance')
    shopper = make_shopper(atlas)

    print(f'Running lumishopper (n_parallel = {args.n_parallel})')
    print(repr(shopper))

    c = Convener(shopper, recorder, args.n_parallel)
    t = args.run_time
    c.go(t)
