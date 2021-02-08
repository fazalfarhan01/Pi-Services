import subprocess
import sys
import threading


class SystemFunctions():
    def __init__(self, DEBUG_MODE=False):
        self.DEBUG_MODE = DEBUG_MODE
        self.setupModes()

    def setupModes(self):
        if self.DEBUG_MODE:
            print("Debug Mode")
            self.STD_OUT = sys.stdout
            self.STD_ERR = sys.stderr
            self.STD_IN = sys.stdin
        else:
            self.STD_OUT = subprocess.PIPE
            self.STD_ERR = subprocess.STDOUT
            self.STD_IN = subprocess.PIPE

    def runUpdates(self):
        command = "sudo apt update"
        stream = subprocess.Popen(command, stdout=self.STD_OUT,
                                  stderr=self.STD_ERR, stdin=self.STD_IN, shell=True)
        thread = threading.Thread(name="scrcpy", target=stream.communicate)

if __name__ == "__main__":
    sysFunc = SystemFunctions(DEBUG_MODE=True)
    sysFunc.runUpdates()
