# Import Config Class
import sys
from pathlib import Path
from typing import Any
from navconfig import BASE_DIR, DEBUG, config
from navconfig.logging import logger
from querysource.conf import CACHE_HOST, CACHE_PORT
from flowtask.utils.functions import get_worker_list
from flowtask.exceptions import FlowTaskError
from flowtask.tasks.storages import FileTaskStorage
from flowtask.tasks.files import FileStore


# Environment
ENVIRONMENT = config.get('ENVIRONMENT', fallback='development')
## environment name:
ENV = config.get('ENV', fallback='dev')

PRODUCTION = config.getboolean('PRODUCTION', fallback=(not DEBUG))
LOCAL_DEVELOPMENT = (DEBUG is True and sys.argv[0] == 'run.py')

APP_DIR = BASE_DIR.joinpath('flowtask')

# DB Default (database used for interaction (rw))
DBHOST = config.get('DBHOST', fallback='localhost')
DBUSER = config.get('DBUSER')
DBPWD = config.get('DBPWD')
DBNAME = config.get('DBNAME', fallback='navigator')
DBPORT = config.get('DBPORT', fallback=5432)
if not DBUSER:
    raise RuntimeError(
        'Missing PostgreSQL Default Settings.'
    )
# database for changes (admin)
default_dsn = f'postgres://{DBUSER}:{DBPWD}@{DBHOST}:{DBPORT}/{DBNAME}'
default_pg = f'postgres://{DBUSER}:{DBPWD}@{DBHOST}:{DBPORT}/{DBNAME}'

### InfluxDB configuration:
## INFLUXDB
USE_INFLUX = config.getboolean('USE_INFLUX', fallback=True)
INFLUX_DRIVER = config.get('INFLUX_DRIVER', fallback='influx')
INFLUX_HOST = config.get('INFLUX_HOST', fallback='127.0.0.1')
INFLUX_PORT = config.get('INFLUX_PORT', fallback='8086')
INFLUX_USER = config.get('INFLUX_USER')
INFLUX_PWD = config.get('INFLUX_PWD')
INFLUX_DATABASE = config.get('INFLUX_DATABASE', fallback='navigator')
INFLUX_TASKS_STARTED = config.get('INFLUX_TASKS_STARTED', fallback='started_tasks')
INFLUX_ORG = config.get('INFLUX_ORG', fallback='navigator')
INFLUX_TOKEN = config.get('INFLUX_TOKEN')
if USE_INFLUX is True and not INFLUX_TOKEN:
    raise FlowTaskError(
        'Missing InfluxDB Settings and Influx DB is enabled.'
    )

### Plugins Folder:
PLUGINS_FOLDER = BASE_DIR.joinpath('plugins')

# TEMPLATE SYSTEM
TEMPLATE_DIR = config.get(
    'TEMPLATE_DIR', fallback=BASE_DIR.joinpath('templates')
)

## Scheduler Configuration
# Schedule System
SCHEDULER = config.getboolean('SCHEDULER', fallback=True)
# Jobs Activation
ENABLE_JOBS = config.getboolean('ENABLE_JOBS', fallback=True)

SCHEDULER_MAX_INSTANCES = config.get('MAX_INSTANCES', fallback=2)
SCHEDULER_GRACE_TIME = config.get('GRACE_TIME', fallback=900)

# Timezone (For parsedate)
TIMEZONE = config.get(
    'timezone', section='l18n', fallback='UTC'
)
USE_TIMEZONE = config.getboolean('USE_TIMEZONE', fallback=True)

DEFAULT_TIMEZONE = config.get(
    'default_timezone', section='l18n', fallback='America/New_York'
)
SYSTEM_LOCALE = config.get(
    'locale', section='l18n', fallback='en_US.UTF-8'
)

