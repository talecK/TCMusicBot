import subprocess
import time
import os
import signal

""" Change the system volume
"""
def change_volume(volume):
    # if not volume:
    #     return "Volume: " + current_volume
    # #parse volume with regex:
    # amixer get Master
    # regex = /\[\w+%\]/g

    if 1 < volume < 100:
        volume_percentage = str(volume)+"%"

        FNULL = open(os.devnull, "w")
        subprocess.Popen(["amixer", "-D", "pulse", "sset", "Master", volume_percentage],  shell=False, stdout=FNULL, stderr=subprocess.STDOUT, bufsize=1)

        return "Set Volume: " + volume_percentage
