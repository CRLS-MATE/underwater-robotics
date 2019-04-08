#CRLS UNDERWATER ROBOTICS TEAM 2015

import os
import sys
import time
import select #not important
import pygame
import serial
import requests
import urllib.parse

# ip of rpi
rovIP = "192.168.4.1"

# this is the number of dots that will be used to display the output of an axis
dots = 8

# this is for pygameeeeee
screen = None

# write to stderr.  pygame clutters up stdout because of a bug
def wrerr(msg): 
    sys.stderr.write(msg)

# print to stderr to avoid SDL messages
def prerr(msg):
    wrerr(msg + "\r\n")

# write out all the information we know about a joystick
def printJoystickInfo(index, js):
    prerr("\n")
    prerr("Joystick %d: %s" % (index, js.get_name()))
    prerr("\tAxes:\t%d" % js.get_numaxes())
    prerr("\tBalls:\t%d" % js.get_numballs())
    prerr("\tButtons:\t%d" % js.get_numbuttons())
    prerr("\tHats:\t%d" % js.get_numhats())


# read joystick info and print it out on the screen
def readJoystick(js):
    pygame.event.pump()  # get joystick events from pygame

    output = []

    # cycle through all joystick axes
    for i, axis in enumerate([js.get_axis(i) for i in range(js.get_numaxes())]):
        if((not js.get_button(7)) and not (js.get_button(6) and i != 2)):
            axis = 0
        norm = (axis + 1.0) * (127/ 2.0) # normalize to the range 0-127
        output.append(round(norm))

        # print the axis number for debugging
        wrerr(str(i) + ": ") 
        #  print an exclamation point if the value is above this dot, otherwise a period
        for d in range(dots):
            if d < (norm * dots)/127:
                wrerr("!")
            else:
                wrerr(".")

        wrerr("\t")

    for j, button in enumerate([js.get_button(k) for k in range(js.get_numbuttons())]):
        #output.append(button)
        wrerr("Button " + str(j) + ": " + str(button))
        
    #prerr("")
    #pygame.event.clear()
    return output


# normal script entry
if __name__ == "__main__":

    # set up pygame, including a screen (even though we don't need it)
    global Screen
    pygame.init()
    #screen = pygame.display.set_mode((640, 480))
    #ser = serial.Serial(2)
    
    # print error message if no joysticks were connected
    if pygame.joystick.get_count() < 1:
        prerr("No joysticks were found :(")
        exit(1)
        
    # print info about each joystick that was found
    for i, js in enumerate([pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]):
        js.init()
        printJoystickInfo(i, js)
        prerr("")

    # print an error message if no joystick was specified
    if len(sys.argv) < 2:
        pygame.quit()
        prerr("You need to choose a specific joystick with the command 'python %s <joystick number> 1>out.log'" % sys.argv[0])
        prerr("")
        exit(1)

    joystickNum = int(sys.argv[1])

    # initialize the joystick that was specified on the command line 
    js = pygame.joystick.Joystick(joystickNum)
    if not js.get_init():
        js.init()
        
    n = 0 
    # loop and read input
    while True:
        values = readJoystick(js) # get array of axis values
        
        # map joystick axis values to servos
        my_query = {
                0: str((values[1] - values[0])/2), # right
                1: str((values[1] + values[0])/2), # left
                2: str(values[3]), # up-right
                3: str(values[3]), # up-left
                }

        my_query = urllib.parse.urlencode(my_query)
        
        prerr("about to send: " + my_query)
        try:
            r = requests.get("http://" + rovIP + ":5000" + "/?" + my_query)
            prerr("sent")
            # prerr(r.text)
        except Exception as e:
            prerr(str(e))
        time.sleep(0.2) 


##### SCRAPS #####
#letters = ["w", "s", "h", "y"] # labels we send to serial port that the arduino expect
# The arduinocamand will call for the label (letters) and the value of the speed(0 - 127)
# the speed is coded as a char
# example of arduinocommand: ::wJsOhUyP
# y -> yaw (spinning in place)
# h -> height?
# s -> speed (forward)?
# w -> ?

# building the arduino command
#myArduinoCommand = ""#"::" # resetting the state of the ardunio

#for i, v in enumerate(values): # going through the values index and its axis value
#    myArduinoCommand = myArduinoCommand + letters[i] # setting up the arduino state 
#    myArduinoCommand = myArduinoCommand + str(int(v))#chr(int(v)) # setting up the arduino spead
#    # chr(int(v)) is going to convert v as integer with the equivalent value of it as a character

# arduino command is now complete

#ser.write(myArduinoCommand) # send the command
## going through the values index and its axis value
#for i, v in enumerate(values): 
#    my_query[i] = v

