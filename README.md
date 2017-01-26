# Stowaway

A real-time sensor data logger, originally developed for containers monitoring.

## Raspberry Pi 3 initial config

Download Raspbian minimal image, extract it and burn it to the micro-SD card (make sure you select the appropriate output device!):

    dd bs=4M if=2017-01-11-raspbian-jessie.img of=/dev/sdd
    sync

Connect a keyboard and a display to the Raspberry and boot from the micro-SD card. Login as `pi` with password `raspberry`. Then:

    sudo raspi-config

- Select the `Expand Filesystem` option.
- Under `Advanced Options`:
  - Enable SSH.
  - Enable I2C.

Reboot.

Make sure to change your default password with `passwd` and add your public key to `.ssh/authorized_keys`. Check that you are able to log in through SSH without needing to enter the password and then disable SSH login with password:

    sudo sed '/PasswordAuthentication yes/s/.*/PasswordAuthentication no/' /etc/ssh/sshd_config | grep PasswordAuthentication
    sudo systemctl restart ssh.service

Upgrade and install dependencies:

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install git i2c-tools

Download and install Miniconda:

    wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh
    # Make sure you verify the checksum at https://repo.continuum.io/miniconda/
    chmod +x chmod +x Miniconda3-latest-Linux-armv7l.sh
    ./Miniconda3-latest-Linux-armv7l.sh

Log out and back in (close and reopen SSH session). You may also want to delete the script you just downloaded.

Then, allow `pi` user to access I2C:

    sudo adduser pi i2c

Log out and back in (close and reopen SSH session).

Verify that the user is able to detect the I2C interface. First list the available I2C interfaces and then take the I2C interface name and test it:

    i2cdetect -y $(i2cdetect -l | awk '{ print $3 }')

If everything went well, the output should look like this:

         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- --
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    70: -- -- -- -- -- -- -- --

Now, let us create a virtual environment for the project:

    conda create -n stowaway python=3
    source activate stowaway

Clone the project and create a virtual environment:

    git clone https://github.com/CojoCompany/stowaway.git
    cd stowaway

Then, within the virtual environment, install the required packages:

    pip install --upgrade pip
    pip install -r requirements.txt
