Setting up python env and installing needed libraries.

python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install esptool
python -m esptool version


1a. Detecting the esp32

1b.Confirming esp32 communicates with laptop . Got an error : 

python -m esptool --chip esp32 --port COM8 --baud 115200 chip_id
Running the above command we got an error that port is busy , we fixed it by closing thonny ide and device manager that were keeping the port com8 busy : 

2a.Erasing the flash on esp32
cd .\firmware\physical\
python -m esptool --chip esp32 --port COM8 --baud 115200 erase_flash

2b.Setting up new micropython firmware: 
python -m esptool --chip esp32 --port COM8 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC.bin
firmware was stored in /firmware/physical

3a. OLED test error : 
The OLED display was added for local device output. During physical testing, the ESP32 successfully flashed MicroPython and executed the OLED driver code. However, I2C scanning returned abnormal results, detecting nearly all addresses instead of the expected sh1106 address 0x3C. 

3b.OLED test fix :
We realized it was a wiring issue and after fixing it the OLED was successfully detected using I2C scan.
Oled was handled by oled_display.py

4a.DHT22 error
We connected the complete circuit adding the : pH , dht22 and soil moisture sensors . Also added the code . We got an error where the DHT22 readings were not being detected

4b.DHT22 error fix
We realized it was a physical connection flaw and we corrected it . full proper readings were able to be read.
Sensors were handled by sensors.py 

5a.Wifi error
We had an error where wifi was not connecting .

5b.Wifi error fix 
We realized it was a code issue where we mistyped the ip address of the laptop which was hotspotting.We fixed this and wifi connected successfully.
Wifi was handled by wifi_manager.py

6a.Starting MQTT message broker
We ran this command together with adding some local mosquitto configs(listener 1883 0.0.0.0
allow_anonymous true ) to be able to start the mosquito broker : 
(venv) PS C:\Users\emman\Development\Group2-IOT-Semester-Project> & "C:\Program Files\mosquitto\mosquitto.exe" -c "C:\Users\emman\Development\Group2-IOT-Semester-Project\mosquitto-local.conf" -v
The above command failed but once we ran it as an administrator it worked.

6b.MQTT subscribing setup on powershell
MQTT subscribing from powershell : 
(venv) PS C:\Users\emman\Development\Group2-IOT-Semester-Project> & "C:\Program Files\mosquitto\mosquitto_sub.exe" -h 127.0.0.1 -p 1883 -t "iot/group2/project" -v
We ran the above command so that mqtt could subscribe to messages being sent from the esp32 to the local pc via the localhost ip address.
To publish from mqtt , setup wifi & oled , and test pin connections . we ran main.py . MQTT was handled in mqtt_manager.py

7.Firebase publishing
We setup a firebase realtime database to capture realtime data streams and stored them in firestore with timestamps for future fetching and persistent storage . We sent up to 30 readings.
Was handled by firebase_client.py

config.py stored all configuration variables

Other steps : 
8.Wokwi circuit creation to prototype the circuit : /firmware/wokwi


