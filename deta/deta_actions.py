from deta import app
import subprocess
import sys


@app.lib.run()
def checkit(event):
    return sys.path
