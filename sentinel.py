import sys
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(stream = sys.stdout ,
                        level = logging.INFO,
                        format = "%(asctime)s %(message)s",
                        datefmt = "%d.%m.%Y %H:%M:%S"
                        )
    logger.info("Started")
    observer = Observer()
    event_handler = LoggingEventHandler()
    path = "."
    observer.schedule(event_handler, path)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()
        logger.info("Finished")

if __name__ == '__main__':
    main()