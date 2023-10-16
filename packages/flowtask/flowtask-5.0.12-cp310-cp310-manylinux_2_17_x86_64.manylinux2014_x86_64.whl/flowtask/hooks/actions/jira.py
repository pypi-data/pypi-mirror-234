from jira import JIRA
from flowtask.conf import (
    JIRA_API_TOKEN,
    JIRA_USERNAME,
    JIRA_INSTANCE,
    JIRA_PROJECT
)
from .ticket import AbstractTicket


class JiraTicket(AbstractTicket):
    """Jira.

    Create a Jira Ticket using a Hook.
    """
    async def open(self):
        args = {
            "basic_auth": (JIRA_USERNAME, JIRA_API_TOKEN)
        }
        try:
            self.service = JIRA(JIRA_INSTANCE, **args)
        except Exception as e:
            self._logger.error(
                f"Error connecting to JIRA Instance: {e}"
            )
            raise

    async def close(self):
        self.service = None

    async def create(self, *args, **kwargs):
        """create.

        Create a new Ticket.
        """
        project = kwargs.pop('project', JIRA_PROJECT)
        summary = kwargs.pop('summary', None)
        description = kwargs.pop('description', None)
        args = {
            "project": project,
            "summary": summary,
            "description": description,
            "issuetype": {'name': 'Bug'}
        }
        if 'issuetype' in kwargs:
            args['issuetype'] = {
                "name": kwargs['issuetype']
            }
        try:
            new_issue = self.service.create_issue(
                **args
            )
            print('ISSUE ', new_issue)
            return new_issue
        except Exception as e:
            self._logger.error(
                f"Error creating Jira Ticket: {e}"
            )
            raise
