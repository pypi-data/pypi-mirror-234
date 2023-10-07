"""
Hook Management.
"""
import asyncio
import importlib
from collections.abc import Callable
from functools import partial
from navconfig.logging import logging
from navigator.types import WebApp
from navigator.applications.base import BaseApplication
from flowtask.conf import (
    TASK_STORAGES
)
from flowtask.exceptions import (
    ConfigError,
    FlowTaskError
)
from .types.base import BaseHook


class HookService:
    def __init__(self, event_loop: asyncio.AbstractEventLoop, **kwargs):
        self._loop = event_loop
        self._hooks: list = []
        self._started: bool = False
        self.app: WebApp = None
        # TaskStorage
        self._storage = kwargs.pop('storage', 'default')
        try:
            self.taskstore = TASK_STORAGES[self._storage]
        except KeyError as exc:
            raise RuntimeError(
                f"Invalid Task Storage {self._storage}"
            ) from exc
        if not self.taskstore.path:
            raise ConfigError(
                f"Current Task Storage {self.taskstore!r} is not Supported for Hooks."
            )

    def add_hook(self, hook: BaseHook):
        self._hooks.append(hook)
        hook.setup(app=self.app)

    def setup(self, app: WebApp) -> None:
        """setup.

            Service Configuration.
        Args:
            app (aiohttp.web.Application): Web Application.
        """
        if isinstance(app, BaseApplication):  # migrate to BaseApplication (on types)
            self.app = app.get_app()
        elif isinstance(app, WebApp):
            self.app = app  # register the app into the Extension
        else:
            raise TypeError(
                f"Invalid type for Application Setup: {app}:{type(app)}"
            )
        # mark service as started.
        self._started = True
        self.load_hooks()

    def load_hooks(self) -> None:
        """load_hooks.

        Load all Hooks from the Task Storage.
        """
        self._hooks = []
        for program_dir in self.taskstore.path.iterdir():
            if program_dir.is_dir():
                hooks_dir = program_dir.joinpath('hooks.d')
                for file_path in hooks_dir.rglob('*.*'):
                    try:
                        hook = Hook(
                            asyncio.run(
                                self.taskstore.open_hook(file_path)
                            )
                        )
                        if hook:
                            for trigger in hook.triggers:
                                self.add_hook(trigger())
                    except FlowTaskError:
                        pass


def import_component(component: str, classpath: str, package: str = 'components'):
    module = importlib.import_module(classpath, package=package)
    obj = getattr(module, component)
    return obj


class StepAction:
    def __init__(self, action: str, params: dict) -> None:
        self.name = action
        self._step: Callable = None
        try:
            self._action = import_component(
                action, 'flowtask.hooks.actions', 'actions'
            )
        except (ImportError, RuntimeError) as exc:
            raise FlowTaskError(
                f"Unable to load Action {action}: {exc}"
            ) from exc
        self.params = params

    def __repr__(self) -> str:
        return f'<StepAction.{self.name}: {self.params!r}>'

    @property
    def component(self):
        return self._action

    async def run(self, *args, **kwargs):
        """Run action involved
        """
        try:
            self._step = self._action(**self.params)
            try:
                async with self._step as step:
                    result = await step.run(*args, **kwargs)
                return result
            except Exception as exc:
                logging.error(
                    f"Error running action {self._action!s}: {exc}"
                )
        except Exception as exc:
            logging.error(
                f'Unable to load Action {self._action}: {exc}'
            )
            raise

class Hook:
    """Hook.

    Compile a Hook (Triggers and Actions) and got every step on the hook.
    """
    def __init__(self, hook: dict):
        self.triggers: list = []
        self.name = hook.pop('name')
        try:
            triggers = hook['When']
        except KeyError as exc:
            raise ConfigError(
                "Hook Error: Unable to find Trigger: *When* parameter"
            ) from exc
        try:
            actions = hook['Then']
        except KeyError as exc:
            raise ConfigError(
                "Hook Error: Unable to get list of Actions: *Then* parameter"
            ) from exc
        ## build Hook Component:
        self.build(triggers, actions)

    def build(self, triggers: list, actions: list):
        self._actions: list = []
        # Then: Load Actions
        for step in actions:
            for step_name, params in step.items():
                action = StepAction(step_name, params)
                self._actions.append(action)
        for step in triggers:
            for step_name, params in step.items():
                trigger = import_component(
                    step_name, 'flowtask.hooks.types', 'types'
                )
                # start trigger:
                args = {
                    "name": self.name,
                    "actions": self._actions
                }
                args = {**args, **params}
                hook = partial(trigger, **args)
                self.triggers.append(hook)
