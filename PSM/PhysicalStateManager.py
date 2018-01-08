from PSM.States import *
from PSM.Transitions import *
#from . import SimulationTypes
#from pypot.creatures import PoppyHumanoid
from pypot.creatures import *

import time

class SimulationTypes:
    NONE, VREP, LIVE = range(0, 3)

class PhysicalStateManager:

    # initialize with simulation type so poppy can be initialized the correct way
    def __init__(self, sim=SimulationTypes.NONE):
        self.simulation_mode = sim

        if sim == SimulationTypes.VREP:  # VREP mode. (Ensure VREP is running with Poppy loaded)
            self.Poppy = creature.PoppyHumanoid(simulator='vrep')
            debug("Physical State Manager in VREP mode")
        elif sim == SimulationTypes.LIVE:  # LIVE mode. When executing on the robot itself
            self.Poppy = PoppyHumanoid(use_http=True)
            debug("Physical State Manager in LIVE mode")
        else:  # Physical State Manager wont do anything
            self.Poppy = None
            debug("Physical State Manager turned off")
            return

        # define some helpful lists that make it easier to access complete body (parts)
        self.left_arm = [self.Poppy.l_shoulder_y, self.Poppy.l_shoulder_x, self.Poppy.l_arm_z, self.Poppy.l_elbow_y]
        self.right_arm = [self.Poppy.r_shoulder_y, self.Poppy.r_shoulder_x, self.Poppy.r_arm_z, self.Poppy.r_elbow_y]
        self.arms = self.left_arm + self.right_arm
        self.left_leg = [self.Poppy.l_hip_x, self.Poppy.l_hip_z, self.Poppy.l_hip_y, self.Poppy.l_knee_y, self.Poppy.l_ankle_y]
        self.right_leg = [self.Poppy.r_hip_x, self.Poppy.r_hip_z, self.Poppy.r_hip_y, self.Poppy.r_knee_y, self.Poppy.r_ankle_y]
        self.legs = self.left_leg + self.right_leg
        self.head = [self.Poppy.head_y, self.Poppy.head_z]
        self.torso = [self.Poppy.abs_x, self.Poppy.abs_y, self.Poppy.abs_z, self.Poppy.bust_x, self.Poppy.bust_y]
        self.body = self.head + self.torso + self.arms + self.torso

        self.possible_transitions = {Shutdown: {StandBy: {'transition': ShutdownToStandBy, 'end_state': StandBy}},
                                     StandBy: {Shutdown: {'transition': StandByToShutdown, 'end_state': Shutdown},
                                               Waving: {'transition': StartWaving, 'end_state': StandBy}}}


        # vrep normally loads Poppy standing. Bring it in shutdown state
        if self.simulation_mode == SimulationTypes.VREP:
            self.vrep_setup()
            self.print_motor_status()

        # poppy should be booted in Shutdown Mode
        self.current = Shutdown()

        # save current motor positions to file
        self.current.save_state('startup_state.json')

    def __enter__(self):
        self.go_to_state(StandBy())
        return self

    def vrep_setup(self):
        # check if mode is vrep otherwise dont proceed
        if self.simulation_mode != SimulationTypes.VREP:
            return

        # poppy model start standing in vrep. The following movement will take it to shutdown state
        self.Poppy.reset_simulation()
        self.Poppy.l_knee_y.goal_position = 45
        self.Poppy.r_knee_y.goal_position = 45
        self.Poppy.l_hip_y.goal_position = -90
        self.Poppy.r_hip_y.goal_position = -90
        self.Poppy.l_shoulder_y.goal_position = 90
        self.Poppy.r_shoulder_y.goal_position = 90
        time.sleep(0.5)
        self.Poppy.l_knee_y.goto_position(70, 2)
        self.Poppy.r_knee_y.goto_position(70, 2)
        time.sleep(0.5)
        self.Poppy.l_knee_y.goto_position(0, 2)
        self.Poppy.r_knee_y.goto_position(0, 2)
        self.Poppy.l_shoulder_x.goto_position(40, 2)
        self.Poppy.r_shoulder_x.goto_position(-40, 2)
        self.Poppy.l_shoulder_y.goto_position(-90, 3)
        self.Poppy.r_shoulder_y.goto_position(-90, 3)
        time.sleep(0.5)
        self.Poppy.l_shoulder_x.goto_position(0, 2)
        self.Poppy.r_shoulder_x.goto_position(0, 2)
        time.sleep(0.5)
        self.Poppy.r_shoulder_x.goto_position(-45.0, 2)
        self.Poppy.r_shoulder_y.goto_position(-180.0, 2)
        self.Poppy.r_arm_z.goto_position(90.0, 2)
        self.Poppy.r_elbow_y.goto_position(-45.0, 2)
        self.Poppy.l_shoulder_x.goto_position(45.0, 2)
        self.Poppy.l_shoulder_y.goto_position(-180.0, 2)
        self.Poppy.l_arm_z.goto_position(-90.0, 2)
        self.Poppy.l_elbow_y.goto_position(-45, 2)
        time.sleep(0.5)
        self.Poppy.bust_y.goto_position(45.0, 2)
        self.Poppy.abs_y.goto_position(51.3, 2)
        self.Poppy.r_hip_x.goto_position(-26.42, 2)
        self.Poppy.r_hip_z.goto_position(-23.52, 2)
        self.Poppy.r_hip_y.goto_position(-100.0, 2)
        self.Poppy.l_hip_x.goto_position(27.38, 2)
        self.Poppy.l_hip_z.goto_position(3.74, 2)
        self.Poppy.l_hip_y.goto_position(-102.09, 2)
        time.sleep(2)

        for motor in self.Poppy.motors:
            motor.goto_behavior = 'minjerk'

    # turns off compliance for an array of motors
    def turn_off_compliance(self, motors):
        if self.simulation_mode == SimulationTypes.NONE:
            return

        for motor in motors:
            motor.compliant = False

    # prints status of all motors
    def print_motor_status(self):
        if self.simulation_mode == SimulationTypes.NONE:
            return

        for motor in self.Poppy.motors:
            debug(motor.name + ': ' + str(motor.present_position))

    # looks up a possible transition
    def find_transition(self, from_state, to_state):
        if self.simulation_mode == SimulationTypes.NONE:
            return

        to_state_list = self.possible_transitions[from_state.__class__]
        transition = to_state_list[to_state.__class__]
        return transition

    # set Poppy in a new state
    def go_to_state(self, desired_state):
        if self.simulation_mode == SimulationTypes.NONE:
            return

        if self.current.is_valid(self.Poppy):  # only go to transaction if current state is valid
            if self.current.__class__ in desired_state.allowed_transitions_from:
                debug("From " + self.current.name + " To " + desired_state.name)
                # lookup transition from current state to new state
                transition = self.find_transition(self.current, desired_state)
                # set state and start the transition
                self.current = desired_state
                transition['transition']().start(self.Poppy)
                # set new state
                self.current = transition['end_state']()
            else:
                debug("Cannot go to the desired state. Current State: " + self.current.__class__.__name__ + \
                      " Desired State: " + desired_state.__class__.__name__)
        else:
            debug("The current robot position is not valid")

    def __exit__(self, exc_type, exc_val, exc_tb):
        # when object is disposed, bring poppy back to turndown state
        self.go_to_state(Shutdown())