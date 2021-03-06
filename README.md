# CarTripComputer
On / Off Car Trip Timer with upcoming weather and internal car conditions monitor

#### Flashing RaspberriPi Hard Disk / Install Required Software (Using Ubuntu Linux)

Download "RASPBIAN JESSIE LITE"
https://www.raspberrypi.org/downloads/raspbian/

**Create your new hard disk for DashboardPI**
>Insert the microSD to your computer via USB adapter and create the disk image using the `dd` command
>
> Locate your inserted microSD card via the `df -h` command, unmount it and create the disk image with the disk copy `dd` command
>
> $ `df -h`
> */dev/sdb1       7.4G   32K  7.4G   1% /media/XXX/1234-5678*
>
> $ `umount /dev/sdb1`
>
> **Caution: be sure the command is completely accurate, you can damage other disks with this command**
>
> *if=location of RASPBIAN JESSIE LITE image file*
> *of=location of your microSD card*
>
> $ `sudo dd bs=4M if=/path/to/raspbian-jessie-lite.img of=/dev/sdb`
> *(note: in this case, it's /dev/sdb, /dev/sdb1 was an existing factory partition on the microSD)*

**Setting up your RaspberriPi**

*Insert your new microSD card to the raspberrypi and power it on with a monitor connected to the HDMI port*

Login
> user: **pi**
> pass: **raspberry**

Change your account password for security
>`sudo passwd pi`

Enable RaspberriPi Advanced Options
>`sudo raspi-config`

Choose:
`1 Expand File System`

`9 Advanced Options`
>`A2 Hostname`
>*change it to "CarTripComputer"*
>
>`A4 SSH`
>*Enable SSH Server*
>
>`A7 I2C`
>*Enable i2c interface*

**Enable the English/US Keyboard**

>`sudo nano /etc/default/keyboard`

> Change the following line:
>`XKBLAYOUT="us"`

**Reboot PI for Keyboard layout changes / file system resizing to take effect**
>$ `sudo shutdown -r now`

**Auto-Connect to your WiFi**

>`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

Add the following lines to have your raspberrypi automatically connect to your home WiFi
*(if your wireless network is named "linksys" for example, in the following example)*

	network={
	   ssid="linksys"
	   psk="WIRELESS PASSWORD HERE"
	}

**Reboot PI to connect to WiFi network**

>$ `sudo shutdown -r now`
>
>Now that your PI is finally on the local network, you can login remotely to it via SSH.
>But first you need to get the IP address it currently has.
>
>$ `ifconfig`
>*Look for "inet addr: 192.168.XXX.XXX" in the following command's output for your PI's IP Address*

**Go to another machine and login to your raspberrypi via ssh**

> $ `ssh pi@192.168.XXX.XXX`

**Start Installing required packages**

>$ `sudo apt-get update`
>
>$ `sudo apt-get upgrade`
>
>$ `sudo apt-get install vim git python-smbus i2c-tools python-imaging python-smbus build-essential python-dev rpi.gpio python3 python3-pip python-gpiozero python-psutil`

**Update local timezone settings**

>$ `sudo dpkg-reconfigure tzdata`

> select your timezone using the interface

**Setup the simple directory `l` command [optional]**

>$ `vi ~/.bashrc`
>
>*add the following line:*
>
>$ `alias l='ls -lh'`
>
>$ `source ~/.bashrc`

**Fix VIM default syntax highlighting [optional]**

>$ `sudo vi /etc/vim/vimrc`
>
>uncomment the following line:
>
>_syntax on_

**Clone Clock repository**

>$ `cd ~`
>
>$ `git clone https://github.com/khinds10/CarTripComputer.git`

**DHT22 Install**

>$ `cd ~`
>
>$ `git clone https://github.com/adafruit/Adafruit_Python_DHT.git`
>
>$ `cd Adafruit_Python_DHT/`
>
>$ `sudo python setup.py install`
>
>$ `sudo python ez_setup.py`
>
>$ `cd examples/`
>
>$ `vi simpletest.py`
>

Change the following line:
> sensor = Adafruit_DHT.DHT22

Comment the line out
> pin = 'P8_11'

Uncomment the line and change the pin number to 17
> pin = 17

Run the test

`python simpletest.py`

> You should see a metric reading of Temp and Humidity displayed on the command line.

## Supplies Needed

**DHT22 Humidistat**

**Momentary Pushbutton**

**2.6" Digole Display**

![Digole Display](https://raw.githubusercontent.com/khinds10/EnvironmentClock/master/images/display.png "Digole Display")

**RaspberriPi Zero**

![Pi Zero](https://raw.githubusercontent.com/khinds10/EnvironmentClock/master/images/pizero.jpg "Pi Zero")

## Build and wire the device

**1) Prepare the Digole Display for i2C**

On the back of the Digole Display, solder the jumper to assign the display to use the i2c protocol
![i2c Jumper Digole](https://raw.githubusercontent.com/khinds10/EnvironmentClock/master/images/display-back.png "i2c Jumper Digole")

**2) Print the Project Enclosure**

Using a 3D printer print the enclosure files included in the 'enclosure/' folder.
.x3g files are MakerBot compatible.  You can also use the .stl and .blend (Blender Program) files to edit and create your own improvements to the design.

**6) Begin wiring the unit using the wiring diagram below as a guide.**

**Digole Display**

> GND -> GND
>
> DATA -> SDA
>
> CLK -> SCL
>
> VCC -> 3V

**DHT22 Humidistat**

> VCC -> 5V
>
> GND -> GND
>
> DATA -> GPIO 17 / PIN 11

**Push Button**

> GND -> GND
>
> GPIO 18 / PIN 36


## Configure Application to run correctly in settings.py config file

Find the file `settings.py` and adjust to your current settings

> \# forecast.io API key for local weather information
>
> weatherAPIURL = 'https://api.forecast.io/forecast/'
>
> weatherAPIKey = 'YOUR API KEY FOR FORECAST.IO'
> 
> \# optional for running the remote temp/humidity logger
>
> deviceLoggerAPI = 'mydevicelogger.com'
>
> \# search google to get the Latitude/Longitude for your home location
>
> latitude = 41.4552578
>
> longitude = -72.1665444
>

## Setup Startup Scripts

>$ `crontab -e`

Add the following lines:

`@reboot nohup python /home/pi/CarTripComputer/button.py >/dev/null 2>&1`

`@reboot nohup python /home/pi/CarTripComputer/status.py >/dev/null 2>&1`

`@reboot nohup python /home/pi/CarTripComputer/weather.py >/dev/null 2>&1`

Verify the display starts working on reboot

>$ `sudo reboot`

## Temp Logger to API script each 10 minutes

>$ `crontab -e`

Add the following lines:

`*/10 * * * * python /home/pi/CarTripComputer/temp-check.py`

## OPTIONAL: Creating your own weather images to render on the display

Upload your own 128x128 file to the following URL:

http://www.digole.com/tools/PicturetoC_Hex_converter.php 

Choose your image file to upload, add what size you want it to be on the screen (Width/Height)

Select "256 Color for Color OLED/LCD(1 byte/pixel)" in the "Used for" dropdown

Obtain the hex output.

Add the hex output to a display/build/ header (.h) file, use the other ones as guides for syntax.

Include the new file in the digole.c file 
`#include "myimage.h`

Include a new command line hook to your image file in the.
_Note: the command below is saying draw your image at position 10 pixels over 10  pixels down. You can change it to different X,Y coordinates, you can also change the values 128,128 to whatever size your new image actually is._

`} else if (strcmp(digoleCommand, "myimage") == 0) {`
    `drawBitmap256(10, 10, 128, 128, &myimageVariableHere,0);  // myimageVariableHere is defined in your (.h) file`
`}`

Now rebuild (ignore the errors) below to have your new image render with the following command.
>$ `./digole myimage`

**Re-Building [Included] Digole Display Driver for your optional changes**

>$ `cd display/build`

>$ `gcc digole.c`

>$ `mv a.out ../../digole`

>$ `chmod +x ../../digole`
