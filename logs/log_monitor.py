# logs/log_monitor.py
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        # Implement additional logic here, e.g., send message to Flask app
    
    def on_created(self, event):
        if event.is_directory:
            return
        # Implement additional logic here, e.g., send message to Flask app

if __name__ == "__main__":
    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
