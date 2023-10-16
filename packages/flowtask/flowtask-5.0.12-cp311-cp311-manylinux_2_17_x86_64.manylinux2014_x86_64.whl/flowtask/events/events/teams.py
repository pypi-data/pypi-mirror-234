from notify.models import TeamsCard, TeamsChannel
from notify.providers.teams import Teams
from notify.conf import (
    MS_TEAMS_DEFAULT_TEAMS_ID,
    MS_TEAMS_DEFAULT_CHANNEL_ID
)
from flowtask.utils.json import json_encoder
from .abstract import AbstractEvent


class TeamsMessage(AbstractEvent):
    async def __call__(self, *args, **kwargs):
        team_id = kwargs.pop('team_id', MS_TEAMS_DEFAULT_TEAMS_ID)
        tm = Teams(
            as_user=True,
            team_id=team_id,
        )
        self.channel = self.get_env_value(
            self.channel,
            default=MS_TEAMS_DEFAULT_CHANNEL_ID
        )
        channel = TeamsChannel(
            name=self.channel_name,
            team_id=MS_TEAMS_DEFAULT_TEAMS_ID,
            channel_id=self.channel
        )
        status = kwargs.pop('status', 'done')
        task = kwargs.pop('task', None)
        program = task.getProgram()
        task_name = f"{program}.{task.taskname}"
        task_id = task.task_id
        message = kwargs.pop(
            'message',
            f'Task Completed {task_name}'
        )
        try:
            stat = task.stats  # getting the stat object:
            stats = stat.to_json()
        except AttributeError:
            stats = []
        if status == 'done':
            icon = '✅'
        elif status in ('error', 'failed', 'exception'):
            icon = '🛑'
        elif status == 'warning':
            icon = '⚠️'
        else:
            icon = '✅'
        txt = f"{icon} {message}"
        if self.type == 'card':
            msg = TeamsCard(
                text=txt,
                summary='Task Summary'
            )
            if hasattr(self, 'with_stats'):
                # iterate over task stats:
                for stat, value in stats['steps'].items():
                    section = msg.addSection(
                        activityTitle=stat,
                        text=stat
                    )
                    section.addFacts(
                        facts=[
                            {
                                "name": stat,
                                "value": json_encoder(value)
                            }
                        ]
                    )
        async with tm as conn:
            result = await conn.send(
                recipient=channel,
                message=msg
            )
            return result
