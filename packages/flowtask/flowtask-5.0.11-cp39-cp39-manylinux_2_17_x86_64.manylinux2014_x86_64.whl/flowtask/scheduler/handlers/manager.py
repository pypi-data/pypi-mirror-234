"""
Scheduler Manager.

API View for Managing the Scheduler.
"""
import asyncio
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from navigator.views import BaseView
from navconfig.logging import logging
from flowtask.exceptions import FlowTaskError


class SchedulerManager(BaseView):
    """Scheduler Manager Facility.

    get: getting Scheduler and Jobs information, for Jobs or a single job
    post: editing existing jobs
    put: inserting a new task into the jobstore
    delete: removing (or pausing) some jobs from the scheduler
    patch: reload all jobs.
    """
    async def get(self):
        app = self.request.app
        scheduler = app['scheduler']
        args = self.match_parameters(self.request)
        qs = self.query_parameters(self.request)
        try:
            job = args['job']
        except KeyError:
            job = None
        if job is None:
            if qs.get('calendar'):
                filter_day = qs.get('day', None)
                jobs_data = []
                for job in scheduler.get_all_jobs():
                    if job:
                        ts = job.next_run_time
                        jobs_data.append(
                            {
                                'id': job.id,
                                'name': job.name,
                                'next_run_time': job.next_run_time,
                                'date': ts.date(),
                                'hour': ts.time(),
                                'day': ts.strftime('%a'),
                                'trigger': f"{job.trigger!r}"
                            }
                        )
                # Organize by day
                jobs_by_day = defaultdict(list)
                job_data = sorted(jobs_data, key=lambda x: x['hour'])
                if filter_day:
                    for job in job_data:
                        if job['day'] == filter_day:
                            jobs_by_day[filter_day].append(job)
                    return self.json_response(
                        response=jobs_by_day,
                        state=200
                    )
                else:
                    # returning all days data:
                    for job in job_data:
                        day_key = job['day']
                        jobs_by_day[day_key].append(job)
                    days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                    job_data = {day: jobs_by_day[day] for day in days_order if day in jobs_by_day}
                return self.json_response(
                    response=job_data,
                    state=200
                )
            job_list = []
            for job in scheduler.get_all_jobs():
                j = scheduler.get_job(job.id)
                obj = {}
                obj[job.id] = {
                    "job_id": job.id,
                    "name": job.name,
                    "trigger": f"{job.trigger!r}",
                    "next_run_time": job.next_run_time,
                    "function": f"{job.func!r}",
                    "last_status": 'paused' if job.next_run_time is None else j['status']
                }
                job_list.append(obj)
            return self.json_response(
                response=job_list,
                state=200
            )
        else:
            # getting all information about a single job.
            try:
                obj = scheduler.get_job(job)
                print(obj)
                data = obj['data']
                print(obj['data'], obj['status'])
                job = obj['job']
                if job.next_run_time is None:
                    status = 'Paused'
                else:
                    status = obj['status']
                result = {
                    "job_id": job.id,
                    "name": job.name,
                    "trigger": f"{job.trigger!r}",
                    "next_run_time": job.next_run_time,
                    "last_exec_time": data['last_exec_time'],
                    "function": f"{job.func!r}",
                    "last_status": status,
                    "last_traceback": data['job_state']
                }
                print(result)
                return self.json_response(
                    response=result,
                    state=200
                )
            except Exception as err:
                logging.exception(f'Error getting Job Scheduler info: {err!s}')
                return self.error(
                    request=self.request,
                    response=f'Error getting Job Scheduler info: {err!s}',
                    state=406
                )

    async def put(self):
        app = self.request.app
        scheduler = app['scheduler']
        return self.json_response(
            response="Empty",
            state=204
        )

    def reload_jobs(self, scheduler):
        try:
            loop = scheduler.event_loop
            asyncio.set_event_loop(loop)
            future = asyncio.run_coroutine_threadsafe(scheduler.create_jobs(), loop)
            print(future)
            return future.result()
        except Exception as err:
            raise FlowTaskError(
                f"{err!s}"
            ) from err

    async def patch(self):
        app = self.request.app
        scheduler = app['scheduler']
        args = self.match_parameters(self.request)
        try:
            job = args['job']
        except KeyError:
            job = None
        if job is None:
            # first: stop the server
            scheduler.scheduler.shutdown(wait=False)
            # second: remove (reload) all jobs from scheduler.
            for job in scheduler.get_all_jobs():
                # first: remove all existing jobs from scheduler
                logging.debug(f'Scheduler: Removing Job {job.id} from job store')
                job.remove()
            # after this, call again create jobs.
            try:
                loop = scheduler.event_loop
                try:
                    with ThreadPoolExecutor(max_workers=2) as executor:
                        fn = partial(self.reload_jobs, scheduler)
                        result = await loop.run_in_executor(executor, fn)
                except Exception as e:
                    print(e)
                # result = await self.reload_jobs(scheduler)
                await asyncio.sleep(.1)
                # start server again
                await scheduler.start()
                result = {
                    "status": "done",
                    "description": "Scheduler was restarted."
                }
                return self.json_response(
                    response=result,
                    state=200
                )
            except Exception as err:
                logging.exception(f'Error Starting Scheduler {err!r}')
                return self.error(
                    request=self.request,
                    response=f'Error Starting Scheduler {err!r}',
                    state=406
                )
        else:
            try:
                job_struc = scheduler.get_job(job)
                job = job_struc['job']
                # getting info about will be paused or removed (TODO removed).
                job.resume()
                return self.json_response(
                    response=f"Job {job} was Resumed from Pause state.",
                    state=202
                )
            except Exception as err:
                logging.exception(f'Invalid Job Id {job!s}: {err!s}')
                return self.error(
                    request=self.request,
                    response=f'Invalid Job Id {job!s}: {err!s}',
                    state=406
                )

    async def delete(self):
        app = self.request.app
        scheduler = app['scheduler']
        args = self.match_parameters(self.request)
        try:
            job = args['job']
        except KeyError:
            job = None
        if job is None:
            # TODO: shutdown the Scheduler
            return self.error(
                request=self.request,
                response='Scheduler: Missing Job Information',
                state=406
            )
        else:
            try:
                job_struc = scheduler.get_job(job)
                job = job_struc['job']
                # getting info about will be paused or removed (TODO removed).
                job.pause()
                return self.json_response(
                    response=f"Job {job} was Paused.",
                    state=202
                )
            except Exception as err:
                logging.exception(f'Invalid Job Id {job!s}: {err!s}')
                return self.error(
                    request=self.request,
                    response=f'Invalid Job Id {job!s}: {err!s}',
                    state=406
                )
