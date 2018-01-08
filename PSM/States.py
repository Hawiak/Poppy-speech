import jsonpickle
from helpers import debug


class State:
    def is_valid(self, poppy):
        for motor_state in self.motor_states:
            if not motor_state.is_valid(poppy):
                debug(motor_state.motor.name + ' is not in valid state ' + self.name)
                debug('{0} should be between {1} and {2}'.format(str(motor_state.motor.get_position(poppy)),
                                                                 str(motor_state.valid_min_position),
                                                                 str(motor_state.valid_max_position)))
                return False
        return True

    def save_state(self, filename):
        json_str = jsonpickle.encode(self)
        output_file = open(filename, 'w')
        output_file.write(json_str)
        output_file.close()

    def __init__(self, name):
        self.name = name
        self.motor_states = [
                       MotorState(-180, 180, 0, 11, 'l_hip_x'),
                       MotorState(-180, 180, 0, 12, 'l_hip_z'),
                       MotorState(-180, 180, 0, 13, 'l_hip_y'),
                       MotorState(-180, 180, 0, 14, 'l_knee_y'),
                       MotorState(-180, 180, 0, 15, 'l_ankle_y'),
                       MotorState(-180, 180, 0, 21, 'r_hip_x'),
                       MotorState(-180, 180, 0, 22, 'r_hip_z'),
                       MotorState(-180, 180, 0, 23, 'r_hip_y'),
                       MotorState(-180, 180, 0, 24, 'r_knee_y'),
                       MotorState(-180, 180, 0, 25, 'r_ankle_y'),
                       MotorState(-180, 180, 0, 31, 'abs_y'),
                       MotorState(-180, 180, 0, 32, 'abs_x'),
                       MotorState(-180, 180, 0, 33, 'abs_z'),
                       MotorState(-180, 180, 0, 34, 'bust_y'),
                       MotorState(-180, 180, 0, 35, 'bust_x'),
                       MotorState(-180, 180, 0, 36, 'head_z'),
                       MotorState(-180, 180, 0, 37, 'head_y'),
                       MotorState(-180, 180, 0, 41, 'l_shoulder_y'),
                       MotorState(-180, 180, 0, 42, 'l_shoulder_x'),
                       MotorState(-180, 180, 0, 43, 'l_arm_z'),
                       MotorState(-180, 180, 0, 44, 'l_elbow_y'),
                       MotorState(-180, 180, 0, 51, 'r_shoulder_y'),
                       MotorState(-180, 180, 0, 52, 'r_shoulder_x'),
                       MotorState(-180, 180, 0, 53, 'r_arm_z'),
                       MotorState(-180, 180, 0, 54, 'r_elbow_y')]


class MotorState:
    def is_valid(self, poppy):
        # type: (Callable[MotorState]) -> bool
        if self.valid_min_position <= self.motor.get_position(poppy) <= self.valid_max_position:
            return True
        return False

    def __init__(self, valid_min_position, valid_max_position, wanted_position, motor_id, motor_name):
        self.valid_min_position = valid_min_position
        self.valid_max_position = valid_max_position
        self.wanted_position = wanted_position
        self.motor = Motor(motor_id, motor_name)


class Motor:
    def __init__(self, motor_id, name):
        self.id = motor_id
        self.position = 0
        self.name = name

    def get_position(self, poppy):
        return getattr(getattr(poppy, self.name), "present_position")


class Shutdown(State):

    def __init__(self):
        self.name = 'Shutdown State'
        self.allowed_transitions_from = [StandBy]
        self.motor_states = [
                       MotorState(25, 29, 27.38, 11, 'l_hip_x'),
                       MotorState(12.5, 23.5, 17.5, 12, 'l_hip_z'),
                       MotorState(-105, -100, -102.09, 13, 'l_hip_y'),
                       MotorState(-180, 180, 0, 14, 'l_knee_y'),
                       MotorState(-180, 180, 0, 15, 'l_ankle_y'),
                       MotorState(-29, -25, -27.38, 21, 'r_hip_x'),
                       MotorState(-25, -20, -23.52, 22, 'r_hip_z'),
                       MotorState(-102.5, -97.5, -100, 23, 'r_hip_y'),
                       MotorState(-180, 180, 0, 24, 'r_knee_y'),
                       MotorState(-180, 180, 0, 25, 'r_ankle_y'),
                       MotorState(47.5, 52.5, 50.0, 31, 'abs_y'),
                       MotorState(-180, 180, 0, 32, 'abs_x'),
                       MotorState(-180, 180, 0, 33, 'abs_z'),
                       MotorState(35, 47.5, 45, 34, 'bust_y'),
                       MotorState(-180, 180, 0, 35, 'bust_x'),
                       MotorState(-180, 180, 0, 36, 'head_z'),
                       MotorState(-180, 180, 0, 37, 'head_y'),
                       MotorState(-182.5, -177.5, -180, 41, 'l_shoulder_y'),
                       MotorState(42.5, 47.5, 45, 42, 'l_shoulder_x'),
                       MotorState(-92.5, -87.5, -90, 43, 'l_arm_z'),
                       MotorState(-180, 180, 0, 44, 'l_elbow_y'),
                       MotorState(-182.5, -177.5, -180, 51, 'r_shoulder_y'),
                       MotorState(-50.0, -45.0, -47.5, 52, 'r_shoulder_x'),
                       MotorState(87.5, 92.5, 90, 53, 'r_arm_z'),
                       MotorState(-47.5, -42.5, -45, 54, 'r_elbow_y')]


