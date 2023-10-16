# -*- coding: utf-8 -*-
#
import os
import re
import datetime
from datetime import timedelta
import time
import traceback
import numbers
import hashlib
import binascii
import ast
from decimal import Decimal
from urllib.parse import urlparse
import dateparser
import pytz
import pandas as pd
import requests
from dateutil import parser
from dateutil.relativedelta import relativedelta
from pytz import timezone
from flowtask.types import strtobool


def _escapeString(value):
    v = value if value != 'None' else ""
    v = str(v).replace("'", "''")
    v = "'{}'".format(v) if isinstance(v, str) else v
    return v


def _parseString(value):
    if str(value).startswith("'"):
        return value[value.startswith('"') and len('"'):-1]
    else:
        return value

def _quoteString(value):
    v = value if value != 'None' else ""
    if isinstance(v, str):
        if v.startswith("'"):  # is already quoted
            return v
        elif v.startswith('"'):  # is double quoted
            return v.replace('"', "'")
        else:
            return "'{}'".format(v)
    else:
        return v


def uri_exists(uri):
    """uri_exists.
    Check if an URL is reachable.
    """
    path = urlparse(uri)
    url = f'{path.scheme!s}://{path.netloc!s}'
    response = requests.get(url, stream=True, timeout=5)
    if response.status_code == 200:
        return True
    else:
        return False

"""
 hash utilities.
"""
def get_hash(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()

"""
Date and Time utilities
"""
def current_year():
    return datetime.datetime.now().year


def previous_year():
    return (datetime.datetime.now() - timedelta(weeks=52))


def previous_month(mask="%m/%d/%Y"):
    return (datetime.datetime.now() - relativedelta(months=1)).strftime(mask)


def current_month():
    return datetime.datetime.now().month


def today(mask="%m/%d/%Y", zone: str = None):
    try:
        if zone is not None:
            tz = timezone(zone)
            a = datetime.datetime.now(tz).strftime(mask)
            print('CALCULATED DATE: ', a)
            return a
        else:
            return time.strftime(mask)
    except Exception as err:
        print(err)
        raise


def midnight(mask="%m/%d/%Y"):
    midnight = datetime.datetime.combine(datetime.datetime.now(), datetime.datetime.min.time())
    return midnight.strftime(mask)


def current_midnight(mask="%Y-%m-%dT%H:%M:%S"):
    midnight = datetime.datetime.combine(
        datetime.datetime.now(), datetime.datetime.min.time()
    )
    return midnight.strftime(mask)


def current_timestamp(mask="%Y-%m-%dT%H:%M:%S", tz: str = None):
    if tz is not None:
        zone = timezone(tz)
        return datetime.datetime.now(zone).strftime(mask)
    else:
        return datetime.datetime.now().strftime(mask)


def current_date(mask="%m/%d/%Y", tz: str = None):
    try:
        if tz is not None:
            zone = timezone(tz)
            a = datetime.datetime.now(zone).strftime(mask)
            print('CALCULATED DATE: ', a)
            return a
        else:
            return time.strftime(mask)
    except Exception as err:
        print(err)
        raise


def date_after(mask="%m/%d/%Y", offset=1):
    return (datetime.datetime.now() + timedelta(seconds=offset)).strftime(mask)


def date_ago(mask="%m/%d/%Y", offset=1):
    try:
        offset = int(offset)
    except Exception as err:
        print(err)
        offset = 1
    return (datetime.datetime.now() - timedelta(seconds=offset)).strftime(mask)


def days_ago(mask="%m/%d/%Y", offset=1):
    try:
        offset = int(offset)
    except Exception as err:
        print(err)
        offset = 1
    return (datetime.datetime.now() - timedelta(days=offset)).strftime(mask)


def format_date(value, mask="%Y-%m-%d"):
    if value == 'current_date' or value == 'now':
        value = datetime.datetime.now()
    elif isinstance(value, datetime.datetime):
        return value.strftime(mask)
    else:
        try:
            d = datetime.datetime.strptime(str(value), "%Y-%m-%d")
            return d.strftime(mask)
        except (TypeError, ValueError) as err:
            print(err)
            raise ValueError(err)


def date_diff(value, diff: int = 1, mode: str = 'days', mask="%Y-%m-%d"):
    if value == 'current_date' or value == 'now':
        value = datetime.datetime.now()
    tp = {
        mode: int(diff)
    }
    delta = timedelta(**tp)
    if delta:
        return (value - delta).strftime(mask)


def first_day_of_month(mask='%Y-%m-%d'):
    return datetime.datetime.now().replace(day=1).strftime(mask)


def yesterday(mask='%Y-%m-%d'):
    return (datetime.datetime.now() - timedelta(1)).strftime(mask)


def yesterday_timestamp(mask="%Y-%m-%dT%H:%M:%S"):
    return (datetime.datetime.now() - timedelta(1)).strftime(mask)


def midnight_yesterday(mask="%m/%d/%Y"):
    midnight = datetime.datetime.combine(
        datetime.datetime.now() - timedelta(1), datetime.datetime.min.time()
    )
    return midnight.strftime(mask)


def yesterday_midnight(mask="%Y-%m-%dT%H:%M:%S"):
    midnight = datetime.datetime.combine(
        datetime.datetime.now() - timedelta(1), datetime.datetime.min.time()
    )
    return midnight.strftime(mask)


def tomorrow(mask='%Y-%m-%d'):
    return (datetime.datetime.now() + timedelta(1)).strftime(mask)


def midnight_tomorrow(mask="%m/%d/%Y"):
    midnight = datetime.datetime.combine(
        datetime.datetime.now() + timedelta(1), datetime.datetime.min.time()
    )
    return midnight.strftime(mask)


def date_dow(day_of_week='monday', mask='%Y-%m-%d'):
    try:
        dows = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2,
            'thursday': 3, 'friday': 4, 'saturday': 5,
            'sunday': 6
        }
        today = datetime.datetime.now()
        dw = today.weekday()
        dow = today - timedelta(days=(dw - dows[day_of_week]))
        return dow.strftime(mask)
    except Exception:
        return None


