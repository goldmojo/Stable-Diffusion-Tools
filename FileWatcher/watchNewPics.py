#!/usr/bin/python
# To be used with Image Viewer => https://github.com/torum/Image-viewer

import os
import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Viewer:
    VIEW = None
    # File extensions of interest
    IMAGES_EXTENSIONS = ["png", "jpg"]
    # Screen to be used (0=primary, 1=secondary, etc.)
    SCREEN = 1

    def display(self, filepath):
        if (filepath[-3:] in self.IMAGES_EXTENSIONS):
            viewerCommandLine = ["imageviewer", "--moniter=" + str(self.SCREEN), "--fullscreen=on", filepath]
            print (viewerCommandLine)
            tempView = subprocess.Popen (viewerCommandLine)
            # Wait for new pic to be displayed before closing previous
            time.sleep(3)
            if self.VIEW:
                self.VIEW.terminate()
            self.VIEW = tempView

class Watcher:
    WATCHED_DIRECTORY = None
    # Directory scan delay in seconds
    POLL_DELAY = 3
    PIC_VIEWER = Viewer()

    def __init__(self, watchedDirectory):
        self.WATCHED_DIRECTORY = watchedDirectory
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.WATCHED_DIRECTORY, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(self.POLL_DELAY)
        except:
            self.observer.stop()
            if self.PIC_VIEWER.VIEW:
                self.PIC_VIEWER.VIEW.terminate()
            print ("Goodbye !")
        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print ("Received created event - %s." % event.src_path)
            # Wait for end of file writing
            time.sleep(0.5)
            Watcher.PIC_VIEWER.display (event.src_path)
        elif event.event_type == 'moved':
            # Take any action here when a file is moved or renamed.
            print ("Received moved event - %s." % event.dest_path)
            # Wait for end of file writing
            time.sleep(0.5)
            Watcher.PIC_VIEWER.display (event.dest_path)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ("Watched folder is requiered as script argument.")
        sys.exit(1)
    if os.path.isdir(sys.argv[1]):
        print ("Watching " + sys.argv[1])
        w = Watcher(sys.argv[1])
        w.run()
    else:
        print ("Watched folder is requiered as script argument.")
        print (sys.argv[1] + " is not a folder.")
        sys.exit(1)