"""
Worker Configuration
"""
WORKER_DEFAULT_HOST = config.get('WORKER_DEFAULT_HOST', fallback='0.0.0.0')
WORKER_DEFAULT_PORT = config.get('WORKER_DEFAULT_PORT', fallback=8888)
WORKER_DEFAULT_QTY = config.get('WORKER_DEFAULT_QTY', fallback=4)
WORKER_QUEUE_SIZE = config.get('WORKER_QUEUE_SIZE', fallback=4)
WORKER_REDIS_DB = config.get('WORKER_REDIS_DB', fallback=2)
WORKER_REDIS = f"redis://{CACHE_HOST}:{CACHE_PORT}/{WORKER_REDIS_DB}"
REDIS_CACHE_DB = config.get('REDIS_CACHE_DB', fallback=1)
REDIS_URL = f"redis://{CACHE_HOST}:{CACHE_PORT}/{REDIS_CACHE_DB}"

workers = config.get('WORKER_LIST')
if workers:
    WORKER_LIST = get_worker_list([e.strip() for e in list(workers.split(","))])
else:
    WORKER_LIST = None

workers_high = config.get('WORKER_HIGH_LIST', fallback='127.0.0.1:8899')
if workers_high:
    WORKER_HIGH_LIST = get_worker_list([e.strip() for e in list(workers_high.split(","))])
else:
    WORKER_HIGH_LIST = None

SCHEDULER_WORKER_TIMEOUT = config.getint(
    'SCHEDULER_WORKER_TIMEOUT', fallback=60
)
SCHEDULER_WORKER_RETRY_ENQUEUE = config.getint(
    'SCHEDULER_WORKER_RETRY_ENQUEUE',
    fallback=30
)

### Memcache
MEMCACHE_HOST = config.get('MEMCACHE_HOST', 'localhost')
MEMCACHE_PORT = config.get('MEMCACHE_PORT', fallback=11211)

### Redash System
REDASH_HOST = config.get('REDASH_HOST')
REDASH_API_KEY = config.get('REDASH_API_KEY')

"""
Notification System
"""
### Notification System
NOTIFY_ON_SUCCESS = config.get('DI_EVENT_ON_SUCCESS', fallback='dummy')
NOTIFY_ON_ERROR = config.get('DI_EVENT_ON_ERROR', fallback='dummy')
NOTIFY_ON_FAILURE = config.get('DI_EVENT_ON_FAILURE', fallback='dummy')
NOTIFY_ON_WARNING = config.get('DI_EVENT_ON_WARNING', fallback='dummy')

SEND_NOTIFICATIONS = bool(config.get('SEND_NOTIFICATIONS', fallback=True))
DEFAULT_RECIPIENT = {
    "name": "Jesus Lara",
    "account": {
        "address": "jesuslarag@gmail.com",
        "number": "+00000000"
    }
}

TELEGRAM_BOT_TOKEN = config.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = config.get('TELEGRAM_CHAT_ID')

EVENT_CHAT_BOT = config.get('EVENT_CHAT_BOT', fallback=TELEGRAM_BOT_TOKEN)
EVENT_CHAT_ID = config.get('EVENT_CHAT_ID', fallback=TELEGRAM_CHAT_ID)

# Notify on Slack
SLACK_DEFAULT_CHANNEL = config.get('SLACK_DEFAULT_CHANNEL')
SLACK_DEFAULT_CHANNEL_NAME = config.get('SLACK_DEFAULT_CHANNEL_NAME')

# this is the backend for saving task executions
USE_TASK_EVENT = config.getboolean('USE_TASK_EVENT', fallback=True)
# this is the backend for saving task executions
TASK_EXEC_BACKEND = config.get('TASK_EXEC_BACKEND', fallback='influx')
TASK_EVENT_TABLE = config.get('TASK_EVENT_TABLE', fallback='task_execution')
TASK_EXEC_TABLE = config.get('TASK_EXEC_TABLE', fallback='task_activity')

TASK_EXEC_CREDENTIALS = {
    "host": INFLUX_HOST,
    "port": INFLUX_PORT,
    "bucket": INFLUX_DATABASE,
    "org": INFLUX_ORG,
    "token": INFLUX_TOKEN
}

# Pub/Sub Channel:
PUBSUB_REDIS_DB = config.get('PUBSUB_REDIS_DB', fallback=5)
PUBSUB_REDIS = f"redis://{CACHE_HOST}:{CACHE_PORT}/{PUBSUB_REDIS_DB}"
ERROR_CHANNEL = config.get('ERROR_CHANNEL', fallback='FLOWTASK:FAILED:TASKS')
ALLOW_RESCHEDULE = config.getboolean('ALLOW_RESCHEDULE', fallback=False)

