
# EMFIT Local API

There is a functional http server running on the device that can be crawled for realtime data. It runs on port 80 and uses plain http.

You will need to know the IP address if your emfit device.

## shortdvm.htm

For demoing / testing with a web browser there is an auto-refreshing page that contains only HR and RR values, it’s name is `shortdvm.htm`

You can access it via `http://<device-ip>/shortdvm.htm`

## dvmstatus.htm

HR, RR and activity values can be acquired by requesting `dvmstatus.htm` -page

You can access it via `http://<device-ip>/dvmstatus.htm`

Variable meanings on the page:
* **PRES** - Presence
* **SER** - Serial number of the device, 6 HEX characters (0..9,a..f)
* **TS** - Timestamp, UNIX time (seconds). This is zero if device has not acquired current time info from our server. For current firmware versions (t120v0.8.xx) it is normal this to be always zero.
* **TS_R** - Relative timestamp, seconds from device boot.
* **HR** - Heart rate in beats per minute.
* **RR** - Respiratory rate, per minute.
* **ACT** - Activity value. (unitless)

This information is present starting from firmware version t120v0.8.13, with basic set of variables. More variables have been added in later versions. 

Recommended polling interval for this page is **1-2 seconds**


## Discovery of the emfit device

If the Emfit device is in SoftAP/configuration mode then the page is easy to access by connecting the WiFi network provided by the device and navigating to `http://<device-ip>/dvmstatus.htm`

However, if the device is connected to some other WiFi network the device’s IP address must first be discovered. 

To discover the IP address of the device it send announce packets to broadcast address (on local area network) to UDP port 30371 have the following data (first 4 bytes are just a “key”-value):

    0x34, 0xA2, 0xD5, 0x83, Device_Serial_Byte0, Device_Serial_Byte1, Device_Serial_Byte2, Fw_TypeID, Fw_VersionID_A, FW_VersionID_B, FW_VersionID_C, Bootloader_Version_A,  Bootloader_Version_B,  Bootloader_Version_C.

Example; device serial number 000757, running firmware t120v0.8.14 and having boot-loader v1.0.3 will broadcast data:

    0x34 0xA2 0xD5 0x83 0x57 0x07 0x00 0x78 0x00 0x08 0x0E 0x01 0x00 0x03

The announce feature is present starting from firmware version t120v0.8.17. Device firmware version can be checked by navigating to factory setup -page, fcfg.htm. `http://<device-ip>/fcfg.htm`

To use the device announce feature to determine it’s IP one could for example use a free program called Packet Sender (http://packetsender.com). It has an option for UDP-server that can show the announce packets that Emfit Device will send. To use it for this purpose: Under settings enable UDP server and set port to 30371, the announcement packets will shortly show on the log-window  along with the device’s current IP address.

One could also use some WiFi router features to find out the IP address of the device based on it’s MAC address.

## Diagnostics

You can access device diagnostics by requesting `fdiag.htm` 

You can access it via `http://<device-ip>/fdiag.htm`

## Net config

You can access the original config dialog by requesting `netconfig.htm` 

You can access it via `http://<device-ip>/netconfig.htm`