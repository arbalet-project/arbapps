#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Arbaloop - Sequencer of Arbalet applications

    Runs and closes Arbalet apps according to a sequence file

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
from arbasdk import Arbapp
from os.path import isfile, join, realpath, dirname
from json import load
from subprocess import Popen
from glob import glob
from shlex import split
from time import sleep, time
from pygame import JOYBUTTONDOWN
from signal import SIGINT
import argparse

# TODO must Arbaloop inherit from Arbapp?
# It should ignore -ng -w and redirect them to the children

class Arbaloop(Arbapp):
    def __init__(self, argparser):
        Arbapp.__init__(self, argparser, True) # starting mock mode, init flags (-w and -ng) will be redirected to the server
        self.server_process = None

    def run(self):
        if len(self.args.sequence)>0:
            if not isfile(self.args.sequence):
                print "Sequence file '{}' not found".format(self.args.sequence)
            else:
                # launch the server
                self.start_server(self.args.hardware, self.args.no_gui)
                # read the sequence
                with open(self.args.sequence) as fsequence:
                    sequence = load(fsequence)
                # and launch every app in the sequence as a client
                try:
                    self.execute_sequence(sequence)
                finally:
                    self.close_server()

    def close_server(self):
        if self.server_process:
            self.server_process.terminate()
            self.server_process.send_signal(SIGINT)
            self.server_process.wait()
            self.server_process = None

    def wait(self, timeout=-1, interruptible=False, process=None):
        start = time()
        # We loop while the process is not terminated, the timeout is not expired, and user has not asked 'next' with the joystick
        while (timeout < 0 or time()-start < timeout) and (process is None or process.poll() is None):
            for e in self.arbalet.events.get():
                if interruptible and e.type == JOYBUTTONDOWN and e.button in self.arbalet.joystick['back']:
                    # A "back" joystick key jumps to the next app, unless interruptible has been disabled
                    return 'joystick'
                elif e.type == JOYBUTTONDOWN and e.button in self.arbalet.joystick['start']:
                    # A "start" joystick key restarts the same app
                    return 'restart'
                else:
                    # Any other activity resets the timer
                    start = time()
            sleep(0.01)
        return 'timeout' if (process is None or process.poll() is None) else 'terminated'

    def start_server(self, hardware, no_gui):
        cwd = join(realpath(dirname(__file__)), '..', 'Arbaserver')
        command = join(cwd, 'Arbaserver.py')
        if hardware:
            command += ' -w'
        if no_gui:
            command += ' -ng'
        print "Starting server with: " + command
        self.server_process = Popen(command.split(), cwd=cwd)

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

        def expand_args(args, cwd):
            args = map(lambda arg: glob(join(cwd, arg)) if len(glob(join(cwd, arg))) > 0 else arg, args)  # Expand . ? and *
            expanded_args = []
            for arg in args:
                if isinstance(arg, str):
                    expanded_args.append(arg)
                else:
                    for expanded_arg in arg:
                        expanded_args.append(expanded_arg)
            expanded_args[0] = join(cwd, expanded_args[0])
            return expanded_args

        while True:
            for command in sequence['sequence']:
                args = split(command['command'])
                cwd = join(realpath(dirname(__file__)), '..', command['dir'])
                while True:  # Loop allowing the user to play again, by restarting app
                    process = Popen(purify_args(expand_args(args, cwd)), cwd=cwd)
                    print "Starting "+str(args)
                    reason = self.wait(command['timeout'], command['interruptible'], process) # TODO interruptible raw_input in new_thread for 2.7, exec with timeout= for 3
                    print "End:", reason
                    if reason != 'terminated':
                        process.terminate()  # SIGTERM
                        process.send_signal(SIGINT)
                        process.wait() # should poll() and kill() if it does not close?
                    if reason != 'restart':
                        break
            if not sequence['infinite']:
                break

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Application sequencer. Runs and closes Arbalet apps according to a sequence file. In general the timeout specifies the duration of user inactivity (joystick or keyboard before switching to the next app. A press on any jostick upper joystick key forces app swicthing unless this has been disabled by interruptible = False within the config files, e.g. for apps already using upper keys. Only apps that guarantee termination in case of user inactivity should set a timeout to -1')
    parser.add_argument('-q', '--sequence',
                        type=str,
                        default='sequences/default.json',
                        nargs='?',
                        help='Configuration file describing the sequence of apps to launch')
    Arbaloop(parser).start()
