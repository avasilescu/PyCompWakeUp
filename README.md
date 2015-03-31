PyCompWakeUp
============

##Summary

PyCompWakeUp is a Python script that is designed to run on a computer or RaspberryPi to wake up a computer not connected to the network via an ethernet cable. 

##Problem Statement

I wanted to wake up my desktop but it is not connect to my router via an ethernet cable. Instead, the desktop connects to the router via a USB WiFi adapter. The USB WiFi cannot wake up the computer. With a RaspberryPi (RPi) connected to the desktop via an ethernet cable, the RPi can send the Wake-On-Lan (WOL) message, also known as "Magic Packet". The RPi is connected to the network via a WiFi adapter. The only thing missing is how to trigger the RPi to send the Magic Packet. Hence, PyCompWakeUp.

##Concept of Operation

RaspberryPi checks an email address looking for a specific email, over WiFi. When it receives this email, it will send a WOL signal to the desktop over ethernet, resulting in turning on the desktop. Gmail is used to filter email and label it. 

##File Structure

- source
  - CompWakeUp.conf
  - CompWakeUp.py
- README.md

##Software to Install

The following software needs to be installed for PyCompWakeUp to work. The commands that follow are to install the software in a Debian based environment (Ubuntu, Raspian, etc).
- wakeonlan - sudo apt-get install wakeonlan
- samba-common-bin - sudo apt-get install samba-common-bin

##Setting up Email

These instructions assume that Gmail is used. Create a filter that looks for a specific email address and subject line and labels the email. For example, the specific email address is "personalemail@gmail.com". The specific email subject line is  "WOL Comp". The filter is to label these emails with a label "WOL Comp". The specific email address and subject line become white lists. The Python script will only check for specific labels, in this example "WOL Comp". 