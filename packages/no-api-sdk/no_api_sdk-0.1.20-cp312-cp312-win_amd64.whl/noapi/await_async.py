# emacs mycoding: utf-8
# mypy: disallow-untyped-defs
# mypy: check-untyped-defs
# mypy: disallow-incomplete-defs

import asyncio
import nest_asyncio # type: ignore
nest_asyncio.apply()
import logging
from typing import Any, Callable

def _handle_task_result(task: asyncio.Task) -> None:
    try:
        task.result()
    except asyncio.CancelledError:
        pass  # Task cancellation should not be logged as an error.
    except Exception as e:  # pylint: disable=broad-except
        print("Exception in task")
        print(e)
        logging.exception('Exception raised by task = %r', task)

def _await_async(f: Any,default_timeout: float=3600.0) -> Any:
    try:
        try:
            loop = asyncio.get_running_loop()
        except:
            loop = None

        if loop is None:
            raise Exception("ERROR: noapi requires an event loop: Put your program in a function f, run it with noapi.run(f). See http://DATALINK/EVENTLOOP")

        tor = loop.run_until_complete(f)
        return tor
    except KeyboardInterrupt as e:
        raise
    except BaseException as e:
        # import traceback
        # print(traceback.format_exc())
        raise
