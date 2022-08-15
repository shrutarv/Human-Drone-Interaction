#!/usr/bin/env python
from __future__ import print_function

import numpy as np
from pycrazyswarm import *
from Tkinter import *
import sys
import math
import time

class CrazyflieWrapper(object):
    def __init__(self, start_time, land_time, movement_time, movement_amount, height):
        self.swarm = Crazyswarm()
        self.allcfs = self.swarm.allcfs
        self.start_time = start_time
        self.land_time = land_time
        self.movement_time = movement_time
        self.movement_amount = movement_amount
        self.height = height
        self.time_for_next_command = time.time()
        self.relative_position = Vector2D()

    def check_and_set_time_for_command(self, commands_seconds):
        if self.time_for_next_command <= time.time():
            self.time_for_next_command = time.time() + commands_seconds
            return True
        return False

    def print_debug(self):
        print("time for starting:", self.start_time)
        print("time for landing:", self.land_time)
        print("time for moving:", self.movement_time)
        print("amount of moving:", self.movement_amount)
        print("height:", self.height)

    def move(self, vector):
        if self.check_and_set_time_for_command(self.movement_time):
            vector.scale(self.movement_amount)
            self.relative_position.addX(vector.getX())
            self.relative_position.addY(vector.getY())
            print(vector.getX(), vector.getY())
            for cf in self.allcfs.crazyflies:
                pos = np.array(cf.initialPosition) + np.array([self.relative_position.getX(), self.relative_position.getY(), self.height])
                cf.goTo(pos, 0, self.movement_time)

    def start(self):
        if self.check_and_set_time_for_command(self.start_time):
            self.allcfs.takeoff(targetHeight=self.height, duration=self.start_time)
            print("start")

    def land(self):
        if self.check_and_set_time_for_command(self.land_time):
            self.allcfs.land(targetHeight=0.00, duration=self.land_time)
            print("land")

    def change_start_time(self, amount):
        self.start_time += amount

    def change_land_time(self, amount):
        self.land_time += amount

    def change_movement_time(self, amount):
        self.movement_time += amount

    def change_move_amount(self, amount):
        self.movement_amount += amount

    def change_height(self, amount):
        self.height += amount

