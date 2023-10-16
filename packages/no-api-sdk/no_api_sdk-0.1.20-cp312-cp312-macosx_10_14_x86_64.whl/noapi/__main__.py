# copied from https://github.com/python/cpython/blob/main/Lib/asyncio/__main__.py
# with changes marked as #DIFF
import ast
import asyncio
import code
import concurrent.futures
import inspect
import sys
import threading
import types
import warnings
import noapi, os, sys, traceback #DIFF
from .msg import msg

# from . import futures
from asyncio import futures #DIFF


class AsyncIOInteractiveConsole(code.InteractiveConsole):

    def __init__(self, locals, loop):
        super().__init__(locals)
        self.compile.compiler.flags |= ast.PyCF_ALLOW_TOP_LEVEL_AWAIT

        self.loop = loop

    def runcode(self, code):
        future = concurrent.futures.Future()

        def callback():
            global repl_future
            global repl_future_interrupted

            repl_future = None
            repl_future_interrupted = False

            func = types.FunctionType(code, self.locals)
            try:
                coro = func()
            except SystemExit:
                raise
            except KeyboardInterrupt as ex:
                repl_future_interrupted = True
                future.set_exception(ex)
                return
            except BaseException as ex:
                future.set_exception(ex)
                return

            if not inspect.iscoroutine(coro):
                future.set_result(coro)
                return

            try:
                repl_future = self.loop.create_task(coro)
                futures._chain_future(repl_future, future)
            except BaseException as exc:
                future.set_exception(exc)

        loop.call_soon_threadsafe(callback)

        try:
            return future.result()
        except SystemExit:
            raise
        except BaseException as e:
            if repl_future_interrupted:
                self.write("\nKeyboardInterrupt\n")
            else:
                try:
                    msg._handle_native_exception(e)
                except:
                    pass
                # self.showtraceback()


async def run_init(init_code):
    if os.path.exists(init_code[0]):
        print(f'{getattr(sys, "ps1", ">>> ")}execute file "{init_code[0]}"')
        try:
            sys.argv = init_code
            exec(open(init_code[0]).read(),None,repl_locals)
        except Exception as e:
            print(f"Exception in file: {init_code[0]}")
            extracts = len(traceback.extract_tb(sys.exc_info()[2]))-1
            traceback.print_exc(limit=-extracts)
    else:
        python_code = "\n".join(init_code)
        print(f"{getattr(sys, 'ps1', '>>>')}eval('''\n{python_code}\n''')")
        try:
            exec(python_code,None,repl_locals)
        except Exception as e:
            extracts = len(traceback.extract_tb(sys.exc_info()[2]))-1
            traceback.print_exc(limit=-extracts)
    added_locals = []
    for k in repl_locals:
        if k not in ["asyncio","noapi"]:
            added_locals.append(k)
    if len(added_locals)>0:
        print("# defined:" ,",".join(added_locals))

class REPLThread(threading.Thread):

    def run(self):
        try:
            banner = ( "" ) # DIF


            console.interact(
                banner=banner,
                exitmsg='exiting noapi REPL...') #DIFF
        finally:
            warnings.filterwarnings(
                'ignore',
                message=r'^coroutine .* was never awaited$',
                category=RuntimeWarning)

            loop.call_soon_threadsafe(loop.stop)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # repl_locals = {'asyncio': asyncio}
    repl_locals = {'asyncio': asyncio,'noapi':noapi} #DIFF
    print(
                f'noapi-{noapi.__version__} REPL {sys.version} on {sys.platform}\n'  #DIFF
                f'Use "await" directly instead of "asyncio.run()".\n'
                f'Type "help", "copyright", "credits" or "license" '
                f'for more information.\n'
                f'{getattr(sys, "ps1", ">>> ")}import asyncio\n'
                f'{getattr(sys, "ps1", ">>> ")}import noapi'
    )
    init_code = None
    if len(sys.argv)>1:
        init_code=sys.argv[1:]
        initer = loop.create_task(run_init(init_code))
        loop.run_until_complete(initer)

    for key in {'__name__', '__package__',
            '__loader__', '__spec__',
            '__builtins__', '__file__'}:
        repl_locals[key] = locals()[key]


    console = AsyncIOInteractiveConsole(repl_locals, loop)

    repl_future = None
    repl_future_interrupted = False

    try:
        import readline  # NoQA
    except ImportError:
        pass

    repl_thread = REPLThread()
    repl_thread.daemon = True
    repl_thread.start()

    while True:
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            if repl_future and not repl_future.done():
                repl_future.cancel()
                repl_future_interrupted = True
            continue
        else:
            break
