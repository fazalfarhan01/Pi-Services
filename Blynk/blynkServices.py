#!/usr/bin/python3
from gpiozero import CPUTemperature
import blynklib
import blynktimer

from IPTools import IPTools
from systemFunction import SystemFunctions

import threading

# importing configuration file
import config

from BlynkSkill import BlynkSkill
skill = BlynkSkill()

import sys

from TPLinkController import TP_Link_Controller

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


@blynk.handle_event("write V{}".format(config.WiFi_5G_PIN))
def toggle5GWiFi(pin, value):
    if value[0] == "1":
        blynk.notify("Toggling 5G WiFi")
        threading.Thread(name="toggle 5G", target=toggleWifi,
                         args=["5G"]).start()
    if DEBUG_MODE:
        print("Got Toggle 5G WiFi Request on pin \tV{}\t{}".format(
            pin, value[0]))


@blynk.handle_event("write V{}".format(config.WiFi_2G_PIN))
def toggle2GWiFi(pin, value):
    if value[0] == "1":
        blynk.notify("Toggling 2G WiFi")
        threading.Thread(name="toggle 2G", target=toggleWifi,
                         args=["2G"]).start()
    if DEBUG_MODE:
        print("Got Toggle 2G WiFi Request on pin \tV{}\t{}".format(
            pin, value[0]))


def toggleWifi(mode):
    while True:
        # Keep Trying until Success
        try:
            tplink = TP_Link_Controller(
                "fazal.farhan@gmail.com", "mohamedfarhan12", DEBUG_MODE=True)
            tplink.login()
            if mode == "5G":
                tplink.toggle_5g_wifi()
                print("5G WiFi")
            else:
                tplink.toggle_2g_wifi()
                print("2G WiFi")
            tplink.close()
            blynk.notify("Success..!")
            break
        except:
            # blynk.notify(
            #     "Error occured!\nError: {}\nContact Developer.".format(sys.exc_info()[0]))
            blynk.notify("Error Occured..!\n\nPlease Wait. Retrying!")


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
    

def setStreamURL(pin, value):
    camera = skill.get("V50")
    quality = skill.get("V51")
    url = "rtsp://admin:admin@ftm.ddns.net:554/cam/realmonitor?channel=" + str(camera) + "&subtype=" + str(int(quality)-1)
    if DEBUG_MODE:
        print("Setting Streaming URL: {}".format(url))
    blynk.set_property(53, "url", url)

while True:
    blynk.run()
    timer.run()
