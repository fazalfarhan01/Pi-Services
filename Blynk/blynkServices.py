#!/usr/bin/python3

from gpiozero import CPUTemperature
import blynklib
import blynktimer
import threading
import psutil

import config

from ipTools.IPTools import IPTools
from systemFunctions.systemFunction import SystemFunctions
from blynkSkill.BlynkSkill import BlynkSkill


skill = BlynkSkill()
blynk = blynklib.Blynk(
    config.BLYNK_AUTH, server=config.SERVER_NAME, port=config.SERVER_PORT)
timer = blynktimer.Timer()


DEBUG_MODE = True


# TIMER TO SEND CURRENT CPU TEMPERATURE
@timer.register(vpin_num=config.TEMP_PIN, interval=1, run_once=False)
def writeCPUTemp(vpin_num=config.TEMP_PIN):
    temp = CPUTemperature().temperature
    blynk.virtual_write(vpin_num, temp)
    if DEBUG_MODE:
        print("Sending CPU Temp to pin \tV{}\t{}".format(vpin_num, temp))


# TIMER TO SEND LOCAL IP ADDRESS TO SERVER
@timer.register(vpin_num=config.LOCAL_IP_PIN, interval=20, run_once=False)
def writeLocalIP(vpin_num=config.LOCAL_IP_PIN):
    try:
        IP = IPTools().getLocalIP()
        blynk.virtual_write(vpin_num, IP)
        if DEBUG_MODE:
            print("Sending Local IP Addrs to pin \tV{}\t{}".format(vpin_num, IP))
    except:
        print("No Internet IG")


# TIMER TO SEND PUBLIC IP TO SERVER
# USES IPTools PACKAGE
@timer.register(vpin_num=config.PUBLIC_IP_PIN, interval=1, run_once=True)
@timer.register(vpin_num=config.PUBLIC_IP_PIN, interval=180, run_once=False)
def writePublicIP(vpin_num=config.PUBLIC_IP_PIN):
    try:
        IP = IPTools().getPublicIP()
        blynk.virtual_write(vpin_num, IP)
        if DEBUG_MODE:
            print("Sending Public IP Addrs to pin \tV{}\t{}".format(vpin_num, IP))
    except:
        print("No Internet IG")


@timer.register(vpin_num=config.CPU_USAGE_PINS[0], interval=1, run_once=True)
def writeCPUUsage(vpin_num=config.CPU_USAGE_PINS[0]):
    threading.Thread(name="CPU Usage", target=sendCPUUsage).start()

def sendCPUUsage():
    while True:
        usage = psutil.cpu_percent(1, True)
        for i in range(len(usage)):
            if DEBUG_MODE:
                print("CPU{} Usage: {}\t\t".format(i, usage[i]), end="")
            blynk.virtual_write(config.CPU_USAGE_PINS[i], usage[i])
        if DEBUG_MODE:
            print("")


'''
TO PERFORM UPDATES
THE REGULAR sudo apt update and upgrade thing
'''


@blynk.handle_event("write V{}".format(config.UPDATE_PIN))
def performUpdate(pin, value):
    if value[0] == "1":
        # blynk.notify("Performing Updates.\n\nPlease Wait..!")
        blynk.notify(
            "Functionality is dangerous to be implemented.!\n\ncould corrupt storage.")
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


@blynk.handle_event("write V{}".format(config.WIFI_2G_PIN))
def toggleWiFi(pin, value):
    currentStatus = SystemFunctions().getWiFiStatus()
    if currentStatus == True:
        message = "Turning OFF WiFi"
    else:
        message = "Turning ON WiFi"
    if DEBUG_MODE:
        print(message)
    threading.Thread(name="Toggle WiFI", target=SystemFunctions(
    ).toggleWiFi, args=[currentStatus]).start()
    blynk.notify(message)
    blynk.virtual_write(config.WIFI_2G_PIN, int(not currentStatus))


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


@blynk.handle_event("write V{}".format(config.CAMERA_SELECT_PIN))
def startStreamingOnCamChange(pin, value):
    setStreamURL(pin, value)


@blynk.handle_event("write V{}".format(config.QUALITY_SELECT_PIN))
def startStreamingOnQualityChange(pin, value):
    setStreamURL(pin, value)


# Run once on start and every 60 mins
@timer.register(vpin_num=config.WIFI_2G_PIN, interval=5, run_once=False)
@timer.register(vpin_num=config.WIFI_2G_PIN, interval=1, run_once=True)
def sendWiFiStatus(vpin_num=config.WIFI_2G_PIN):
    status = SystemFunctions().getWiFiStatus()
    if DEBUG_MODE:
        print("Got WiFi Status: {}".format(status))
    blynk.virtual_write(config.WIFI_2G_PIN, int(
        SystemFunctions().getWiFiStatus()))


def setStreamURL(pin, value):
    camera = skill.get("V50")
    quality = skill.get("V51")
    url = "rtsp://admin:admin@ftm.ddns.net:554/cam/realmonitor?channel=" + \
        str(camera) + "&subtype=" + str(int(quality)-1)
    if DEBUG_MODE:
        print("Setting Streaming URL: {}".format(url))
    blynk.set_property(53, "url", url)


while True:
    blynk.run()
    timer.run()
