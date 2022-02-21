# !/usr/bin/env python3

# Using an Arduino with Python LESSON 6: Analog Voltage Meter in vPython.
# https://www.youtube.com/watch?v=61VKJ64Bdks
# https://toptechboy.com/using-an-arduino-with-python-lesson-6-analog-voltage-meter-in-vpython/

# Internet References:
# https://www.glowscript.org/docs/VPythonDocs/index.html

import time
import serial
from vpython import *
import numpy as np

# vPython refresh rate.
vPythonRefreshRate = 100

# Draw the meter box.
meterBoxX = 2.5
meterBoxY = 1.5
meterBoxZ = 0.1
meterBox = box(color = color.white, opacity = 1, size = vector(meterBoxX, meterBoxY, meterBoxZ), pos = vector(0, 0.9 * meterBoxY / 2, -meterBoxZ))

# Draw the meter needle and set it to the 0 position.
meterNeedleL = 1.0
meterNeedleW = 0.02
meterNeedle = arrow(length = meterNeedleL, shaftwidth = meterNeedleW, color = color.red, axis = vector(meterNeedleL * np.cos(5 * np.pi / 6), meterNeedleL * np.sin(5 * np.pi / 6), 0))
meterNeedleBaseR = 0.05
meterNeedleBlob = sphere(radius = meterNeedleBaseR, color = color.red)
meterNeedleDisc = cylinder(color = color.gray(0.5), pos = vector(0, 3 * meterNeedleBaseR, -meterBoxZ / 2), axis = vector(0, 0, 0.01), radius = 4 * meterNeedleBaseR)

# Place the meter name.
myName = "Volts"
meterName = text(text = myName, color = color.blue, opacity = 1, align = "center", height = 0.1, pos = vector(0, meterNeedleL + 0.25, 0), axis = vector(1, 0, 0))

# Draw the meter scale major marks.
majTickL = 0.1
majTickW = 0.02
majTickH = 0.02
for unitCounter, theta in zip(range(6), np.linspace(5 * np.pi / 6, np.pi / 6, 6)):
    majorUnit = text(text = str(unitCounter), color = color.red, opacity = 1, align = "center", height = 0.1, pos = vector((meterNeedleL + 0.10) * np.cos(theta), (meterNeedleL + 0.10) * np.sin(theta), -0.025))
    majorUnit.rotate(angle = theta - np.pi / 2, axis = vector(0, 0, 1))
    majorTick = box(color = color.black, pos = vector(meterNeedleL * np.cos(theta), meterNeedleL * np.sin(theta), -0.025), size = vector(majTickL, majTickW, majTickH), axis = vector(meterNeedleL * np.cos(theta), meterNeedleL * np.sin(theta), 0))

# Draw the meter scale minor marks.
minTickL = 0.05
minTickW = 0.01
minTickH = 0.01
for unitCounter, theta in zip(range(51), np.linspace(5 * np.pi / 6, np.pi / 6, 51)):
    if unitCounter % 5 == 0 and unitCounter % 10 != 0:
        minorUnit = text(text = "5", color = color.red, opacity = 1, align = "center", height = 0.05, pos = vector((meterNeedleL + 0.05) * np.cos(theta), (meterNeedleL + 0.05) * np.sin(theta), -0.025))
        minorUnit.rotate(angle = theta - np.pi / 2, axis = vector(0, 0, 1))
    minorTick = box(color = color.black, pos = vector(meterNeedleL * np.cos(theta), meterNeedleL * np.sin(theta), -0.025), size = vector(minTickL, minTickW, minTickH), axis = vector(meterNeedleL * np.cos(theta), meterNeedleL * np.sin(theta), 0))

# Add a raw reading too.
rawValue = label(text = "0000", color = color.red, height = 10, opacity = 0, box = False, pos = vector(-0.9, meterNeedleL + 0.25, 0))
# Displaying the raw reading as a text object does initially work, but the text cannot be changed afterwards.
# rawValue = text(text = "0000", color = color.red, opacity = 1, align = "left", height = 0.1, pos = vector(-0.95 * meterScale, ((meterNeedleL + 0.25) * meterScale), 0))

