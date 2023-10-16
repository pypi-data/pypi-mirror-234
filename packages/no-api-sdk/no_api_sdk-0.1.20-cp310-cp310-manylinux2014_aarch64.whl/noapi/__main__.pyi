import code
import threading
from .msg import msg as msg
from _typeshed import Incomplete

class AsyncIOInteractiveConsole(code.InteractiveConsole):
    loop: Incomplete
    def __init__(self, locals, loop) -> None: ...
    def runcode(self, code): ...

async def run_init(init_code) -> None: ...

class REPLThread(threading.Thread):
    def run(self) -> None: ...
