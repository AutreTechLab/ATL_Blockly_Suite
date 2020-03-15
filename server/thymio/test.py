#!/usr/bin/python
##################################################
## Example using Thymio and Python to test the setup
##################################################
## Author: Autre Techlab
## Email: autretechlab@gmail.com
##################################################

import dbus
import dbus.mainloop.glib
from gi.repository import GObject as gobject
from gi.repository import GLib as glib
import sys
import os

class ThymioController():
    def __init__(self):
        # init the main loop and sends the ASEBA code to the Thymio bot for the on-robot computations
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        # get stub of the Aseba network
        bus = dbus.SessionBus()
        asebaNetworkObject = bus.get_object('ch.epfl.mobots.Aseba', '/')
        self.asebaNetwork = dbus.Interface(asebaNetworkObject,
                                           dbus_interface='ch.epfl.mobots.AsebaNetwork')

        # schedules first interaction with the Robot
        glib.timeout_add(20, self.callThymio)

    def run(self):
        # run event loop
        self.loop = gobject.MainLoop()
        self.loop.run()

    def dbusReply(self):
        # correct replay on D-Bus, ignore
        pass

    def dbusError(self, e):
        # there was an error on D-Bus, stop loop
        print('dbus error: %s' % str(e))
        self.loop.quit()

    def callThymio(self):
        # if no loop is running, skip function
        if not self.loop.is_running():
            return

        self.asebaNetwork.SendEventName("SetColor",
                                        [32, 20, 20],
                                        reply_handler=self.dbusReply,
                                        error_handler=self.dbusError
                                        )
        self.loop.quit()

        # reschedule scan of joystick
        glib.timeout_add(20, self.callThymio)


def main():
    # create and run controller

    thymioController = ThymioController()
    thymioController.run()


if __name__ == '__main__':
    main()