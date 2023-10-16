import time
import uuid

import numpy as np
import pandas as pd
from urllib3 import HTTPResponse


def make_request(i, app_name):
    """

    Args:
        i:
        app_name:

    Returns:
        HTTPResponse:

    """

    t = i + 500 + np.random.normal(0, 0.01)
    time.sleep(t/1000 + abs(np.random.normal(0, 0.05)))

    return HTTPResponse(
        body='{"a":"b"}',
        headers=[
            (f'{app_name}-meta-requestId', f'request_{i}'),
            (f'{app_name}-meta-success', 'true'),
            (f'{app_name}-meta-duration', str(int(t))),
        ]
    )


class MockQuery:
    """

    """

    def __init__(self, x):
        """

        Args:
            x:
        """
        self.x = x
        self.call_count = 0

    def go_async(self, **kwargs):
        """

        Args:
            **kwargs:

        Returns:

        """
        self.call_count += 1
        status = 'Faulted' if self.x < 1 else 'WaitingForActivation'
        return MockQueryJob(self, status)

    def result(self, quiet=False):
        """

        Args:
            quiet:

        Returns:

        """
        rows = [{'A': i, 'B': i**2, 'C': i**0.5} for i in range(self.x)]
        if self.x < 1:
            raise ValueError("This is a test error")

        return pd.DataFrame(rows)

    def get_sql(self):
        """

        Returns:

        """
        return f"select * from mock.provider limit {self.x}"

    @staticmethod
    def build(x):
        """

        Args:
            x:

        Returns:

        """
        return MockQuery(x)


class MockQueryJob:
    """

    """

    def __init__(self, mock_query: MockQuery, status):
        """

        Args:
            mock_query:
            status:

        """
        self.mock_query = mock_query
        self.ex_id = str(uuid.uuid4())
        self._status = status
        self._progress_lines = ["This is a test error"]

    def interactive_monitor(self, quiet=False, wait=0.1, should_stop=None):
        """

        Args:
            quiet:
            wait:
            should_stop:

        Returns:

        """
        time.sleep(1)

    def get_result(self, quiet=False):
        """

        Args:
            quiet:

        Returns:

        """
        return self.mock_query.result()

    def get_progress(self):
        return '''
        FROM
   [Sys.Finbourne.Lab.Luminesce]
GROUP BY
   [name], [errored], date([start])
ORDER BY
   [name] ASC, [start] ASC
Rows         : 162
Data Volume  : 12439 B
Prep         : 207.5345 ms
Providers    : 1150.7677 ms
Merge/Sql    : 0.1951 ms
FillTable    : 548.8983 ms
(total)      : 1907.3956 ms
Session Id   : ae8d941a-7f9a-47e1-aed0-4ad439a8d030
Execution Id : 9f1653e4-26fe-4d94-8882-bb927666ddbc
Ext. Ex. Id  : 0HMRJ2GO4B0EF:00000071
Client       : fbn-ci
Client Id    : 0oa7draltjzKvjCz92p7
User Id      : 00u4edufouxFGBrcN2p7
Api Version  : 1.13.10.0
Dependency & Execution details:
.                           |208ms|                        1.315s||          1.907s|
Sys.Finbourne.Lab.Luminesce |     |>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>||                | -> 29024 row(s)
Query Coordinator           |*****|-------------------------------|>>>>>>>>>>>>>>>>| -> 162 row(s)
        '''