# Add a digital reading too.
digitalValue = label(text = "0.00V", color = color.red, height = 10, opacity = 0, box = False, pos = vector(0.9, meterNeedleL + 0.25, 0))
# Displaying the raw reading as a text object does initially work, but the text cannot be changed afterwards.
# digitalValue = text(text = "0.00V", color = color.red, opacity = 1, align = "right", height = 0.1, pos = vector(0.95 * meterScale, ((meterNeedleL + 0.25) * meterScale), 0))

# Lets decorate the meter...
# Top Left corner screw.
screwTLHead = cylinder(color = color.black, pos = vector(-1.17, 1.34, -0.15), axis = vector(0,0 , 0.12), radius = 0.06)
screwTLShaft = cone(color = color.black, pos = vector(-1.17, 1.34, -0.15), axis = vector(0, 0, -0.3), radius = 0.05)
slotTLAngle1 = np.random.rand() * np.pi / 2 # An angle between 0 and 90 degrees.
slotTLAngle2 = slotTLAngle1 + np.pi / 2 # Add 90 degrees for the other part of the cross.
screwTLCross1 = box(color = vector(0.8, 0.8, 0.8), opacity = 1, pos = vector(-1.17, 1.34, -0.0399), size = vector(0.1, 0.02, 0.02))
screwTLCross1.rotate(angle = slotTLAngle1, axis = vector(0, 0, 1))
screwTLCross2 = box(color = vector(0.8, 0.8, 0.8), opacity = 1, pos = vector(-1.17, 1.34, -0.0399), size = vector(0.1, 0.02, 0.02))
screwTLCross2.rotate(angle = slotTLAngle2, axis = vector(0, 0, 1))
# Top Right corner screw.
screwTRHead = cylinder(color = color.black, pos = vector(1.17, 1.34, -0.15), axis = vector(0, 0, 0.12), radius = 0.06)
screwTRShaft = cone(color = color.black, pos = vector(1.17, 1.34, -0.15), axis = vector(0, 0, -0.3), radius= 0.05)
slotTRAngle1 = np.random.rand() * np.pi / 2 # An angle between 0 and 90 degrees.
slotTRAngle2 = slotTRAngle1 + np.pi / 2
screwTRCross1 = box(color = vector(0.8, 0.8, 0.8), opacity = 1, pos = vector(1.17, 1.34, -0.0399), size = vector(0.1, 0.02, 0.02))
screwTRCross1.rotate(angle = slotTRAngle1, axis = vector(0, 0, 1))
screwTRCross2 = box(color = vector(0.8, 0.8, 0.8), opacity = 1, pos = vector(1.17, 1.34, -0.0399), size = vector(0.1, 0.02, 0.02))
screwTRCross2.rotate(angle = slotTRAngle2, axis = vector(0, 0, 1))
# Bottom Left corner screw.
screwBLHead = cylinder(color = color.black, pos = vector(-1.17, 0, -0.15), axis = vector(0, 0, 0.12), radius = 0.06)
screwBLShaft = cone(color = color.black, pos = vector(-1.17, 0, -0.15), axis = vector(0, 0, -0.3), radius = 0.05)
slotBLAngle1 = np.random.rand() * np.pi / 2 # An angle between 0 and 90 degrees.
slotBLAngle2 = slotBLAngle1 + np.pi / 2
screwBLCross1 = box(color = vector(0.8, 0.8, 0.8), opacity = 1, pos = vector(-1.17, 0, -0.0399), size = vector(0.1, 0.02, 0.02))
screwBLCross1.rotate(angle = slotBLAngle1, axis = vector(0, 0, 1))
screwBLCross2 = box(color = vector(0.8, 0.8, 0.8), opacity = 1, pos = vector(-1.17, 0, -0.0399), size = vector(0.1, 0.02, 0.02))
screwBLCross2.rotate(angle = slotBLAngle2, axis = vector(0, 0, 1))
# Bottom Right corner screw.
screwBRHead = cylinder(color = color.black, pos = vector(1.17, 0, -0.15), axis = vector(0, 0, 0.12), radius = 0.06)
screwBRShaft = cone(color = color.black, pos = vector(1.17, 0, -0.15), axis = vector(0, 0, -0.3), radius = 0.05)
slotBRAngle1 = np.random.rand() * np.pi / 2 # An angle between 0 and 90 degrees.
slotBRAngle2 = slotBRAngle1 + np.pi / 2
screwBRCross1 = box(color = vector(0.8, 0.8, 0.8), opacity = 1, pos = vector(1.17, 0, -0.0399), size = vector(0.1, 0.02, 0.02))
screwBRCross1.rotate(angle = slotBRAngle1, axis = vector(0, 0, 1))
screwBRCross2 = box(color = vector(0.8, 0.8, 0.8), opacity = 1, pos = vector(1.17, 0, -0.0399), size = vector(0.1, 0.02, 0.02))
screwBRCross2.rotate(angle = slotBRAngle2, axis = vector(0, 0, 1))
# Lets put a mostly transparent glass cover over the meter.
meterCoverX = 2.5
meterCoverY = 1.5
meterCoverZ = 0.25
meterCover = box(color = color.white, opacity = 0.25, size = vector(meterCoverX, meterCoverY, meterCoverZ), pos = vector(0, 0.9 * meterCoverY / 2, 0))
# Now lets stamp my logo on the meter, "EasiFace". This is my logo - you need your own!
myLogo = "EasiFace"
for letterCounter, theta in zip(range(len(myLogo)), np.linspace(5 * np.pi / 8, 3 * np.pi / 8, len(myLogo))):
    logoLetter = myLogo[letterCounter]
    logoCharacter = text(text = logoLetter, color = color.green, opacity = 1, align = "center", height = 0.1, pos = vector((meterNeedleL - 0.25) * np.cos(theta), (meterNeedleL - 0.25) * np.sin(theta), -0.035), axis = vector(1, 0, 0))
    logoCharacter.rotate(angle = theta - np.pi / 2, axis = vector(0, 0, 1))