class Vector2D(object):
    def __init__(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y
    def addX(self, amount):
        self.x += amount
    def addY(self, amount):
        self.y += amount
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    def scale(self, amount):
        own_length = self.length()
        self.x = amount * self.x / own_length
        self.y = amount * self.y / own_length

def format_decimal(number):
    return '{0:.2f}'.format(number)

def goto_command(char, object):
    current_direction = Vector2D()
    if char == "Left":
        current_direction.addX(-1.0)
    if char == "Right":
        current_direction.addX(1.0)
    if char == "Up":
        current_direction.addY(1.0)
    if char == "Down":
        current_direction.addY(-1.0)

    if current_direction.length() > 0.01:
        object.move(current_direction)

class Screen:
    def __init__(self, main_window):
        self.main_window = main_window
        main_window.title("Crazyswarm Flight Controller")

        self.start_time = 2.5
        self.land_time = 2.5
        self.movement_time = 2.5
        self.movement_amount = 0.5
        self.height = 0.3
        self.cfs = CrazyflieWrapper(self.start_time, self.land_time, self.movement_time, self.movement_amount, self.height)

        self.takeoff_time_label = Label(main_window, text = "Takeoff Time:")
        self.land_time_label = Label(main_window, text = "Land Time:")
        self.movement_time_label = Label(main_window, text = "Move Time:")
        self.movement_amount_label = Label(main_window, text = "Move Amount:")
        self.height_label = Label(main_window, text = "Height:")
        self.takeoff_time_shortcut_label = Label(main_window, text = "( F1 | F2 )", fg = "grey")
        self.land_time_shortcut_label = Label(main_window, text = "( F3 | F4 )", fg = "grey")
        self.movement_time_shortcut_label = Label(main_window, text = "( F5 | F6 )", fg = "grey")
        self.movement_amout_shortcut_label = Label(main_window, text = "( F7 | F8 )", fg = "grey")
        self.height_shortcut_label = Label(main_window, text = "( F9 | F10 )", fg = "grey")
        self.takeoff_shortcut_label = Label(main_window, text = "( Page-Up )", fg = "grey")
        self.land_shortcut_label = Label(main_window, text = "( Page-Down )", fg = "grey")
        self.shortcut_label = Label(main_window, text = "Shortcuts", font = ("bold"))

        self.takeoff_button = Button(main_window, text = "Takeoff", command = lambda : self.cfs.start())
        self.land_button = Button(main_window, text = "Land", command = lambda : self.cfs.land())
        self.left_button = Button(main_window, text = "<", command = lambda : goto_command("Left", self.cfs))
        self.right_button = Button(main_window, text = ">", command = lambda : goto_command("Right", self.cfs))
        self.up_button = Button(main_window, text = "^", command = lambda : goto_command("Up", self.cfs))
        self.down_button = Button(main_window, text = "v", command = lambda : goto_command("Down", self.cfs))
        self.exit_button = Button(main_window, text = "Quit", command = main_window.quit)

        self.takeoff_entry = Entry(main_window, bd = 2, width = 6)
        self.land_entry = Entry(main_window, bd = 2, width = 6)
        self.movement_time_entry = Entry(main_window, bd = 2, width = 6)
        self.movement_amount_entry = Entry(main_window, bd = 2, width = 6)
        self.height_entry = Entry(main_window, bd = 2, width = 6)

        self.takeoff_time_label.grid(row = 0, column = 0, pady = 20, padx = 20, sticky = W)
        self.land_time_label.grid(row = 1, column = 0, pady = 20, padx = 20, sticky = W)
        self.movement_time_label.grid(row = 2, column = 0, pady = 20, padx = 20, sticky = W)
        self.movement_amount_label.grid(row = 3, column = 0, pady = 20, padx = 20, sticky = W)
        self.height_label.grid(row = 4, column = 0, pady = 20, padx = 20, sticky = W)
        self.takeoff_time_shortcut_label.grid(row = 0, column = 2, pady = 20, padx = 20, sticky = W)
        self.land_time_shortcut_label.grid(row = 1, column = 2, pady = 20, padx = 20, sticky = W)
        self.movement_time_shortcut_label.grid(row = 2, column = 2, pady = 20, padx = 20, sticky = W)
        self.movement_amout_shortcut_label.grid(row = 3, column = 2, pady = 20, padx = 20, sticky = W)
        self.height_shortcut_label.grid(row = 4, column = 2, pady = 20, padx = 20, sticky = W)
        self.takeoff_shortcut_label.grid(row = 5, column = 0, padx = 20, sticky = W)
        self.land_shortcut_label.grid(row = 5, column = 1)
        self.shortcut_label.grid(row = 5, column = 2)

        self.takeoff_button.grid(row = 6, column = 0, pady = 20, padx = 20, sticky = W)
        self.land_button.grid(row = 6, column = 1, pady = 20, padx = 20, sticky = W)
        self.left_button.grid(row = 6, column = 3)
        self.right_button.grid(row = 6, column = 5)
        self.up_button.grid(row = 5, column = 4)
        self.down_button.grid(row = 6, column = 4)
        self.exit_button.grid(row = 6, column = 2, pady = 20, padx = 20, sticky = W)

        self.takeoff_entry.grid(row = 0, column = 1, pady = 20, padx = 20, sticky = W)
        self.land_entry.grid(row = 1, column = 1, pady = 20, padx = 20, sticky = W)
        self.movement_time_entry.grid(row = 2, column = 1, pady = 20, padx = 20, sticky = W)
        self.movement_amount_entry.grid(row = 3, column = 1, pady = 20, padx = 20, sticky = W)
        self.height_entry.grid(row = 4, column = 1, pady = 20, padx = 20, sticky = W)

        self.takeoff_entry.insert(0, self.start_time)
        self.land_entry.insert(0, self.land_time)
        self.movement_time_entry.insert(0, self.movement_time)
        self.movement_amount_entry.insert(0, self.movement_amount)
        self.height_entry.insert(0, self.height)

        current_direction = Vector2D()
        # In der Ereignisschleife auf Eingabe des Benutzers warten.
        main_window.bind("<Left>", lambda event, : goto_command("Left", self.cfs))
        main_window.bind("<Right>", lambda event, : goto_command("Right", self.cfs))
        main_window.bind("<Up>", lambda event, : goto_command("Up", self.cfs))
        main_window.bind("<Down>", lambda event, : goto_command("Down", self.cfs))
        main_window.bind("<Prior>", lambda event, : self.cfs.start())
        main_window.bind("<Next>", lambda event, : self.cfs.land())
        main_window.bind("<End>", lambda event, : main_window.quit())
        main_window.bind("<F1>", lambda event, : self.cfs.change_start_time(-0.1))
        main_window.bind("<F2>", lambda event, : self.cfs.change_start_time(0.1))
        main_window.bind("<F3>", lambda event, : self.cfs.change_land_time(-0.1))
        main_window.bind("<F4>", lambda event, : self.cfs.change_land_time(0.1))
        main_window.bind("<F5>", lambda event, : self.cfs.change_movement_time(-0.1))
        main_window.bind("<F6>", lambda event, : self.cfs.change_movement_time(0.1))
        main_window.bind("<F7>", lambda event, : self.cfs.change_move_amount(-0.1))
        main_window.bind("<F8>", lambda event, : self.cfs.change_move_amount(0.1))
        main_window.bind("<F9>", lambda event, : self.cfs.change_height(-0.1))
        main_window.bind("<F10>", lambda event, : self.cfs.change_height(0.1))

        self.update_window()

    def update_window(self):
        self.takeoff_entry.delete(0, END)
        self.takeoff_entry.insert(0, format_decimal(self.cfs.start_time))
        self.land_entry.delete(0, END)
        self.land_entry.insert(0, format_decimal(self.cfs.land_time))
        self.movement_time_entry.delete(0, END)
        self.movement_time_entry.insert(0, format_decimal(self.cfs.movement_time))
        self.movement_amount_entry.delete(0, END)
        self.movement_amount_entry.insert(0, format_decimal(self.cfs.movement_amount))
        self.height_entry.delete(0, END)
        self.height_entry.insert(0, format_decimal(self.cfs.height))
        self.main_window.after(200, self.update_window)

def main():
    main_window = Tk()
    crazyswarm_controller = Screen(main_window)
    main_window.mainloop()

if __name__ == "__main__":
    main()
