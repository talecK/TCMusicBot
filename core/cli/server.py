import subprocess
import os


def change_volume(volume):
    """ Change the system volume
    """
    if 1 < volume < 100:
        volume_percentage = str(volume)+"%"

        FNULL = open(os.devnull, "w")
        subprocess.Popen(["amixer", "-D", "pulse", "sset", "Master", volume_percentage],  shell=False, stdout=FNULL, stderr=subprocess.STDOUT, bufsize=1)

        return "Set Volume: " + volume_percentage
