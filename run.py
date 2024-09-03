import sys
import yaml
import threading
import argparse

from sr.robot import *

# Modify run.py to handle an additional seed argument
parser = argparse.ArgumentParser(description="Run the robot simulator.")
parser.add_argument('-c', '--config', type=str, required=True, help="Path to the configuration file.")
parser.add_argument('robot_scripts', nargs='+', help="Robot scripts to run.")
parser.add_argument('--seed', type=int, help="Seed for random number generator.")

args = parser.parse_args()

# Read the configuration file
with open(args.config, 'r') as f:
    config = yaml.load(f)

# Now pass the seed to the simulator
sim = Simulator(config=config, background=False, seed=args.seed)

def read_file(fn):
    with open(fn, 'r') as f:
        return f.read()

robot_scripts = args.robot_scripts
if not robot_scripts:
    prompt = "Enter the names of the Python files to run, separated by commas: "
    while not robot_scripts:
        robot_script_names = raw_input(prompt).split(',')
        if robot_script_names == ['']:
            continue
        robot_scripts = [read_file(s.strip()) for s in robot_script_names]
else:
    # If scripts are provided in the command line arguments
    robot_scripts = [read_file(s.strip()) for s in robot_scripts]

class RobotThread(threading.Thread):
    def __init__(self, zone, script, *args, **kwargs):
        super(RobotThread, self).__init__(*args, **kwargs)
        self.zone = zone
        self.script = script
        self.daemon = True

    def run(self):
        try:
            def robot():
                with sim.arena.physics_lock:
                    robot_object = SimRobot(sim)
                    robot_object.zone = self.zone
                    robot_object.location = sim.arena.start_locations[self.zone]
                    robot_object.heading = sim.arena.start_headings[self.zone]
                    return robot_object

            exec(self.script, {'Robot': robot})

        except SystemExit:
            print("Robot in zone {} has completed its task.".format(self.zone))
            sim.stop()  # Stops the simulation when the robot completes the circuit.
            sys.exit(0)  # Ensures the thread exits cleanly.

threads = []
for zone, robot in enumerate(robot_scripts):
    thread = RobotThread(zone, robot)
    thread.start()
    threads.append(thread)

sim.run()

# Warn PyScripter users that despite the exit of the main thread, the daemon
# threads won't actually have gone away.
threads = [t for t in threads if t.is_alive()]
if threads:
    print("WARNING: {0} robot code threads still active.".format(len(threads)))
    #####                                                               #####
    # If you see the above warning in PyScripter and you want to kill your  #
    # robot code you can press Ctrl+F2 to re-initialize the interpreter and #
    # stop the code running.                                                #
    #####                                                               #####

