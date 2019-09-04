# Glenair Conduit Fatigue Tester

The graphical user interface (GUI) and motion control for Glenair conduit fatigue testing.

## Getting Started

Follow these instructions to get a new copy of the project up and running on a Raspberry Pi. Necessary if the files are wiped or the SD card becomes corrupted.

### Prerequisites

Connect the Raspberry Pi to Wi-Fi using the icon in the upper right hand corner of the Desktop. Alternatively, open the control box and use the ethernet port to create a wired internet connection.

Ensure the Raspberry Pi software is up to date by opening the Terminal window and entering these commands one by one. _This may take a few minutes to complete._

    sudo apt-get update
    sudo apt-get upgrade
    sudo reboot

After rebooting, enter this command in the Terminal to download guizero, a simple GUI creator for Python.

    sudo apt-get install python-guizero

Create a folder for the project files on the Desktop named "Glenair". In the Terminal, enter this command to navigate to the new directory.

    cd Desktop/Glenair

Follow with these commands to install the TMCL serial interface created by NativeDesign.

    git clone https://github.com/NativeDesign/python-tmcl.git
    python setup.py install
    
At this point, all files in the Glenair folder may be moved to trash with the exception of the folder named "TMCL". _This is an optional step._
    
### Installing

While still in the Glenair directory, enter this command in the Terminal to download the GUI repository.

    git clone https://github.com/kyliefern/glenair-conduit.git

In order to create a Desktop shortcut for running the interface, move the file named "glenairtest.desktop" from the Glenair folder to the Desktop and the icon will appear.

To initialize the On/Off switch for the Raspberry Pi, enter this command in the Terminal.

    sudo nano /etc/rc.local
    
Add this line right above "exit 0".

    python3 /home/pi/Desktop/Glenair/switch.py &
    
Press Ctrl-X, Y, and Enter to save and exit. The switch will not be active until the Raspberry Pi is rebooted again.

## Running Tests

At this point, the software is capable of running tests. Should the GUI need to be altered, make changes to the file named "conduitgui.py". If the motors are not being set up correctly, check the file named "motorsetup.py" for errors.

### Demo

In order to check motor functionality, a simple test may be run by entering this command in the Terminal.

    python3 Desktop/Glenair/motortest.py
    
The motors should take turns rotating 180 degrees four times.

### Fatigue Test

Double-clicking on the Conduit Test icon will open the GUI and allow for parameter selection and test control. Futher information is available in the project documentation.

## Author

Kylie Fernandez

Questions? Email kylie_fern@yahoo.com
