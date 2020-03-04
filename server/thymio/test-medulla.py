#!/usr/bin/python

import dbus
import dbus.mainloop.glib
#import glib
#import gobject
import pygame
import sys

import gi.repository

class ThymioController(object):
    def __init__(self, filename):
        # init the main loop and joystick
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        pygame.init()
#        self.joystick = pygame.joystick.Joystick(0)
#        self.joystick.init()
        self.ox = 0
        self.oy = 0
        self.oc = [0] * 3

        # get stub of the Aseba network
        bus = dbus.SessionBus()
        asebaNetworkObject = bus.get_object('ch.epfl.mobots.Aseba', '/')
        self.asebaNetwork = dbus.Interface(asebaNetworkObject,
                                           dbus_interface='ch.epfl.mobots.AsebaNetwork')

        # load the file
        self.asebaNetwork.LoadScripts(sys.argv[1],
                                      reply_handler=self.dbusReply,
                                      error_handler=self.dbusError
                                      )

        # schedules first scan of joystick
        glib.timeout_add(20, self.scanJoystick)

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

    def scanJoystick(self):
        # if no loop is running, skip function
        if not self.loop.is_running():
            return

        # scan joystick and send command to Thymio
        pygame.event.pump()
  #      x = self.joystick.get_axis(0) * 300
 #       y = -self.joystick.get_axis(1) * 300
#        c = [self.joystick.get_button(i) for i in range(3)]

        # send speed command
        if x != self.ox or y != self.oy:
            self.asebaNetwork.SendEventName('SetSpeed',
                                            [y + x, y - x],
                                            reply_handler=self.dbusReply,
                                            error_handler=self.dbusError
                                            )
            self.ox, self.oy = x, y

        # send color command
        if cmp(c, self.oc) != 0:
            self.asebaNetwork.SendEventName('SetColor',
                                            map(lambda x: 32 * x, c),
                                            reply_handler=self.dbusReply,
                                            error_handler=self.dbusError
                                            )
            self.oc = c

        # read and display horizontal sensors
        horizontalProximity = self.asebaNetwork.GetVariable(
            'thymio-II', 'prox.horizontal')
        print(', '.join(map(str, horizontalProximity)))

        # reschedule scan of joystick
        glib.timeout_add(20, self.scanJoystick)


def main():
    # check command-line arguments
    if len(sys.argv) != 2:
        print('Usage %s FILE' % sys.argv[0])
        return

    # create and run controller
    thymioController = ThymioController(sys.argv[1])
    thymioController.run()


if __name__ == '__main__':
    main()