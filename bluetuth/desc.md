# Bluetooth connection
The Raspberry Pi will create a bluetooth server. This bluetooth server will be used to send a panic signal from an Android phone. In case something goes wrong and we need to stop the vehicle, we'll press the big red button on the app, and the vehicle will stop and terminate the code.
It also allows to send the target coordinates to the vehicle.

## Warning
The current version doesn't work on Windows, only in Raspbian.

## Files
_blue_server.py_ is the server file that will run on the Raspberry Pi. _OpenMob.aia_ is the MIT App Inventor project of the Android app, and _OpenMob.apk_ is the source code to be installed in the device.

## Debugging
### ImportError: libbluetooth.so.3: cannot open shared object file: No such file or directory
Run the following:
```
sudo apt install libbluetooth-dev
```
### bluetooth.btcommon.BluetoothError: (2, 'No such file or directory')
https://stackoverflow.com/questions/36675931/bluetooth-btcommon-bluetootherror-2-no-such-file-or-directory
Read the whole post, all the way down.


## References
- https://github.com/pybluez/pybluez/blob/master/examples/simple/rfcomm-server.py
- https://github.com/dinohorvat/pybluez--rfcomm-server/blob/master/rfcomm-server.py