# Finally, lets mount it on a gray metal panel.
meterPanelX = 3.25
meterPanelY = 2.25
meterPanelZ = 0.1
meterPanel = box(color = color.gray(0.5), texture = textures.metal, size = vector(meterPanelX, meterPanelY, meterPanelZ), pos = vector(0, 0.6 * meterPanelY / 2, -meterPanelZ * 2))

# Connect to the Arduino on the correct serial port!
serialOK = True
try:
    # My Arduino happens to connect as serial port 'com3'. Yours may be different!
    arduinoDataStream = serial.Serial('com3', 115200)
    # Give the serial port time to connect.
    time.sleep(1)
except serial.SerialException as err:
    serialOK = False
    # Put an error message on top of the meter.
    serialErrorVisible = 0
    serialError = text(text = "-Serial Error-", color = color.red, opacity = serialErrorVisible, align = "center", height = 0.25, pos = vector(0, meterNeedleL / 2, 0), axis = vector(1, 0, 0))
    print("Serial Error: %s." % (str(err)[0].upper() + str(err)[1:])) # A cosmetic fix to uppercase the first letter of err.

# An infinite loop...
while True:
    # Set the vPython refresh rate.
    rate(vPythonRefreshRate)
    if serialOK:
        # Wait until data has been received from the Arduino.
        while arduinoDataStream.in_waiting == 0:
            pass
        # Read the data from the Arduino.
        arduinoDataPacket = arduinoDataStream.readline()
        # Convert the data from a byte stream to a string.
        arduinoDataPacket = str(arduinoDataPacket, 'utf-8')
        # Convert the string to a number.
        potValue = int(arduinoDataPacket.strip('\r\n'))
        # Print the raw potentiometer value.
        rawValue.text = str("<i>%04d</i>" % potValue)
        # Print the digital voltage.
        voltage = round(5 * potValue / 1024, 2)
        digitalValue.text = str("%1.2f" % voltage) + "V"
        # Use the potentiometer to set the meter needle angle.
        # How this works:
        #   0V is 5pi/6 rads, 5V is pi/6 rads, thus the needle range is 4pi/6 rads.
        #   The pot range is 0 - 1023, or 1024 steps, so each step is 4pi/6/1024, or pi/1536 rads.
        #   Thus, the needle position is 5pi/6 - (pi/1536 X Potentiometer Value) rads.
        theta = (5 * np.pi / 6) - (np.pi / 1536 * potValue)
        meterNeedle.axis = vector(meterNeedleL * np.cos(theta), meterNeedleL * np.sin(theta), 0)
    else:
        # Flash the serial error message on top of the meter.
        serialErrorVisible = (serialErrorVisible + 1) % 2 # Using modulo 2 maths to toggle the variable between 0 and 1.
        serialError.opacity = serialErrorVisible
        # Wait for a bit...
        time.sleep(0.5)

# EOF
