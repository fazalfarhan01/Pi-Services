from gpiozero import CPUTemperature
import blynklib, blynktimer

from IPTools import IPTools

# importing configuration file
import config

blynk = blynklib.Blynk(config.BLYNK_AUTH, server=config.SERVER_NAME, port=config.SERVER_PORT)
timer = blynktimer.Timer()


DEBUG_MODE = True


@timer.register(vpin_num=config.TEMP_PIN, interval=1, run_once=False)
def writeCPUTemp(vpin_num = config.TEMP_PIN):
    temp = CPUTemperature().temperature
    blynk.virtual_write(vpin_num, temp)
    if DEBUG_MODE:
        print("Sending CPU Temp to pin \tV{}\t{}".format(vpin_num, temp))

@timer.register(vpin_num=config.LOCAL_IP_PIN, interval=20, run_once=False)
def writeLocalIP(vpin_num = config.LOCAL_IP_PIN):
    IP = IPTools().getLocalIP()
    blynk.virtual_write(vpin_num, IP)
    if DEBUG_MODE:
        print("Sending Local IP Addrs to pin \tV{}\t{}".format(vpin_num, IP))

@timer.register(vpin_num=config.PUBLIC_IP_PIN, interval=1, run_once=True)
@timer.register(vpin_num=config.PUBLIC_IP_PIN, interval=60, run_once=False)
def writePublicIP(vpin_num = config.PUBLIC_IP_PIN):
    IP = IPTools().getPublicIP()
    blynk.virtual_write(vpin_num, IP)
    if DEBUG_MODE:
        print("Sending Public IP Addrs to pin \tV{}\t{}".format(vpin_num, IP))

@blynk.handle_event("write V{}".format(config.UPDATE_PIN))
def performUpdate(pin, value):
    if value[0] == "1":
        blynk.notify("Performing Updates.\n\nPlease Wait..!")
    if DEBUG_MODE:
        print("Got Update Request on pin \tV{}\t{}".format(pin, value[0]))

@blynk.handle_event("write V{}".format(config.BACKUP_PIN))
def performBackup(pin, value):
    if value[0] == "1":
        blynk.notify("Performing Backup.\n\nPlease Wait..!")
    if DEBUG_MODE:
        print("Got Backup Request on pin \tV{}\t{}".format(pin, value[0]))

@blynk.handle_event("write V{}".format(config.SHUTDOWN_PIN))
def performShutdown(pin, value):
    if value[0] == "100":
        blynk.notify("Turning off RPi4!")
        blynk.virtual_write(pin, 0)
    if DEBUG_MODE:
        print("Got Shutdown Request on pin \tV{}\t{}".format(pin, value[0]))

@blynk.handle_event("write V{}".format(config.RESTART_PIN))
def performRestart(pin, value):
    if value[0] == "100":
        blynk.notify("Restarting RPi4!")
        blynk.virtual_write(pin, 0)
    if DEBUG_MODE:
        print("Got Restart Request on pin \tV{}\t{}".format(pin, value[0]))

while True:
    blynk.run()
    timer.run()