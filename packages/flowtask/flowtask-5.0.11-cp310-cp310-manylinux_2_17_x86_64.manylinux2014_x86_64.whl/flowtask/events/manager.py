from typing import Union, Any
from collections.abc import Callable, Awaitable
import asyncio
import threading
import importlib
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from navconfig.logging import logging
from .events import AbstractEvent
from .events.publish import PublishEvent


class EventManager:
    """
    Basic Event Manager of flowtask.

    This manager allows for dynamic loading and dispatching of events based on a provided payload.
    Each event can have multiple actions, and actions can be loaded dynamically from modules.
    """

    def __init__(self, name: str = None):
        self._handlers: list[Callable] = []
        self._name = name  # event name

    def dispatch(self, event_name: str, *args, **kwargs):
        event = getattr(self, event_name, None)
        if event is None:
            raise ValueError(
                f"No event named '{event_name}' found."
            )
        try:
            event(*args, **kwargs)
        except Exception as e:
            event.logger.error(
                f'Event Error: {e}'
            )

    class Event:
        def __init__(self, functions: list[Callable], event_name: str) -> None:
            if not isinstance(functions, list):
                raise TypeError(
                    'Event Function Callable need to be a List'
                )
            self._name = event_name
            self._handlers = functions
            self.logger = logging.getLogger('Flowtask.Event')
            self._event = threading.Event()
            self._lock = threading.Lock()
            self._executor = ThreadPoolExecutor(max_workers=20)

        def add(self, func: Union[Callable, Awaitable]) -> Any:
            with self._lock:
                self._handlers.append(func)
            return self

        def close(self):
            try:
                self._executor.shutdown()
            except Exception:
                pass

        def __repr__(self) -> str:
            return f'<Event: {self._name}>'

        def __iadd__(self, func: Union[Callable, Awaitable]) -> Any:
            with self._lock:
                self._handlers.append(func)
            return self

        def __isub__(self, func: Union[Callable, Awaitable]):
            with self._lock:
                self._handlers.remove(func)
            return self

        def __call__(self, *args, **kwargs):
            self._event.set()
            # creating the executor
            fn = partial(
                self._executeEvent,
                handlers=self._handlers,
                *args, **kwargs
            )
            # sending function coroutine to a thread
            self._executor.submit(fn)

        def _executeEvent(self, handlers: list[Callable], *args, **kwargs):
            """
            executeEvent.

            Executing Event Functions associated with an event dispatched from Flowtask.
            """
            self._event.wait()
            for fn in handlers:
                if asyncio.iscoroutinefunction(fn) or isinstance(fn, AbstractEvent):
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        try:
                            loop.run_until_complete(fn(*args, event_loop=loop, **kwargs))
                        except Exception as ex:
                            print(f'Event Error: {ex}')
                        finally:
                            tasks = asyncio.all_tasks(loop)
                            for task in tasks:
                                try:
                                    task.cancel()
                                    # await task
                                except asyncio.CancelledError:
                                    pass
                            loop.close()
                    except Exception as err:
                        raise RuntimeError(
                            f"Event Error: {err!s}"
                        ) from err
                else:
                    try:
                        fn(*args, **kwargs)
                    except Exception as err:
                        self.logger.exception(err)
                        raise RuntimeError(
                            f"Event Error: {err!s}"
                        ) from err

    @classmethod
    def addEvent(cls, **kwargs):
        """
        addEvent( event1 = [f1,f2,...], event2 = [g1,g2,...], ... )
        creates events using **kwargs to create any number of events.
        Each event recieves a list of functions,
        where every function in the list recieves the same parameters.
        Example:
        def hello(): print("Hello ")
        def world(): print("World")

        EventManager.addEvent( salute = [hello] )
        EventManager.salute += world

        EventManager.salute()

        Output:
        Hello
        World
        """
        evt = {}
        for key, value in kwargs.items():
            if not isinstance(value, list):
                fn = [value]
            else:
                fn = value
            evt[key] = cls.Event(fn, key)
            setattr(cls, key, evt[key])
        return evt

    def validate_event_payload(self, payload: dict):
        if not isinstance(payload, dict):
            raise ValueError("Event payload should be a dictionary.")

        for event_name, event_list in payload.items():
            if not isinstance(event_list, list):
                raise ValueError(f"Event {event_name} should have a list of actions.")

            for action in event_list:
                if not isinstance(action, dict):
                    raise ValueError(f"Action for event {event_name} should be a dictionary.")

    def LoadEvents(self, event_payload: dict):
        """
        Load all events and their associated actions based on the provided payload.

        The payload should be a dictionary where each key is an event name and the associated value
        is a list of action dictionaries. Each action dictionary should have a single key (the action name)
        and a value that is a dictionary of parameters for that action.

        Example payload:
        {
            "completed": [
                {
                    "Dummy": {
                        "message": "Finished"
                    }
                }
            ],
            ...
        }

        Args:
            event_payload (dict): The event payload dictionary.

        Raises:
            RuntimeError: If there's an error loading an action.
        """
        # finished task will be published into a pub/sub channel
        publish = event_payload.pop('publish', False)
        # Add this execution to the publish channel.
        if publish is True:
            pub = PublishEvent()
            completed = getattr(self, 'completed')
            if completed:
                completed += pub
            exception = getattr(self, 'exception')
            if exception:
                exception += pub
        self.validate_event_payload(event_payload)
        for event_name, event_list in event_payload.items():
            evt = getattr(self, event_name, None)
            if evt:
                for event_obj in event_list:
                    event_type = list(event_obj.keys())[0]
                    event_data = event_obj[event_type]
                    action = self.LoadEventAction(event_type, event_data)
                    try:
                        # added this event to the event list
                        evt += action
                    except Exception as e:
                        logging.error(
                            f"Load Event Error: {e}"
                        )

    def LoadEventAction(self, action_name: str, data):
        try:
            current_package = __package__
            module_name = f"{current_package}.events"
            mod = importlib.import_module(module_name, package=action_name)
            obj = getattr(mod, action_name)
            return obj(**data)
        except ImportError as e:
            logging.error(
                f"Event Action: Error getting Function: {action_name}, {e!s}"
            )
