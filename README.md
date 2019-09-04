# Glenair Conduit Fatigue Tester

The graphical user interface (GUI) and motion control for Glenair conduit fatigue testing.

## Getting Started

Follow these instructions to get a new copy of the project up and running on a Raspberry Pi. Necessary if the files are wiped or the SD card becomes corrupted.

### Prerequisites

Connect the Raspberry Pi to Wi-Fi using the icon in the upper right hand corner of the desktop. Alternatively, open the control box and use the ethernet port to create a wired internet connection.

Ensure the Raspberry Pi software is up to date by entering these commands one by one in a terminal window. _This may take a few minutes to complete._

    sudo apt-get update
    sudo apt-get upgrade
    sudo reboot

Create a folder for the project files on the Desktop named "Glenair". In a terminal, enter this command to navigate to the new directory.

    cd /home/pi/Desktop/Glenair

Follow with these commands to install the TMCL serial interface created by NativeDesign and guizero, a simple GUI creator for Python.

    git clone https://github.com/NativeDesign/python-tmcl.git
    python setup.py install
    sudo apt-get install python-guizero
    
### Installing

While still in the project folder directory, enter this terminal command to download the GUI.

    git clone https://github.com/kyliefern/glenair-conduit.git

In order to create a desktop shortcut for running the interface, create an empty file named, "conduit_test.desktop" within the Desktop directory.

Add this text to the file,

    [Desktop Entry]
    Name=Conduit Test
    Icon=/usr/share/pixmaps/pstree32.xpm
    Exec=python3 conduitgui.py
    Type=Application
    Terminal=false
    
The shortcut icon should appear on the desktop.

## Running Tests

At this point, the software is capable of running tests. Should the GUI need to be altered, edit the file named conduitgui.py. If the motors are not being set up correctly, check the file motorsetup.py for errors.

### Demo

In order to check motor functionality, a simple test may be run by entering this command in a terminal.

    python3 /home/pi/Desktop/Glenair/motortest.py
    
The motors should take turns spinning a quarter revolution and back four times.

### Fatigue Test

Doubleclicking on the Conduit Test icon will open the GUI and allow for parameter selection and test control. Futher information is available in the project documentation.

## Author

Kylie Fernandez

Questions? Email kylie_fern@yahoo.com
