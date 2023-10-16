"""
NavScheduler.

Job for attaching tasks to the Scheduler.
"""
import asyncio
import locale
import os
import socket
import sys
import traceback
import zoneinfo
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor as ThreadExecutor
from datetime import datetime, timedelta
from functools import partial
from redis import asyncio as aioredis
from aiohttp import web
from apscheduler.events import (
    EVENT_JOB_ADDED,
    EVENT_JOB_ERROR,
    EVENT_JOB_EXECUTED,
    EVENT_JOB_MAX_INSTANCES,
    EVENT_JOB_MISSED,
    EVENT_JOB_SUBMITTED,
    EVENT_SCHEDULER_SHUTDOWN,
    EVENT_SCHEDULER_STARTED,
    JobExecutionEvent
)
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.executors.debug import DebugExecutor
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.base import ConflictingIdError, JobLookupError
# Jobstores
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.redis import RedisJobStore
# apscheduler library  #
# Default Scheduler:
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger, OrTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
# Triggers
from apscheduler.triggers.interval import IntervalTrigger
# navconfig
from navconfig import config as navConfig
from navconfig.logging import logging
# asyncdb:
from asyncdb import AsyncDB
from navigator.connections import PostgresPool
from querysource.types.validators import Entity

# Queue Worker Client:
from qw.client import QClient
# dataintegration
from flowtask.conf import (
    CACHE_HOST, CACHE_PORT,
    ENABLE_JOBS, ENVIRONMENT,
    SCHEDULER_GRACE_TIME, SCHEDULER_MAX_INSTANCES,
    SYSTEM_LOCALE, TIMEZONE, WORKER_HIGH_LIST,
    WORKER_LIST, default_dsn,
    USE_TIMEZONE,
    PUBSUB_REDIS,
    ERROR_CHANNEL,
    ALLOW_RESCHEDULE
)
from flowtask.utils.json import json_decoder
# Handler
from .handlers import SchedulerManager
from .notifications import send_notification
from .functions import TaskScheduler, get_function


# disable logging of APScheduler
logging.getLogger('apscheduler').setLevel(logging.WARNING)


jobstores = {
    'default': MemoryJobStore(),
    'db': RedisJobStore(
        db=3,
        jobs_key='apscheduler.jobs',
        run_times_key='apscheduler.run_times',
        host=CACHE_HOST,
        port=CACHE_PORT
    )
}

job_defaults = {
    'coalesce': True,
    'max_instances': SCHEDULER_MAX_INSTANCES,
    'misfire_grace_time': SCHEDULER_GRACE_TIME
}

