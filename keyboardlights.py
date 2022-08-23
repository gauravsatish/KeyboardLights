#!/bin/python

from time import sleep
import os
import random
import sys

input_number = "15"


def light(led: str, operation: str):
    if (led == "capslock" or led == "scrolllock" or led == "numlock"):
        if operation == "on":
            os.system("brightnessctl -d input" + input_number + "::" + led + " s 1 >> /dev/null")
        elif operation == "off":
            os.system("brightnessctl -d input" + input_number + "::" + led + " s 0 >> /dev/null")
        else:
            print("Not a valid operation")
    else:
        print("not a valid light (received: " + led + ")")


def clear():
    light("capslock", "off")
    light("numlock", "off")
    light("scrolllock", "off")


def sequential():
    clear()

    last_led = "scrolllock"
    for i in range(0, 100):
        light(last_led, "off")
        if last_led == "scrolllock":
            light("numlock", "on")
            last_led = "numlock"
        elif last_led == "numlock":
            light("capslock", "on")
            last_led = "capslock"
        elif last_led == "capslock":
            light("scrolllock", "on")
            last_led = "scrolllock"

        sleep(0.15)


def sequential_and_back():
    clear()
    last_led = "scrolllock"
    forward = True
    count = 0
    for _ in range (0, 100):
        light(last_led, "off")
        if last_led == "scrolllock":
            last_led = "numlock" if forward else "capslock"
        elif last_led == "numlock":
            last_led = "capslock" if forward else "scrolllock"
        elif last_led == "capslock":
            last_led = "scrolllock" if forward else "numlock"
        light(last_led, "on")

        count = count + 1
        if count == 3:
            forward = False if forward else True
            count = 1
            
        sleep(0.15)


def all_on_all_off():
    clear()
    on = False
    for i in range (0, 200):
        if on:
            light("capslock", "off")
            light("scrolllock", "off")
            light("numlock", "off")
            on = False
        elif on == False:
            light("capslock", "on")
            light("scrolllock", "on")
            light("numlock", "on")
            on = True
        sleep(0.25)


def random_lights():
    clear()
    
    numlock = False
    capslock = False
    scrolllock = False
    
    numlock_timer = random.random()
    capslock_timer = random.random()
    scrolllock_timer = random.random()
    
    for i in range (0, 1000):
        next_timer = min(numlock_timer, capslock_timer, scrolllock_timer)
        sleep(next_timer)
        
        if (next_timer == numlock_timer):
            light("numlock", "off" if numlock else "on")
            numlock = False if numlock else True
        elif (next_timer == capslock_timer):
            light("capslock", "off" if capslock else "on")
            capslock = False if capslock else True
        elif (next_timer == scrolllock_timer):
            light("scrolllock", "off" if scrolllock else "on")
            scrolllock = False if scrolllock else True
    
        numlock_timer -= next_timer
        capslock_timer -= next_timer
        scrolllock_timer -= next_timer
    
        if numlock_timer <= 0:
            numlock_timer = random.random()
        elif capslock_timer <= 0:
            capslock_timer = random.random()
        elif scrolllock_timer <= 0:
            scrolllock_timer = random.random()
    

if len(sys.argv) > 1:
    if sys.argv[1] == "left-to-right":
        sequential()
    elif sys.argv[1] == "on-off":
        all_on_all_off()
    elif sys.argv[1] == "left-right-and-back":
        sequential_and_back()
    elif sys.argv[1] == "random":
        random_lights()
    else:
        print("Not a valid option\nAvailable Options:\nleft-to-right\non-off\nleft-right-and-back\nrandom")
else:
    print("specify an input :skull:")
