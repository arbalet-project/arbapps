#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Arbaloop - Sequencer of Arbalet applications

    Runs and closes Arbalet apps according to a sequence file

    Copyright (C) 2015 Yoan Mollard <yoan@konqifr.fr>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""
from arbasdk import Arbapp
from os.path import isfile, join, realpath, dirname
from json import load
from subprocess import Popen
from shlex import split
from time import sleep, time
from pygame import event, init, joystick, JOYBUTTONDOWN
import argparse

# TODO must Arbaloop inherit from Arbapp?
# It should ignore -ng -w and redirect them to the children

class Arbaloop(Arbapp):
    def __init__(self, argparser):
        Arbapp.__init__(self, argparser)
        init()
        joystick.init()
        self.joysticks = []

        # Joysticks initialization
        for i in range(joystick.get_count()):
            joy = joystick.Joystick(i)
            joy.init()
            if joy.get_numbuttons()>0:
                self.joysticks.append(joy)
            else:
                joy.quit()

        print len(self.joysticks), 'joystick(s) with buttons found!'

    def run(self):
        if len(self.args.sequence)>0:
            if not isfile(self.args.sequence):
                print "Sequence file '{}' not found".format(self.args.sequence)
            else:
                with open(self.args.sequence) as sequence:
                    self.execute_sequence(load(sequence))

    def wait(self, timeout=-1, interruptible=False, process=None):
        if interruptible:
            start = time()
            # We loop while the process is not termianted, the timeout is not expired, and user has not asked 'next' with the joystick
            while (timeout < 0 or time()-start < timeout) and (process==None or process.poll()==None):
                e = event.poll()
                if e.type == JOYBUTTONDOWN:
                    return 'joystick'
                else:
                    sleep(0.01)
        return 'timeout' if (process==None or process.poll()==None) else 'terminated'

    def execute_sequence(self, sequence):
        def purify_args(args):
            for rm_arg in ['-h, --hardware', ]:
                try:
                    args.remove(rm_arg)
                except ValueError:
                    pass
            for add_arg in ['--no-gui', '--server']:
                args.append(add_arg)
            return args

        while True:
            for command in sequence['sequence']:
                args = split(command['command'])
                cwd = join(realpath(dirname(__file__)), '..', command['dir'])
                args[0] = join(cwd, args[0])
                process = Popen(purify_args(args), cwd=cwd)
                print "Starting "+str(args)
                reason = self.wait(command['timeout'], command['interruptible'], process) # TODO interruptible raw_input in new_thread for 2.7, exec with timeout= for 3
                if reason!='terminated':
                    process.terminate()
                    process.wait() # should poll() and kill() if it does not close?
            if not sequence['infinite']:
                break

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Application sequencer. Runs and closes Arbalet apps according to a sequence file')
    parser.add_argument('-q', '--sequence',
                        type=str,
                        const='sequences/default.json',
                        nargs='?',
                        help='Configuration file describing the sequence of apps to launch')
    Arbaloop(parser).start()