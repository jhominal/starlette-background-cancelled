import anyio
from starlette.applications import Starlette
from starlette.background import BackgroundTask, BackgroundTasks
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route


async def sleep_and_print(identifier: str, delay: float):
    try:
        print(f"Background task {identifier} entered")
        await anyio.sleep(delay)
        print(f"Background task {identifier} completed after {delay} seconds")
    except anyio.get_cancelled_exc_class():
        print(f"Background task {identifier} was cancelled")
        raise


async def single_background_task(request: Request) -> Response:
    background = BackgroundTask(sleep_and_print, "single", 5)
    return Response(background=background)


async def multiple_background_tasks(request: Request) -> Response:
    background = BackgroundTasks()
    background.add_task(sleep_and_print, "1", 5)
    background.add_task(sleep_and_print, "2", 5)
    return Response(background=background)


async def wait_before_response(request: Request) -> Response:
    delay = 5
    try:
        print(f"wait_before_response entered")
        await anyio.sleep(delay)
        print(f"wait_before_response completed after {delay} seconds")
        return Response()
    except anyio.get_cancelled_exc_class():
        print(f"wait_before_response cancelled")
        raise


application = Starlette(
    routes=[
        Route("/single", endpoint=single_background_task),
        Route("/multiple", endpoint=multiple_background_tasks),
        Route("/wait", endpoint=wait_before_response),
    ],
)