class NavScheduler:
    """NavScheduler.

    Demonstrates how to use the asyncio compatible scheduler to schedule jobs.
    """
    def __init__(self, event_loop=None):
        self.db = None
        self._pool = None
        self._connection = None
        self._jobs: dict = {}
        self._loop = None
        self.scheduler = None
        self._args = None
        self._event = asyncio.Event()
        if event_loop:
            self._loop = event_loop
        else:
            try:
                self._loop = asyncio.get_running_loop()
            except RuntimeError:
                self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        # logging
        self.logger = logging.getLogger(name='Flowtask.Scheduler')
        # asyncio scheduler
        self._timezone = zoneinfo.ZoneInfo(TIMEZONE)
        self.scheduler = AsyncIOScheduler(
            jobstores=jobstores,
            executors={
                'default': AsyncIOExecutor(),
                'process': ProcessPoolExecutor(max_workers=512),
                'thread': ThreadPoolExecutor(max_workers=512),
                'debug': DebugExecutor()
            },
            job_defaults=job_defaults,
            timezone=self._timezone
        )
        # defining Locale
        try:
            locale.setlocale(locale.LC_ALL, SYSTEM_LOCALE)
        except locale.Error as e:
            self.logger.exception(e, exc_info=True)

    def setup(self, app: web.Application):
        self.db = PostgresPool(
            dsn=default_dsn,
            name='FlowTask.Scheduler',
            startup=self.startup
        )
        self.db.configure(app, register='database')  # pylint: disable=E1123
        # add the scheduler to the current app
        app['scheduler'] = self
        # add the routes:
        app.router.add_view(
            '/api/v2/scheduler', SchedulerManager
        )
        app.router.add_view(
            '/api/v2/scheduler/{job}', SchedulerManager
        )
        app.on_startup.append(
            self.start_subscriber
        )
        app.on_cleanup.append(
            self.stop_subscriber
        )

    async def start_subscriber(self, app):
        self._redis = await aioredis.from_url(
            PUBSUB_REDIS,
            encoding="utf-8",
            decode_responses=True
        )
        ## listen subscriber:
        app['redis_listener'] = asyncio.get_event_loop().create_task(
            self.listen_task_events()
        )

    async def stop_subscriber(self, app):
        try:
            self.logger.notice("Stopping subscriber")
            self._event.set()
            app['redis_listener'].cancel()
        finally:
            await self._redis.close()
            try:
                await self._redis.connection_pool.disconnect()
            except Exception:
                pass

    async def listen_task_events(self):
        try:
            async with self._redis.pubsub() as pubsub:
                await pubsub.subscribe(ERROR_CHANNEL)
                future = asyncio.create_task(
                    self.event_reader(pubsub)
                )
                await future
        except Exception as exc:
            print(exc)

    async def event_reader(self, channel: aioredis.client.PubSub):
        try:
            while not self._event.is_set():
                msg = await channel.get_message(ignore_subscribe_messages=True)
                if msg is not None:
                    message = json_decoder(msg['data'])
                    self.logger.error(
                        f"Received Signal for Failed Task: {msg}"
                    )
                    status = message.get('status', 'error')
                    task = message.get('task', None)
                    if status != 'task not found':
                        self.process_failed_task(task)
        except Exception as err:
            self.logger.warning(
                f"Error reading from Task Event Subscription {err}"
            )
        finally:
            await channel.unsubscribe(ERROR_CHANNEL)

    def process_failed_task(self, task_name: str):
        program, task = task_name.split('.')
        job_id = f"{program}_{task}"
        try:
            info = self._jobs[job_id]
            job_info = info.get('data', None)
            if job_info:
                if ALLOW_RESCHEDULE is True and job_info['reschedule'] is True:
                    # Task was dispatched by me?
                    if self._jobs[job_id]['status'] != 'dispatched':
                        # This task was not dispatched by me, returning
                        return
                    # Jitter for re-scheduling in minutes
                    jitter = job_info['reschedule_jitter']
                    job = self.scheduler.get_job(job_id)
                    old_trigger = job.trigger
                    self._jobs[job_id]['trigger'] = old_trigger
                    job.reschedule(
                        trigger=IntervalTrigger(minutes=jitter)
                    )
                    self.logger.warning(
                        f"Job {job_id} was re-scheduled to {jitter} minutes."
                    )
        except KeyError:
            self.logger.warning(
                f"Job with id {job_id} does not exist on Jobstore"
            )

    async def startup(self, app: web.Application, conn: Callable):
        """
        Scheduler Startup.
        """
        try:
            self._pool = conn
        except Exception as err:
            self.logger.exception(err)
            raise RuntimeError(
                f"{err!s}"
            ) from err
        # auxiliary connection
        if self._pool:
            self._connection = await self._pool.acquire()
        ## getting workers:
        if WORKER_LIST:
            self.qworker = QClient(
                worker_list=WORKER_LIST
            )
            self.qworker_high = QClient(
                worker_list=WORKER_HIGH_LIST
            )
        else:
            self.qworker = QClient()  # auto-discovering of workers
            self.qworker_high = self.qworker
        # getting Jobs
        await self.create_jobs()
        # adding listeners
        self.add_listeners()
        self.logger.info(
            f"Scheduled Started at {datetime.now()}"
        )
        try:
            # starting scheduler
            self.scheduler.start()
        except Exception as err:
            raise RuntimeError(
                f'Error Starting Scheduler {err!r}'
            ) from err
        # set Zoneinfo:
        if USE_TIMEZONE is True:
            tz = f"SET timezone TO '{TIMEZONE}'"
            await self._connection.execute(tz)
        ## Add Scheduler to Application:
        app['_scheduler_'] = self.scheduler

    @property
    def event_loop(self):
        return self._loop

    def set_test_job(self):
        self.logger.debug(
            'Scheduler: Adding a Test job'
        )
        run_date = datetime.now(self._timezone) + timedelta(minutes=1)
        # define Task:
        program = 'navigator'
        task = 'startup_job'
        sched = TaskScheduler(
            program,
            task,
            worker=self.qworker
        )
        sched.__class__.__name__ = f'Task({program}.{task})'
        self.scheduler.add_job(
            sched,
            id='on_startup_job',
            name='startup_test_job',
            logger=self.logger,
            jobstore_retry_interval=30,
            jobstore='default',
            executor='default',
            trigger=DateTrigger(
                run_date=run_date,
                timezone=self._timezone
            ),
            replace_existing=True,
            remove_job_on_completion=True
        )

    async def create_jobs(self):
        self._jobs = {}
        if ENABLE_JOBS is True:
            # Job for self-service discovering
            sql_jobs = 'SELECT * FROM troc.jobs WHERE enabled = true'
            jobs, error = await self._connection.query(sql_jobs)
        else:
            jobs = []
            error = None
        if error:
            raise RuntimeError(
                f'[{ENVIRONMENT} - Scheduler] Error getting Jobs: {error!s}'
            )
        # Add a Job for testing purposes.
        self.set_test_job()
        for job in jobs:
            jitter = None
            job_id = job['job_id']
            if job['jitter']:
                jitter = job['jitter']
            # function or other call
            priority = job.get('priority', 'low')
            if priority == 'high':
                worker = self.qworker_high
            else:
                worker = self.qworker
            func = get_function(job, priority=priority, worker=worker)
            schedule_type = job['schedule_type']
            self.logger.debug(
                f"Created new Job {job_id} with {func!s} and schedule: {schedule_type}"
            )
            if schedule_type == 'interval':
                t = job['schedule']
                if job['start_date']:
                    t = {
                        **t,
                        **{"start_date": job['start_date']}
                    }
                if job['end_date']:
                    t = {
                        **t,
                        **{"end_date": job['end_date']}
                    }
                trigger = IntervalTrigger(**t)
            elif schedule_type == 'crontab':
                t = job['schedule']['crontab']
                tz = job['schedule'].get('timezone', TIMEZONE)
                trigger = CronTrigger.from_crontab(t, timezone=tz)
            elif schedule_type == 'cron':
                # trigger = self.get_cron_params(job['schedule'])
                trigger = job['schedule']
                if job['start_date']:
                    trigger = {
                        **trigger,
                        **{"start_date": job['start_date']}
                    }
                if job['end_date']:
                    trigger = {
                        **trigger,
                        **{"end_date": job['end_date']}
                    }
                if jitter:
                    trigger = {**trigger, **{"jitter": jitter}}
                trigger = CronTrigger(**trigger)
            elif schedule_type == 'date':
                trigger = DateTrigger(
                    run_date=job['run_date'],
                    timezone=self._timezone
                )
            elif schedule_type == 'combined':
                # syntax:
                # { type="and", "schedule": [{"cron": "cron"}, {"cron": "cron"} ] }
                t = job['schedule']
                try:
                    jointype = t['type']
                except KeyError:
                    jointype = 'and'
                steps = []
                for trigger in t['schedule']:
                    # the expression need to be equal to Trigger Requirements
                    for step, value in trigger.items():
                        obj = self.get_trigger(step)
                        tg = obj(**value)
                        steps.append(tg)
                if jointype == 'and':
                    trigger = AndTrigger(steps)
                else:
                    trigger = OrTrigger(steps)
            ## Building Job for Scheduler:
            job_struct = {
                'id': f'{job_id}',
                'name': f'{job_id}',
                'replace_existing': True,
                'jobstore': job['jobstore'],
                'executor': job['executor']
            }
            arguments = {}
            if job['params']:
                arguments = {**job['params']}
            # agregar al args que recibe la tarea:
            arguments['loop'] = self._loop
            arguments['ENV'] = navConfig
            attributes = []
            if job['attributes']:
                attributes = job['attributes']
            ## add this job
            if job_struct:
                try:
                    j = self.scheduler.add_job(
                        func,
                        logger=self.logger,
                        jobstore_retry_interval=30,
                        trigger=trigger,
                        kwargs=arguments,
                        args=attributes,
                        **job_struct
                    )
                    info = {
                        'data': job,
                        'job': j,
                        'status': 'idle',
                        'trigger': None
                    }
                    self._jobs[job_id] = info
                except ConflictingIdError as err:
                    self.logger.error(err)
                except Exception as err:
                    self.logger.exception(err)
            else:
                self.logger.error(
                    'Scheduler: Missing Scheduled Job Structure'
                )

    def add_listeners(self):
        # Asyncio Scheduler
        self.scheduler.add_listener(
            self.scheduler_status, EVENT_SCHEDULER_STARTED)
        self.scheduler.add_listener(
            self.scheduler_shutdown, EVENT_SCHEDULER_SHUTDOWN)
        self.scheduler.add_listener(self.job_success, EVENT_JOB_EXECUTED)
        self.scheduler.add_listener(
            self.job_status, EVENT_JOB_ERROR | EVENT_JOB_MISSED
        )
        # job was submitted:
        self.scheduler.add_listener(self.job_submitted, EVENT_JOB_SUBMITTED)
        # a new job was added:
        self.scheduler.add_listener(self.job_added, EVENT_JOB_ADDED)

    def job_added(self, event: JobExecutionEvent, *args, **kwargs):
        try:
            job = self.scheduler.get_job(event.job_id)
            job_name = job.name
            self.logger.debug(
                f'Job {job_name!s} was added with args: {args!s}/{kwargs!r}'
            )
        except Exception:
            pass

    def get_jobs(self):
        return [
            job.id for job in self.scheduler.get_jobs()
        ]

    def get_all_jobs(self):
        return self.scheduler.get_jobs()

    def get_job(self, job_id):
        try:
            return self._jobs[job_id]
        except KeyError:
            return None

    def scheduler_status(self, event):
        print(event)
        self.logger.debug(f'[{ENVIRONMENT} - NAV Scheduler] :: Started.')
        self.logger.info(
            f'[{ENVIRONMENT} - NAV Scheduler] START time is: {datetime.now()}'
        )

    def scheduler_shutdown(self, event):
        self.logger.info(
            f'[{ENVIRONMENT}] Scheduler {event} Stopped at: {datetime.now()}'
        )

    def fix_job_schedule(self, job, job_id):
        if job_id in self._jobs and 'trigger' in self._jobs[job_id]:
            try:
                trigger = self._jobs[job_id]['trigger']
                if trigger and job.trigger != trigger:
                    # This task was rescheduled:
                    job.reschedule(trigger=trigger)
                    self._jobs[job_id]['trigger'] = None
                    self._jobs[job_id]['status'] = 'reverted'
                    self.logger.info(
                        f"Job {job_id} reverted to its original schedule."
                    )
            except Exception as err:
                self.logger.warning(
                    f"Error while reverted job {job_id} to original schedule: {err}"
                )

    def job_success(self, event: JobExecutionEvent):
        """Job Success.

        Event when a Job was executed successfully.

        :param apscheduler.events.JobExecutionEvent event: job execution event
        """
        job_id = event.job_id
        job = self.scheduler.get_job(job_id)
        self.fix_job_schedule(job, job_id)
        try:
            self._jobs[job_id]['status'] = 'success'
        except KeyError:
            # Job is missing from the Job Store.
            return False
        job_name = job.name
        self.logger.info(
            f'[Schedulder - {ENVIRONMENT}]: {job_name} with id {event.job_id!s} \
             was queued successfully @ {event.scheduled_run_time!s}'
        )
        # saving into Database
        event_loop = asyncio.new_event_loop()
        fn = partial(
            self.save_db_event,
            event_loop=event_loop,
            event=event,
            job=job
        )
        try:
            with ThreadExecutor(max_workers=1) as pool:
                event_loop.run_in_executor(pool, fn)
        finally:
            event_loop.close()

    def job_status(self, event: JobExecutionEvent):
        """React on Error events from scheduler.

        :param apscheduler.events.JobExecutionEvent event: job execution event.

        TODO: add the reschedule_job
        scheduler = sched.scheduler #it returns the native apscheduler instance
        scheduler.reschedule_job('my_job_id', trigger='cron', minute='*/5')

        """
        job_id = event.job_id
        job = self.scheduler.get_job(job_id)
        self.fix_job_schedule(job, job_id)
        saved_job = self._jobs[job_id]
        job_name = job.name
        scheduled = event.scheduled_run_time
        stack = event.traceback
        if event.code == EVENT_JOB_MISSED:
            self._jobs[job_id]['status'] = 'missed'
            self.logger.warning(
                f"[{ENVIRONMENT} - NAV Scheduler] Job {job_name} \
                was missed for scheduled run at {scheduled}"
            )
            message = f'⚠️ :: [{ENVIRONMENT} - NAV Scheduler] Job {job_name} was missed \
            for scheduled run at {scheduled}'
        elif event.code == EVENT_JOB_ERROR:
            saved_job['status'] = 'error'
            self.logger.error(
                f"[{ENVIRONMENT} - NAV Scheduler] Job {job_name} scheduled at \
                {scheduled!s} failed with Exception: {event.exception!s}"
            )
            message = f'🛑 :: [{ENVIRONMENT} - NAV Scheduler] Job **{job_name}** \
             scheduled at {scheduled!s} failed with Error {event.exception!s}'
            if stack:
                self.logger.exception(
                    f"[{ENVIRONMENT} - NAV Scheduler] Job {job_name} id: {job_id!s} \
                    StackTrace: {stack!s}"
                )
                message = f'🛑 :: [{ENVIRONMENT} - NAV Scheduler] Job \
                **{job_name}**:**{job_id!s}** failed with Exception {event.exception!s}'
            # send a Notification error from Scheduler
        elif event.code == EVENT_JOB_MAX_INSTANCES:
            saved_job['status'] = 'Not Submitted'
            self.logger.exception(
                f"[{ENVIRONMENT} - Scheduler] Job {job_name} could not be submitted \
                Maximum number of running instances was reached."
            )
            message = f'⚠️ :: [{ENVIRONMENT} - NAV Scheduler] Job **{job_name}** was \
            missed for scheduled run at {scheduled}'
        else:
            saved_job['status'] = 'exception'
            # will be an exception
            message = f'🛑 :: [{ENVIRONMENT} - NAV Scheduler] Job \
            {job_name}:{job_id!s} failed with Exception {stack!s}'
            # send a Notification Exception from Scheduler
        # send notification:
        event_loop = asyncio.new_event_loop()
        fn = partial(
            send_notification,
            event_loop=event_loop,
            message=message,
            provider='telegram'
        )
        saved = partial(
            self.save_db_event,
            event_loop=event_loop,
            event=event,
            job=job
        )
        # sending function coroutine to a thread
        try:
            with ThreadExecutor(max_workers=1) as pool:
                event_loop.run_in_executor(pool, saved)
                event_loop.run_in_executor(pool, fn)
        finally:
            event_loop.close()

    def save_db_event(self, event_loop, event, job):
        asyncio.set_event_loop(event_loop)
        state = Entity.escapeString(event.exception)
        trace = Entity.escapeString(event.traceback)
        if event.code == EVENT_JOB_MISSED:
            status = 3
        elif event.code == EVENT_JOB_ERROR:
            status = 2
        elif event.code == EVENT_JOB_MAX_INSTANCES:
            status = 4
        else:
            state = 'null'
            trace = 'null'
            status = 1
        status = {
            'last_exec_time': event.scheduled_run_time,
            'next_run_time': job.next_run_time,
            'job_state': state,
            'job_status': status,
            'traceback': trace,
            'job_id': event.job_id
        }
        try:
            result = event_loop.run_until_complete(
                self.update_task_status(event_loop, status)
            )
            if isinstance(result, Exception):
                self.logger.exception(result)
        except Exception as err:
            print(err)
            self.logger.exception(err)

    async def update_task_status(self, event_loop, status):
        # TODO: migrate to Prepared statements
        asyncio.set_event_loop(event_loop)
        sql = """UPDATE troc.jobs
        SET last_exec_time='{last_exec_time}', next_run_time='{next_run_time}',
        job_status='{job_status}', job_state='{job_state}', traceback='{traceback}'
        WHERE job_id = '{job_id}';"""
        sentence = sql.format(**status)
        result = None
        options = {
            "server_settings": {
                'application_name': 'Flowtask.Scheduler',
                'client_min_messages': 'notice',
                'max_parallel_workers': '256',
                'jit': 'off'
            },
            "timeout": 60
        }
        conn = AsyncDB('pg', dsn=default_dsn, loop=event_loop, **options)
        try:
            async with await conn.connection() as conn:
                result, error = await conn.execute(sentence)
                if error:
                    self.logger.error(error)
            return result
        except Exception as err:
            print(err)
            self.logger.exception(err)

    def job_submitted(self, event):
        try:
            job_id = event.job_id
            job = self.scheduler.get_job(job_id)
        except JobLookupError as exc:
            raise RuntimeError(
                f'Scheduler: There is no such Job {job_id}: {exc}'
            ) from exc
        except Exception as err:
            raise RuntimeError(
                f'Scheduler: Error on {job_id} {err}'
            ) from err
        try:
            job_name = job.name
            now = datetime.now()
            self.logger.info(
                f'Sched: Job {job_name} with id {job_id!s} was submitted @ {now}'
            )
            self._jobs[job_id]['status'] = 'dispatched'
        except AttributeError as exc:
            # we don't need to worry about startup_job.
            if event.job_id == 'on_startup_job':
                return
            raise RuntimeError(
                f'Scheduler: Error {exc}'
            ) from exc

    def get_stacktrace(self):
        """Returns the full stack trace."""

        type_, value_, traceback_ = sys.exc_info()
        return ''.join(traceback.format_exception(type_, value_, traceback_))

    def get_hostname(self):
        """Returns the host name."""
        return socket.gethostname()

    def get_pid(self):
        """Returns the process ID"""
        return os.getpid()

    async def start(self):
        try:
            # asyncio scheduler
            self.scheduler.start()
        except Exception as err:
            raise RuntimeError(
                f'Error Starting Scheduler {err!r}'
            ) from err

    async def shutdown(self, app: web.Application):
        try:
            # self.backscheduler.shutdown(wait=True)
            self.scheduler.shutdown(wait=True)
            if self._connection:
                await self._pool.release(self._connection)
            await self.db.shutdown(app)
        except Exception as err:
            self.logger.exception(f'Error on Scheduler Shutdown {err!r}')

    def get_cron_params(self, expression):
        trigger = {
            "year": "*",
            "month": "*",
            "day": "*",
            "week": "*",
            "day_of_week": "*",
            "hour": "*",
            "minute": "*",
            "second": "0"
        }
        return {**trigger, **expression}

    def get_cron_strings(self, expression):
        """Returns cron strings.
        :param dict expression: an array of cron structures.
        :return: cron strings
        :rtype: dict
        """
        trigger = expression['cron']
        return {
            'month': str(trigger[1]),
            'day': str(trigger[2]),
            'week': str(trigger[3]),
            'day_of_week': str(trigger[4]),
            'hour': str(trigger[5]),
            'minute': str(trigger[6])
        }

    def get_trigger(self, expression):
        if expression == 'cron' or expression == 'crontab':
            return CronTrigger
        elif expression == 'date':
            return DateTrigger
        elif expression == 'interval':
            return IntervalTrigger
        else:
            self.logger.exception(f'Wrong Trigger type: {expression}')
            return None
