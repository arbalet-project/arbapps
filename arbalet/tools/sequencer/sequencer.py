#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Sequencer of Arbalet applications

    Runs and closes Arbalet apps according to a sequence file

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
from arbalet.core import Application
from os.path import isfile, join, realpath, dirname
from os import chdir
from sys import executable
from json import load
from subprocess import Popen
from glob import glob
from shlex import split
from time import sleep, time
from pygame import JOYBUTTONDOWN
from signal import SIGINT, signal

# TODO must Sequencer inherit from Application?
# It should ignore -ng -w and redirect them to the children

class Sequencer(Application):
    def __init__(self, argparser):
        Application.__init__(self, argparser, True) # starting mock mode, init flags (-w and -ng) will be redirected to the server
        self.server_process = None
        self.running = True
        signal(SIGINT, self.close_processes)

    def close_processes(self, signal, frame):
        self.running = False
 
    def run(self):
        if len(self.args.sequence)>0:
            sequence_file = join(realpath(dirname(__file__)), self.args.sequence)
            if not isfile(sequence_file):
                print("[Arbalet Sequencer] Sequence file '{}' not found".format(sequence_file))
            else:
                # launch the server
                self.start_server(self.args.hardware, self.args.no_gui)
                # read the sequence
                with open(sequence_file) as fsequence:
                    sequence = load(fsequence)
                # and launch every app in the sequence as a client
                try:
                    self.execute_sequence(sequence)
                finally:
                    self.close_server()

    def close_server(self):
        if self.server_process:
            self.server_process.send_signal(SIGINT)
            self.server_process.wait()
            self.server_process = None

    def wait(self, timeout=-1, interruptible=False, process=None):
        start = time()
        # We loop while the process is not terminated, the timeout is not expired, and user has not asked 'next' with the joystick
        while self.running and (timeout < 0 or time()-start < timeout) and (process is None or process.poll() is None):
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
        command = "{} -m arbalet.tools.server".format(executable)
        if hardware:
            command += ' -w'
        if no_gui:
            command += ' -ng'
        print("[Arbalet Sequencer] Starting server with: " + command)
        self.server_process = Popen(command.split())

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
            #args = map(lambda arg: if len(glob(join(cwd, arg))) > 0 else arg, args)  # Expand . ? and *
            expanded_args = []
            for arg in args:
                globed_arg = glob(arg)
                if len(globed_arg)==0:
                    expanded_args.append(arg)
                else:
                    for expanded_arg in globed_arg:
                        expanded_args.append(expanded_arg)
            return expanded_args

        # change WD to the modules' root
        cwd = join(realpath(dirname(__file__)), '..', '..', 'apps')
        chdir(cwd)

        while self.running:
            for command in sequence['sequence']:
                args = "{} -m {} {}".format(executable, command['app'], command['args'] if 'args' in command else '')
                module_command = purify_args(expand_args(args.split(), join(*command['app'].split('.'))))
                while self.running:  # Loop allowing the user to play again, by restarting app
                    print("[Arbalet Sequencer] STARTING {}".format(module_command))
                    process = Popen(module_command, cwd=cwd)
                    timeout = command['timeout'] if 'timeout' in command else -1
                    reason = self.wait(timeout, command['interruptible'], process) # TODO interruptible raw_input in new_thread for 2.7, exec with timeout= for 3
                    print("[Arbalet Sequencer] END: {}".format(reason))
                    if reason != 'terminated' or not self.running:
                        process.send_signal(SIGINT)
                        process.wait()
                    if reason != 'restart':
                        break
            if not sequence['infinite']:
                break
