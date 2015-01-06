PyCompWakeUp
============

##Summary

PyCompWakeUp is a Python script that is designed to run on a computer or RaspberryPi to wake up a computer not connected to the network via an ethernet cable. 

##Problem Statement

I wanted to wake up my desktop but it is not connect to my router via an ethernet cable. Instead, the desktop connects to the router via a USB WiFi adapter. With a RaspberryPi (RPi) connected to the desktop via an ethernet cable, the RPi can send the Wake-On-Lan (WOL) message, also known as "Magic Packet". The RPi is connected to the network via a WiFi adapter. The only thing missing is how to trigger the RPi to send the Magic Packet. Hence, PyCompWakeUp.