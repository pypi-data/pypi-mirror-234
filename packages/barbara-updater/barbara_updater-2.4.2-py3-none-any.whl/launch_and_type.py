#!/usr/bin/env python3

import subprocess
import os
import time

def focus_on_shell():
    # Use xdotool to find the Thonny shell window and focus on it
    subprocess.run(["xdotool", "search", "--name", "Shell", "windowactivate"])

def launch_and_type():
    # Set the DISPLAY environment variable
    os.environ['DISPLAY'] = ":0.0"

    # Launch Thonny
    subprocess.Popen(["thonny"])

    # Wait for Thonny to initialize (adjust the sleep time as needed)
    time.sleep(13)

    # Focus on the Thonny shell window
    focus_on_shell()

    # Type something in the terminal window
    subprocess.run(["xdotool", "type", "%Run /home/santod/barbara.py"])
    subprocess.run(["xdotool", "key", "Return"])

if __name__ == "__main__":
    launch_and_type()