def date_diff_dow(diff=0, day_of_week='monday', mask='%Y-%m-%d'):
    try:
        dows = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2,
            'thursday': 3, 'friday': 4, 'saturday': 5,
            'sunday': 6
        }
        today = datetime.datetime.now()
        dw = today.weekday()
        dow = today - timedelta(days=(dw - dows[day_of_week]))
        delta = dow - timedelta(days=(diff))
        return delta.strftime(mask)
    except Exception:
        return None

def fdom():
    return (datetime.datetime.now()).strftime("%Y-%m-01")


def ldom():
    return (datetime.datetime.now() + relativedelta(day=31)).strftime("%Y-%m-%d")


def first_dow(mask='%Y-%m-%d'):
    today = datetime.datetime.now()
    fdow = (today - timedelta(today.weekday()))
    return fdow.strftime(mask)


def now():
    return datetime.datetime.now()


def due_date(days=1):
    return datetime.datetime.now() + timedelta(days=days)


def to_midnight(value, mask='%Y-%m-%d'):
    midnight = datetime.datetime.combine(
        (value + timedelta(1)), datetime.datetime.min.time()
    )
    return midnight.strftime(mask)


def epoch_to_date(value):
    if value:
        s, ms = divmod(value, 1000.0)
        return datetime.datetime.fromtimestamp(s, pytz.utc)
    else:
        return None

def year(value=''):
    if value:
        try:
            newdate = parser.parse(value)
            return newdate.date().year
        except ValueError:
            dt = value[:-4]
            dt = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
            return dt.date().year
    else:
        return None


def month(value=''):
    if value:
        try:
            newdate = parser.parse(value)
            return newdate.date().month
        except ValueError:
            dt = value[:-4]
            dt = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
            return dt.date().month
    else:
        return None

def to_date(value=None, mask="%Y-%m-%d %H:%M:%S", tz=None):
    if isinstance(value, datetime.datetime):
        # print('to_date 1', value)
        return value
    else:
        try:
            result = datetime.datetime.strptime(str(value), mask)
            if tz is not None:
                result = result.replace(tzinfo=pytz.timezone(tz))
            # print('to_date 2', value, result)
            return result
        except Exception:
            # print('to_date 3', 'dateparser')
            return dateparser.parse(str(value), languages=['en', 'es'])


def to_time(value, mask="%H:%M:%S"):
    if value == 0:
        return datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if isinstance(value, datetime.datetime):
        return value
    else:
        if len(str(value)) < 6:
            value = str(value).zfill(6)
        try:
            return datetime.datetime.strptime(str(value), mask)
        except ValueError:
            return datetime.datetime.strptime(str(value), "%H:%M:%S")