class StandBy(State):
    def __init__(self):
        self.name = 'Sitting up State'
        self.allowed_transitions_from = [Shutdown, Waving]
        self.motor_states = [
                       MotorState(-180, 180, 0, 11, 'l_hip_x'),
                       MotorState(-180, 180, 0, 12, 'l_hip_z'),
                       MotorState(-180, 180, 0, 13, 'l_hip_y'),
                       MotorState(-180, 180, 0, 14, 'l_knee_y'),
                       MotorState(-180, 180, 0, 15, 'l_ankle_y'),
                       MotorState(-180, 180, 0, 21, 'r_hip_x'),
                       MotorState(-180, 180, 0, 22, 'r_hip_z'),
                       MotorState(-180, 180, 0, 23, 'r_hip_y'),
                       MotorState(-180, 180, 0, 24, 'r_knee_y'),
                       MotorState(-180, 180, 0, 25, 'r_ankle_y'),
                       MotorState(-180, 180, 0, 31, 'abs_y'),
                       MotorState(-180, 180, 0, 32, 'abs_x'),
                       MotorState(-180, 180, 0, 33, 'abs_z'),
                       MotorState(-180, 180, 0, 34, 'bust_y'),
                       MotorState(-180, 180, 0, 35, 'bust_x'),
                       MotorState(-180, 180, 0, 36, 'head_z'),
                       MotorState(-180, 180, 0, 37, 'head_y'),
                       MotorState(-180, 180, 0, 41, 'l_shoulder_y'),
                       MotorState(-180, 180, 0, 42, 'l_shoulder_x'),
                       MotorState(-180, 180, 0, 43, 'l_arm_z'),
                       MotorState(-180, 180, 0, 44, 'l_elbow_y'),
                       MotorState(-180, 180, 0, 51, 'r_shoulder_y'),
                       MotorState(-180, 180, 0, 52, 'r_shoulder_x'),
                       MotorState(-180, 180, 0, 53, 'r_arm_z'),
                       MotorState(-180, 180, 0, 54, 'r_elbow_y')]


class Waving(State):
    def __init__(self):
        self.name = 'Waving State'
        self.allowed_transitions_from = [StandBy]
        self.motor_states = [
                       MotorState(-180, 180, 0, 11, 'l_hip_x'),
                       MotorState(-180, 180, 0, 12, 'l_hip_z'),
                       MotorState(-180, 180, 0, 13, 'l_hip_y'),
                       MotorState(-180, 180, 0, 14, 'l_knee_y'),
                       MotorState(-180, 180, 0, 15, 'l_ankle_y'),
                       MotorState(-180, 180, 0, 21, 'r_hip_x'),
                       MotorState(-180, 180, 0, 22, 'r_hip_z'),
                       MotorState(-180, 180, 0, 23, 'r_hip_y'),
                       MotorState(-180, 180, 0, 24, 'r_knee_y'),
                       MotorState(-180, 180, 0, 25, 'r_ankle_y'),
                       MotorState(-180, 180, 0, 31, 'abs_y'),
                       MotorState(-180, 180, 0, 32, 'abs_x'),
                       MotorState(-180, 180, 0, 33, 'abs_z'),
                       MotorState(-180, 180, 0, 34, 'bust_y'),
                       MotorState(-180, 180, 0, 35, 'bust_x'),
                       MotorState(-180, 180, 0, 36, 'head_z'),
                       MotorState(-180, 180, 0, 37, 'head_y'),
                       MotorState(-180, 180, 0, 41, 'l_shoulder_y'),
                       MotorState(-180, 180, 0, 42, 'l_shoulder_x'),
                       MotorState(-180, 180, 0, 43, 'l_arm_z'),
                       MotorState(-180, 180, 0, 44, 'l_elbow_y'),
                       MotorState(-180, 180, 0, 51, 'r_shoulder_y'),
                       MotorState(-180, 180, 0, 52, 'r_shoulder_x'),
                       MotorState(-180, 180, 0, 53, 'r_arm_z'),
                       MotorState(-180, 180, 0, 54, 'r_elbow_y')]
