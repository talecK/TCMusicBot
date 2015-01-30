import subprocess
import platform
import os

def change_volume(volume):
    """ Change the system volume
    """
    if 1 < volume < 100:
      volume_percentage = str(volume)+"%"

      if not 'Darwin' in platform.system():

        FNULL = open(os.devnull, "w")
        subprocess.Popen(["amixer", "-D", "pulse", "sset", "Master", volume_percentage],  shell=False, stdout=FNULL, stderr=subprocess.STDOUT, bufsize=1)

    return "Set Volume: " + volume_percentage