"""
Email Configuration
"""
# email:
EMAIL_USERNAME = config.get('sendgrid_user')
EMAIL_PASSWORD = config.get('sendgrid_password')
EMAIL_PORT = config.get('sendgrid_port', fallback=587)
EMAIL_HOST = config.get('sendgrid_host')
IMAP_RETRY_SELECT = config.getint('IMAP_RETRY_SELECT', fallback=3)

"""
MS Teams
"""
MS_TEAMS_NAVIGATOR_CHANNEL = config.get('MS_TEAMS_NAVIGATOR_CHANNEL', fallback='Navigator')
MS_TEAMS_NAVIGATOR_CHANNEL_ID = config.get('MS_TEAMS_NAVIGATOR_CHANNEL_ID')

"""
Resource Usage
"""
QUERY_API = config.getboolean('QUERY_API', fallback=True)
WEBSOCKETS = config.getboolean('WEBSOCKETS', fallback=True)
VARIABLES = config.getboolean('VARIABLES', fallback=True)
API_TIMEOUT = 36000  # 10 minutes
SEMAPHORE_LIMIT = config.get('SEMAPHORE_LIMIT', fallback=4096)
# upgrade no-files
NOFILES = config.get('ULIMIT_NOFILES', fallback=16384)

"""
Tasks and ETLs
"""
## Default Task Path
program = config.get('TASK_PATH')
if not program:
    TASK_PATH = BASE_DIR.joinpath('tasks', 'programs')
else:
    TASK_PATH = Path(program).resolve()

logger.debug(f'FlowTask Default Path: {TASK_PATH}')

TASK_STORAGES: dict[str, Any] = {
    "default": FileTaskStorage(path=TASK_PATH)
}

ETL_PATH = config.get('ETL_PATH')
FILES_PATH = Path(ETL_PATH).resolve()

FILE_STORAGES: dict[str, Any] = {
    "default": FileStore(path=FILES_PATH, prefix='files')
}

#################################################
### MarketPlace infraestructure:

MARKETPLACE_DIR = config.get('MARKETPLACE_DIR')
USE_SSL = config.getboolean("SSL", section="ssl", fallback=False)
if not MARKETPLACE_DIR:
    MARKETPLACE_DIR = BASE_DIR.joinpath('docs', 'plugins', 'components')

## Sign-in infraestructure
MARKETPLACE_PUBLIC_KEY = BASE_DIR.joinpath('docs', 'ssl', 'public_key.pem')
MARKETPLACE_CERTIFICATE = BASE_DIR.joinpath('docs', 'ssl', 'certificate.pem')
MARKETPLACE_PRIVATE_KEY = BASE_DIR.joinpath('docs', 'ssl', 'private_key.pem')


murl = 'http://nav-api.dev.local:5000/api/v1/marketplace/'
MARKETPLACE_URL = config.get(
    'MARKETPLACE_URL', fallback=murl
)

## PGP component:
# PGP Credentials
PGP_KEY_PATH = config.get('PGP_KEY_PATH')
PGP_PASSPHRASE = config.get('PGP_PASSPHRASE')

# JIRA:
JIRA_API_TOKEN = config.get('JIRA_API_TOKEN')
JIRA_USERNAME = config.get('JIRA_USERNAME')
JIRA_INSTANCE = config.get('JIRA_INSTANCE')
JIRA_PROJECT = config.get('JIRA_PROJECT')

# Zammad:
ZAMMAD_INSTANCE = config.get('ZAMMAD_INSTANCE')
ZAMMAD_TOKEN = config.get('ZAMMAD_TOKEN')
ZAMMAD_USER = config.get('ZAMMAD_USER')
ZAMMAD_PASSWORD = config.get('ZAMMAD_PASSWORD')
ZAMMAD_DEFAULT_GROUP = config.get('ZAMMAD_DEFAULT_GROUP')
ZAMMAD_DEFAULT_CUSTOMER = config.get('ZAMMAD_DEFAULT_CUSTOMER')

#####
try:
    from settings.settings import *  # pylint: disable=W0614,W0401
except ImportError as exc:
    logger.warning(
        f"Unable to load System Settings: {exc}"
    )
