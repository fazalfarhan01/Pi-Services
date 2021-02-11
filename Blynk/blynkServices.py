#!/usr/bin/python3
from TPLinkController import TP_Link_Controller
import sys
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


blynk = blynklib.Blynk(
    config.BLYNK_AUTH, server=config.SERVER_NAME, port=config.SERVER_PORT)
timer = blynktimer.Timer()


DEBUG_MODE = True

wifi_5g_status = None
wifi_2g_status = None


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
# @timer.register(vpin_num=config.WiFi_2G_STATUS_PIN, interval=60*60, run_once=False)
@timer.register(vpin_num=config.WiFi_2G_STATUS_PIN, interval=1, run_once=True)
def sendWiFiStatus(vpin_num=config.WiFi_2G_STATUS_PIN):
    threading.Thread(name="WiFi Status", target=setWiFiStatus).start()


def setStreamURL(pin, value):
    camera = skill.get("V50")
    quality = skill.get("V51")
    url = "rtsp://admin:admin@ftm.ddns.net:554/cam/realmonitor?channel=" + \
        str(camera) + "&subtype=" + str(int(quality)-1)
    if DEBUG_MODE:
        print("Setting Streaming URL: {}".format(url))
    blynk.set_property(53, "url", url)


def setWiFiStatus():
    global wifi_2g_status, wifi_5g_status
    try:
        tplink = TP_Link_Controller(
            config.TP_LINK_LOGIN_EMAIL, config.TP_LINK_LOGIN_PASSWORD, DEBUG_MODE=DEBUG_MODE)
        tplink.login()
        response = tplink.get_status()
        wifi_2g_status = response["data"]["wireless_2g_enable"].upper()
        wifi_5g_status = response["data"]["wireless_5g_enable"].upper()
        if DEBUG_MODE:
            print("Setting 2G WiFi Status: {}".format(wifi_2g_status))
            print("Setting 5G WiFi Status: {}".format(wifi_5g_status))
        blynk.virtual_write(config.WiFi_2G_STATUS_PIN, wifi_2g_status)
        blynk.virtual_write(config.WiFi_5G_STATUS_PIN, wifi_5g_status)
        tplink.close()
    except:
        tplink.close()
        sendWiFiStatus()


def toggleWifi(mode):
    global wifi_5g_status, wifi_2g_status
    while True:
        # Keep Trying until Success
        try:
            tplink = TP_Link_Controller(config.TP_LINK_LOGIN_EMAIL, config.TP_LINK_LOGIN_PASSWORD, DEBUG_MODE=DEBUG_MODE)
            tplink.login()
            if mode == "5G":
                tplink.toggle_5g_wifi()
                print("5G WiFi Toggeled")
                if wifi_5g_status == "ON":
                    wifi_5g_status = "OFF"
                else:
                    wifi_5g_status = "ON"
                blynk.virtual_write(config.WiFi_5G_STATUS_PIN, wifi_5g_status)
            else:
                tplink.toggle_2g_wifi()
                print("2G WiFi Toggeled")
                if wifi_2g_status == "ON":
                    wifi_2g_status = "OFF"
                else:
                    wifi_2g_status = "ON"
                blynk.virtual_write(config.WiFi_2G_STATUS_PIN, wifi_2g_status)
            tplink.close()
            blynk.notify("Success..!")
            break
        except:
            # blynk.notify(
            #     "Error occured!\nError: {}\nContact Developer.".format(sys.exc_info()[0]))
            blynk.notify("Error Occured..!\n\nPlease Wait. Retrying!")


while True:
    blynk.run()
    timer.run()
