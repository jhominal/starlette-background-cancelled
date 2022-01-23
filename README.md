# starlette-bg-cancelled

This repository is here to reproduce a bug observed in the usage of background tasks in Starlette.

## Requirements

Install uvicorn, gunicorn and starlette
```commandline
pip install uvicorn gunicorn starlette
```

## Launch the server

Launch the server either with `uvicorn`, on a TCP or Unix socket:

```commandline
uvicorn bg_tasks:application --port 8000
```
```commandline
uvicorn bg_tasks:application --uds server.sock
```

Or with `gunicorn`

```commandline
gunicorn -k uvicorn.workers.UvicornWorker bg_tasks:application --bind 127.0.0.1:8000
```
```commandline
gunicorn -k uvicorn.workers.UvicornWorker bg_tasks:application --bind unix:server.sock
```

## Launch the HTTP client scripts

The HTTP client scripts will target port 8000 (default for both
uvicorn and gunicorn).

To call the `/single` route - connection is closed after response is received:
```commandline
python http_call.py single --tcp 127.0.0.1:8000
```
```commandline
python http_call.py single --uds server.sock
```

To call the `/multiple` route - connection is closed after response is received:
```commandline
python http_call.py multiple --tcp 127.0.0.1:8000
```
```commandline
python http_call.py multiple --uds server.sock
```

To call the `/wait` route and close connection without waiting for the response:
```commandline
python http_call.py wait --tcp 127.0.0.1:8000 --action close_nowait
```
```commandline
python http_call.py wait --uds server.sock --action close_nowait
```
