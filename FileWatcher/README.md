# File watcher

Watches a folder for new pictures (.jpg, .png) and display it automatically on a second physical screen.
* Relies on external *Image Viewer* https://github.com/torum/Image-viewer to display pictures
* Uses <code>watchdog</code> library (<code>pip install watchdog</code>)
* Watched direcory is the only argument (exemple : <code>python watchNewPics.py c:\myAIgeneratedPicsFolder</code>)
