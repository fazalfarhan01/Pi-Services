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

    def getUpdates(self):
        command = "sudo apt update"
        stream = subprocess.Popen(command, stdout=self.STD_OUT,
                                  stderr=self.STD_ERR, stdin=self.STD_IN, shell=True)
        # stream.communicate()
        updateThread = threading.Thread(name="update", target=stream.communicate)
        updateThread.join()
        # while True:
        #     output = stream.stdout.readline()
        #     if output == '' and stream.poll() is not None:
        #         break
        #     if output:
        #         rc = stream.poll()
        #         yield(output.strip().decode("utf-8"), rc)
        # return (output.strip().decode("utf-8"), rc)
        self.__doUpgrades()

    def __doUpgrades(self):
        command = "sudo apt upgrade -y"
        stream = subprocess.Popen(command, stdout=self.STD_OUT,
                                  stderr=self.STD_ERR, stdin=self.STD_IN, shell=True)
        upgradeThread = threading.Thread(name="upgrade", target=stream.communicate)

    def shutdownSystem(self):
        command = "sudo shutdown now"
        stream = subprocess.Popen(command, stdout=self.STD_OUT,
                                  stderr=self.STD_ERR, stdin=self.STD_IN, shell=True)
        stream.communicate()

    def restartSystem(self):
        command = "sudo reboot"
        stream = subprocess.Popen(command, stdout=self.STD_OUT,
                                  stderr=self.STD_ERR, stdin=self.STD_IN, shell=True)
        stream.communicate()
        


if __name__ == "__main__":
    sysFunc = SystemFunctions(DEBUG_MODE=True)
    # sysFunc.getUpdates()
