#!/bin/sh -e
sudo bash -c 'echo -1 > /sys/module/usbcore/parameters/autosuspend'

sudo bash -c 'echo 0 > /sys/devices/system/cpu/cpuquiet/tegra_cpuquiet/enable'
sudo bash -c 'echo 1 > /sys/devices/system/cpu/cpu0/online'
sudo bash -c 'echo 1 > /sys/devices/system/cpu/cpu1/online'
sudo bash -c 'echo 1 > /sys/devices/system/cpu/cpu2/online'
sudo bash -c 'echo 1 > /sys/devices/system/cpu/cpu3/online'
sudo bash -c 'echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor'

sudo resetusb

python camera/main.py
python speech/main.py
