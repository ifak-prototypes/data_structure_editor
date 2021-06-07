import os
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def build():
    cmd = "npm run build"
    os.system(cmd)

def on_created(event):
    print("hey, {0} has been created!".format(event.src_path))
    build()

def on_deleted(event):
    print("what the f**k! Someone deleted {0}!".format(event.src_path))
    build()

def on_modified(event):
    print("hey buddy, {0} has been modified".format(event.src_path))
    build()

def on_moved(event):
    print("ok ok ok, someone moved {0} to {1}".format(event.src_path, event.dest_path))
    build()

if __name__ == "__main__":
    patterns = "*.vue;*.js"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    path = "./src"
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
