import sys
import logging
import psutil
import hashlib
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

logger = logging.getLogger(__name__)
file_hashes = {}

class RansomwareMonitor(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        file_hash = self.calculate_hash(file_path)

        if file_path in file_hashes and file_hashes[file_path] != file_hash:
            print(f"[!!!] Possible ransomware detection: {file_path}")

        file_hashes[file_path] = file_hash
    
    def calculate_hash(self, file_path):
        try:
            with open(file_path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except:
            return None

def main():
    # Log configuration for LoggingEventHandler()
    logging.basicConfig(stream = sys.stdout ,
                        level = logging.INFO,
                        format = "%(asctime)s %(message)s",
                        datefmt = "%d.%m.%Y %H:%M:%S"
                        )
    logger.info("Started")
    #
    observer = Observer()
    event_handler = RansomwareMonitor() # / LoggingEventHandler()
    path = "C:/.."
    observer.schedule(event_handler, path, recursive=True)
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