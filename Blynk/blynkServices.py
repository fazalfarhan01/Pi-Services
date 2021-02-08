#!/usr/bin/python3

from gpiozero import CPUTemperature
import blynklib, blynktimer

from IPTools import IPTools
from systemFunction import SystemFunctions

# importing configuration file
import config

blynk = blynklib.Blynk(config.BLYNK_AUTH, server=config.SERVER_NAME, port=config.SERVER_PORT)
timer = blynktimer.Timer()


DEBUG_MODE = True

# TIMER TO SEND CURRENT CPU TEMPERATURE
@timer.register(vpin_num=config.TEMP_PIN, interval=2, run_once=False)
def writeCPUTemp(vpin_num = config.TEMP_PIN):
    temp = CPUTemperature().temperature
    blynk.virtual_write(vpin_num, temp)
    if DEBUG_MODE:
        print("Sending CPU Temp to pin \tV{}\t{}".format(vpin_num, temp))

# TIMER TO SEND LOCAL IP ADDRESS TO SERVER
@timer.register(vpin_num=config.LOCAL_IP_PIN, interval=20, run_once=False)
def writeLocalIP(vpin_num = config.LOCAL_IP_PIN):
    IP = IPTools().getLocalIP()
    blynk.virtual_write(vpin_num, IP)
    if DEBUG_MODE:
        print("Sending Local IP Addrs to pin \tV{}\t{}".format(vpin_num, IP))

# TIMER TO SEND PUBLIC IP TO SERVER
# USES IPTools PACKAGE
@timer.register(vpin_num=config.PUBLIC_IP_PIN, interval=1, run_once=True)
@timer.register(vpin_num=config.PUBLIC_IP_PIN, interval=60, run_once=False)
def writePublicIP(vpin_num = config.PUBLIC_IP_PIN):
    IP = IPTools().getPublicIP()
    blynk.virtual_write(vpin_num, IP)
    if DEBUG_MODE:
        print("Sending Public IP Addrs to pin \tV{}\t{}".format(vpin_num, IP))


'''
TO PERFORM UPDATES
THE REGULAR sudo apt update and upgrade thing
'''
@blynk.handle_event("write V{}".format(config.UPDATE_PIN))
def performUpdate(pin, value):
    if value[0] == "1":
        # blynk.notify("Performing Updates.\n\nPlease Wait..!")
        blynk.notify("Functionality is dangerous to be implemented.!\n\ncould corrupt storage.")
        # SystemFunctions().getUpdates()
    if DEBUG_MODE:
        print("Got Update Request on pin \tV{}\t{}".format(pin, value[0]))


"""
TO PERFORM BACKUP OF ALL NECESSARY FILES AND DATA
EXAMPLE BLYNK DATA AND OTHER CONFIGURATION FILES
"""
@blynk.handle_event("write V{}".format(config.BACKUP_PIN))
def performBackup(pin, value):
    if value[0] == "1":
        blynk.notify("Performing Backup.\n\nPlease Wait..!")
    if DEBUG_MODE:
        print("Got Backup Request on pin \tV{}\t{}".format(pin, value[0]))

# TO PERFORM BASIC SHUTDOWN
@blynk.handle_event("write V{}".format(config.SHUTDOWN_PIN))
def performShutdown(pin, value):
    if value[0] == "100":
        blynk.notify("Turning off RPi4!")
        blynk.virtual_write(pin, 0)
        SystemFunctions().shutdownSystem()
    if DEBUG_MODE:
        print("Got Shutdown Request on pin \tV{}\t{}".format(pin, value[0]))

# TO PERFORM BASIC RESTART
@blynk.handle_event("write V{}".format(config.RESTART_PIN))
def performRestart(pin, value):
    if value[0] == "100":
        blynk.notify("Restarting RPi4!")
        blynk.virtual_write(pin, 0)
        SystemFunctions().restartSystem()
    if DEBUG_MODE:
        print("Got Restart Request on pin \tV{}\t{}".format(pin, value[0]))

while True:
    blynk.run()
    timer.run()