def build_date(value, mask="%Y-%m-%d %H:%M:%S"):
    if isinstance(value, list):
        dt = to_date(value[0], mask=mask[0])
        mt = to_time(value[1], mask=mask[1]).time()
        return datetime.datetime.combine(dt, mt)
    elif isinstance(value, datetime.datetime):
        return value
    else:
        if value == 0:
            return datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            return datetime.datetime.strptime(str(value), mask)

"""
 Numeric Functions.
"""

def truncate_decimal(value=''):
    print(value, type(value), isinstance(value, str))
    if isinstance(value, numbers.Number):
        head, sep, tail = value.partition('.')
        return head
    elif isinstance(value, str):
        try:
            val = float(value)
            head, sep, tail = value.partition('.')
            return head
        except Exception:
            return None
    else:
        return None


def to_percent(value):
    return round(float(value) * 100.0, 2)


def to_round(number='', ndigits=0):
    if isinstance(number, numbers.Number):
        return round(number, ndigits)
    elif number is not None:
        try:
            return round(float(number), ndigits)
        except Exception as err:
            return None
    else:
        return None

def to_integer(value):
    if not value:
        return 0
    try:
        return int(value)
    except ValueError:
        return None

def to_boolean(value):
    if isinstance(value, bool):
        return value
    elif value is None:
        return False
    elif value == 'null' or value == 'NULL':
        return False
    else:
        return strtobool(value)


def to_double(value):
    if isinstance(value, int):
        return float(value)
    elif "," in value:
        val = value.replace(",", ".")
    else:
        val = value
    try:
        return float(val)
    except (ValueError, TypeError) as err:
        print(err)
        try:
            return Decimal(val)
        except Exception as e:
            print(e)
            return None

def trim(value):
    if isinstance(value, str):
        return value.strip()
    else:
        return value

"""
 Filename Operations.
"""

def filename(path):
    return os.path.basename(path)


def file_extension(path):
    return os.path.splitext(os.path.basename(path))[1][1:].strip().lower()


"""
 Other Utilities.
"""
def extract_path(value, regex, to_date=False, to_datetime=False, mask="%m/%d/%Y"):
    p = re.compile(regex)
    if p:
        try:
            found = re.search(regex, value)
            result = found.group(1)
            if to_date:
                result = datetime.datetime.strptime(result, mask).date()
            if to_datetime:
                result = datetime.datetime.strptime(result, mask)
            return result
        except Exception as err:
            print(err)
            return None
    else:
        return None

# others:
def extract_string(value, exp=r"_((\d+)_(\d+))_", group=1, parsedate=False, masks=["%Y-%m-%d %H:%M:%S"]):
    match = re.search(r"{}".format(exp), value)
    if match:
        result = match.group(group) if not parsedate else dateparser.parse(
            match.group(group), date_formats=masks, languages=['en', 'es']
        )
        return result

def get_environment(env, key=None, default=''):
    value = env.get(key)
    return value if value is not None else default


def convert(value, env=None, escape=False):
    if isinstance(value, list):
        try:
            func = value[0]
            try:
                kwargs = value[1]
            except IndexError:
                kwargs = None
            if kwargs:
                if env is not None:
                    kwargs['env'] = env
                try:
                    try:
                        return globals()[func](**kwargs)
                    except Exception:
                        if env is not None:
                            del kwargs['env']
                        return globals()[func](**kwargs)
                except (TypeError, ValueError) as err:
                    print('Convert Error:', err)
                    print(traceback.format_exc())
                    return ''
            else:
                try:
                    return globals()[func]()
                except (TypeError, ValueError):
                    return ''
        except (NameError, KeyError) as err:
            print('Convert Error: ', err)
            print(traceback.format_exc())
            return ''
    else:
        if isinstance(value, str):
            if escape:
                return f"'{str(value)}'"
            else:
                return f"{str(value)}"
        return value


def is_boolean(value: str) -> bool:
    if isinstance(value, bool):
        return value
    try:
        return ast.literal_eval(value)
    except ValueError:
        return False


def check_empty(obj):
    """check_empty.
    Check if a basic object is empty or not.
    """
    if isinstance(obj, pd.DataFrame):
        return True if obj.empty else False
    else:
        return bool(not obj)

is_empty = check_empty


def as_boolean(value: str) -> bool:
    """as_boolean.

    Converting any value to a boolean.
    """
    if isinstance(value, bool):
        return value
    try:
        return ast.literal_eval(value)
    except ValueError:
        return False
