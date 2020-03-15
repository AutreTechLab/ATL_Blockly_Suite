#!/usr/bin/python3
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

class ThymioBot(object):
    def __init__(self, filename):
        # init the main loop and sends the ASEBA code to the Thymio bot for the on-robot computations
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        # get stub of the Aseba network
        bus = dbus.SessionBus()
        asebaNetworkObject = bus.get_object('ch.epfl.mobots.Aseba', '/')
        self.asebaNetwork = dbus.Interface(asebaNetworkObject,
                                           dbus_interface='ch.epfl.mobots.AsebaNetwork')

        # load the ASEBA file to the Thymio II bot for the on-robot computations.
        self.asebaNetwork.LoadScripts(sys.argv[1],
                                      reply_handler=self.dbusReply,
                                      error_handler=self.dbusError
                                      )

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

        # send speed command

        motorLeftTarget = 0
        motorRightTarget = 0
        self.asebaNetwork.SendEventName('SetSpeed',
                                        [motorLeftTarget, motorRightTarget],
                                        reply_handler=self.dbusReply,
                                        error_handler=self.dbusError
                                        )

        # send color command

        self.asebaNetwork.SendEventName('SetColor',
                                        [ 6, 13, 32],
                                        reply_handler=self.dbusReply,
                                        error_handler=self.dbusError
                                        )

        # read and display horizontal sensors
        proxHorizontal = self.asebaNetwork.GetVariable(
            'thymio-II', 'prox.horizontal')



        # reschedule scan of joystick
        glib.timeout_add(20, self.callThymio)


    # Requesting Thymio Sensor data
    def getACCSensorData(self):
        acc = self.asebaNetwork.GetVariable(
            'thymio-II', 'acc')

        print("prox.horizontal: " + (', '.join(map(str, proxHorizontal))) + "\t acc: " + (', '.join(map(str, acc))))


def main():
    # check command-line arguments
    if len(sys.argv) != 2:
        print('Usage %s FILE' % sys.argv[0])
        return

    # create and run controller
    ThymioBot = ThymioBot(sys.argv[1])
    ThymioBot.run()


if __name__ == '__main__':
    main()