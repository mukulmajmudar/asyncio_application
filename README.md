# asyncio_application
## Clean startup and shutdown for asyncio-based applications
Call `asyncio_application.start()` to start the event loop. Gracefully shutdown the application by sending the `SIGINT` (Ctrl+C) or `SIGTERM` signal to the process.

Requires Python 3.7 or higher.
