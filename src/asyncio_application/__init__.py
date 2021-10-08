import asyncio
import logging
import signal
from functools import partial

logger = logging.getLogger(__name__)

def start():
    loop = asyncio.get_event_loop()

    # Install SIGINT and SIGTERM handlers to shutdown the server
    loop.add_signal_handler(signal.SIGINT,
            partial(loop.create_task, shutdown(signal.SIGINT)))
    loop.add_signal_handler(signal.SIGTERM,
            partial(loop.create_task, shutdown(signal.SIGTERM)))

    # Log on next loop iteration
    loop.call_soon(lambda: logger.info('Started asyncio application'))

    # Start event loop
    loop.run_forever()


async def shutdown(sig):
    '''
    Inspired by https://gist.github.com/nvgoldin/30cea3c04ee0796ebd0489aa62bcf00a
    '''
    logger.info('Caught {0}, shutting down...'.format(sig.name))

    # Finish all tasks currently scheduled
    logger.info('Awaiting all scheduled tasks...')
    tasks = [task for task in asyncio.all_tasks() if task is not
             asyncio.current_task()]
    await asyncio.gather(*tasks, return_exceptions=True)
    logger.info('Finished all scheduled tasks.')

    # Stop the event loop
    asyncio.get_event_loop().stop()
