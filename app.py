from flask import Flask
from flask import request
app = Flask(__name__)
import json
from flask import render_template
from flask import send_file
import time

# For now this server will only generate one file at a time due to compiling issues with a manditory file users_
# defines file.
lock = False

MY_BINDING_PHRASE = "default ExpressLRS binding phrase"
Regulatory = "-DRegulatory_Domain_FCC_915"
switches = False               # -DHYBRID_SWITCHES_8 # Improves Inital Syncing/Binding Speed (Currently Experimental)
fastSync = True                # -DFAST_SYNC
r9mPower = False               # -DR9M_UNLOCK_HIGHER_POWER# unlocks >250mw output power for R9M (Fan mod suggested:
syncOnArm = False              # -DNO_SYNC_ON_ARM
armChannel = "AUX1"            # -DARM_CHANNEL=AUX1
featureOpenTXSync = True       # -DFEATURE_OPENTX_SYNC_AUTOTUNE
lockOnFirstConnection = False  # -DLOCK_ON_FIRST_CONNECTION
lockOn50hz = False             # -DLOCK_ON_50HZ
uartInverted = True            # -DUART_INVERTED
r9mmR9miniSBUS = True          # -DUSE_R9MM_R9MINI_SBUS
autoWifiOnBoot = True          # -DAUTO_WIFI_ON_BOOT
useESP8266backpack = False     # -DUSE_ESP8266_BACKPACK
justBeepOnce = False           # -DJUST_BEEP_ONCE
myStartupMelody = ""           # -DMY_STARTUP_MELODY="B5 16 P16 B5 16 P16 B5 16 P16 B5 2 G5 2 A5 2 B5 8 P4 A5 8 B5 1|140|-3"
use500hz = False               # -DUSE_500HZ


def CreateUserDefines(options):
    options['MY_BINDING_PHRASE']
    f = open("user_defines.txt", "w+")
    f.write("-DMY_BINDING_PHRASE=\"" + str(options['MY_BINDING_PHRASE']) + "\"")
    f.write("\n")

    f.write(str(options['regulatory']))
    f.write("\n")

    if str(options['HYBRID_SWITCHES_8']) == "True":
        f.write("-DHYBRID_SWITCHES_8")
        f.write("\n")

    if str(options['FAST_SYNC']) == "True":
        f.write("-DFAST_SYNC ")
        f.write("\n")

    if str(options['R9M_UNLOCK_HIGHER_POWER']) == "True":
        f.write("-DR9M_UNLOCK_HIGHER_POWER")
        f.write("\n")

    if str(options['NO_SYNC_ON_ARM']) == "True":
        f.write("-DNO_SYNC_ON_ARM")
        f.write("\n")

    if str(options['ARM_CHANNEL']) != "":
        f.write("-DARM_CHANNEL=\"" + str(options['ARM_CHANNEL']) + "\"")
        f.write("\n")

    if str(options['FEATURE_OPENTX_SYNC']) == "True":
        f.write("-DFEATURE_OPENTX_SYNC")
        f.write("\n")

    if str(options['FEATURE_OPENTX_SYNC_AUTOTUNE']) == "True":
        f.write("-DFEATURE_OPENTX_SYNC_AUTOTUNE")
        f.write("\n")

    if str(options['LOCK_ON_FIRST_CONNECTION']) == "True":
        f.write("-DLOCK_ON_FIRST_CONNECTION")
        f.write("\n")

    if str(options['LOCK_ON_50HZ']) == "True":
        f.write("-DLOCK_ON_50HZ")
        f.write("\n")

    if str(options['UART_INVERTED']) == "True":
        f.write("-DUART_INVERTED")
        f.write("\n")

    if str(options['USE_R9MM_R9MINI_SBUS']) == "True":
        f.write("-DUSE_R9MM_R9MINI_SBUS")
        f.write("\n")

    if str(options['AUTO_WIFI_ON_BOOT']) == "True":
        f.write("-DAUTO_WIFI_ON_BOOT")
        f.write("\n")

    if str(options['USE_ESP8266_BACKPACK']) == "True":
        f.write("-DUSE_ESP8266_BACKPACK")
        f.write("\n")

    if str(options['JUST_BEEP_ONCE']) == "True":
        f.write("-DJUST_BEEP_ONCE")
        f.write("\n")

    if str(options['MY_STARTUP_MELODY']) != "":
        f.write("-DMY_STARTUP_MELODY=\"" + str(options['MY_STARTUP_MELODY']) + "\"")
        f.write("\n")

    if str(options['USE_500HZ']) != "":
        f.write("-DUSE_500HZ")
        f.write("\n")
    f.close()
    time.sleep(10)

@app.route('/<options>')
def hello(options):
    global lock
    option_dict = json.loads(options)
    if lock:
        return render_template('page.html'), 429

    # Do some catch here to check for json shit....
    # GOD DAMN MOTHER FUCKERS wanted a back end server

    lock = True
    CreateUserDefines(option_dict)
    lock = False

    try:
        return send_file('./user_defines.txt',
                         attachment_filename='user_defines.txt')
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


# {
#   "MY_BINDING_PHRASE": "default ExpressLRS binding phrase",
#   "regulatory": "-DRegulatory_Domain_FCC_915",
#   "HYBRID_SWITCHES_8": "False",
#   "FAST_SYNC": "True",
#   "R9M_UNLOCK_HIGHER_POWER": "False",
#   "NO_SYNC_ON_ARM": "False",
#   "ARM_CHANNEL=AUX1": "False",
#   "FEATURE_OPENTX_SYNC": "True",
#   "FEATURE_OPENTX_SYNC_AUTOTUNE": "False",
#   "LOCK_ON_FIRST_CONNECTION": "False",
#   "LOCK_ON_50HZ": "False",
#   "UART_INVERTED": "True",
#   "USE_R9MM_R9MINI_SBUS": "False",
#   "AUTO_WIFI_ON_BOOT": "True",
#   "USE_ESP8266_BACKPACK": "False",
#   "JUST_BEEP_ONCE": "False",
#   "MY_STARTUP_MELODY": "B5 16 P16 B5 16 P16 B5 16 P16 B5 2 G5 2 A5 2 B5 8 P4 A5 8 B5 1|140|-3",
#   "USE_500HZ": "False"
# }