from typing import Dict
from navconfig.logging import logging
from querysource.exceptions import DataNotFound as QSNotFound
from flowtask.exceptions import (ComponentError, DataNotFound)
from .QSBase import QSBase


class GoogleA4(QSBase):
    """GoogleA4

    Overview

           This component captures the data from the Google Analytics 4 API to be
           processed and stored in Navigator.

    .. table:: Properties
       :widths: auto

    +--------------+----------+-----------+-------------------------------------------------------+
    | Name         | Required | Summary                                                           |
    +--------------+----------+-----------+-------------------------------------------------------+
    | datalist     |   Yes    |  Method for reports                                               |
    +--------------+----------+-----------+-------------------------------------------------------+
    | subtask      |   Yes    |  Identifiers of property and metrics                              |
    +--------------+----------+-----------+-------------------------------------------------------+

    Return the list of arbitrary days

    """

    type = 'report'
    _driver = 'ga'
    _metrics: Dict = {
        "sessions": "sessions",
        "totalUsers": "total_users",
        "newUsers": "new_users",
        "engagedSessions": "engaged_users",
        "sessionsPerUser": "per_user"
    }

    async def report(self):
        try:
            resultset = await self._qs.report()
            result = []
            # TODO: making a better data-transformation
            for row in resultset:
                res = {}
                # res['property_id'] = self._kwargs['property_id']
                res['start_date'] = self._kwargs['start_date']
                res['end_date'] = self._kwargs['end_date']
                res['company_id'] = self._kwargs['company_id']
                res['dimension'] = self._kwargs['dimensions']
                if 'ga4_dimension' in self._variables:
                    res['ga4_dimension'] = self._variables['ga4_dimension']
                elif 'ga4_dimension' in self._kwargs:
                    res['ga4_dimension'] = self._kwargs['ga4_dimension']
                dimensions = {}
                for dimension in self._kwargs['dimensions']:
                    dimensions[dimension] = row[dimension]
                res['dimensions'] = dimensions
                metrics = {}
                for metric in self._kwargs['metric']:
                    metrics[metric] = row[metric]
                    try:
                        new_metric = self._metrics[metric]
                        res[new_metric] = row[metric]
                    except KeyError:
                        pass
                res['metric'] = metrics
                result.append(res)
            return result
        except QSNotFound as err:
            raise DataNotFound(
                f"GA4 Not Found: {err}"
            ) from err
        except Exception as err:
            logging.exception(
                err
            )
            raise ComponentError(
                f'Google Analytics 4 ERROR: {err!s}'
            ) from err
