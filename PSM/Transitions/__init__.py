import time


class Transition:
    def __init__(self):
        raise NotImplementedError

    def start(self, poppy):
        raise NotImplementedError


class ShutdownToStandBy(Transition):
    def __init__(self):
        pass

    def start(self, poppy):
        poppy.abs_x.compliant = False
        poppy.bust_x.compliant = False

        poppy.l_hip_x.compliant = False
        poppy.l_hip_z.compliant = False
        poppy.l_hip_y.compliant = False

        poppy.r_hip_x.compliant = False
        poppy.r_hip_z.compliant = False
        poppy.r_hip_y.compliant = False

        poppy.l_hip_x.goto_position(3.47, 1)
        poppy.l_hip_z.goto_position(3.3, 1)
        poppy.l_hip_y.goto_position(-99.27, 1)
        poppy.l_knee_y.goto_position(-1.1, 1)
        poppy.l_ankle_y.goto_position(-41.45, 1)

        poppy.r_hip_x.goto_position(1.27, 1)
        poppy.r_hip_z.goto_position(-20.19, 1)
        poppy.r_hip_y.goto_position(-98.68, 1)
        poppy.r_knee_y.goto_position(-1.71, 1)
        poppy.r_ankle_y.goto_position(-39.78, 1)

        time.sleep(1)

        poppy.abs_x.compliant = False
        poppy.abs_y.compliant = False
        poppy.abs_z.compliant = False
        poppy.bust_x.compliant = False
        poppy.bust_y.compliant = False

        poppy.r_shoulder_y.compliant = False
        poppy.l_shoulder_y.compliant = False
        poppy.r_shoulder_x.compliant = False
        poppy.l_shoulder_x.compliant = False
        poppy.r_arm_z.compliant = False
        poppy.l_arm_z.compliant = False

        poppy.r_elbow_y.compliant = True
        poppy.r_elbow_y.compliant = True
        poppy.abs_y.compliant = False
        poppy.abs_x.goto_position(0, 2)
        poppy.abs_z.goto_position(0, 2)
        poppy.bust_x.goto_position(0, 2)
        poppy.r_shoulder_x.goto_position(-30.4, 1)

        time.sleep(2)

        poppy.r_shoulder_y.goto_position(-20, 3)
        poppy.l_shoulder_y.goto_position(-20, 3)
        poppy.bust_y.goto_position(0, 3)
        poppy.abs_y.goto_position(0, 3);

        time.sleep(2)

        r_arm = [poppy.r_shoulder_y, poppy.r_shoulder_x, poppy.r_arm_z, poppy.r_elbow_y]
        l_arm = [poppy.l_shoulder_y, poppy.l_shoulder_x, poppy.l_arm_z, poppy.l_elbow_y]
        for m in r_arm:
            m.compliant = True
        for m in l_arm:
            m.compliant = True

        poppy.l_knee_y.compliant = True
        poppy.r_knee_y.compliant = True
        poppy.l_knee_y.goto_position(0, 1)
        poppy.r_knee_y.goto_position(0, 1)

        poppy.r_ankle_y.compliant = False
        poppy.l_ankle_y.compliant = False
        poppy.l_ankle_y.goto_position(45.93, 2)
        poppy.r_ankle_y.goto_position(39.78, 2)

        time.sleep(1)

        poppy.l_hip_y.goto_position(-90, 2)
        poppy.r_hip_y.goto_position(-90, 2)

        time.sleep(3)
        poppy.l_knee_y.compliant = False
        poppy.r_knee_y.compliant = False


class StandByToShutdown(Transition):
    def start(self, poppy):
        poppy.r_shoulder_x.compliant = False
        poppy.r_shoulder_y.compliant = False
        poppy.r_arm_z.compliant = False
        poppy.r_elbow_y.compliant = False

        poppy.l_shoulder_x.compliant = False
        poppy.l_shoulder_y.compliant = False
        poppy.l_arm_z.compliant = False
        poppy.l_elbow_y.compliant = False

        poppy.r_shoulder_x.goto_position(-43.45, 2)
        poppy.r_shoulder_y.goto_position(-184.99, 2)
        poppy.r_arm_z.goto_position(83, 2)
        poppy.r_elbow_y.goto_position(-52, 44, 2)

        poppy.l_shoulder_x.goto_position(32.73, 2)
        poppy.l_shoulder_y.goto_position(-170.4, 2)
        poppy.l_arm_z.goto_position(-83.12, 2)
        poppy.l_elbow_y.goto_position(-44.97, 2)

        time.sleep(3.0)

        poppy.l_hip_x.compliant = False
        poppy.l_hip_z.compliant = False
        poppy.l_hip_y.compliant = False

        poppy.r_hip_x.compliant = False
        poppy.r_hip_z.compliant = False
        poppy.r_hip_y.compliant = False

        poppy.l_hip_x.goto_position(27.38, 1)
        poppy.l_hip_z.goto_position(3.74, 1)
        poppy.l_hip_y.goto_position(-102.09, 1)

        poppy.r_hip_x.goto_position(-26.42, 1)
        poppy.r_hip_z.goto_position(-23.52, 1)
        poppy.r_hip_y.goto_position(-100.0, 1)

        time.sleep(2.0)

        poppy.abs_y.compliant = False
        poppy.abs_y.goto_position(51.3, 2.5)

        poppy.bust_y.compliant = False
        poppy.bust_y.goto_position(45.32, 2.5)

        time.sleep(2.5)


class StartWaving(Transition):
    def start(self, poppy):
        r_arm = [poppy.r_shoulder_y, poppy.r_shoulder_x, poppy.r_arm_z, poppy.r_elbow_y];
        for m in r_arm:
            m.compliant = False
        poppy.r_arm_z.goto_position(-90, 1)
        poppy.r_shoulder_x.goto_position(-90, 1)
        time.sleep(1)

        for x in range(3):
            poppy.r_elbow_y.goto_position(-45, 1)
            time.sleep(1)
            poppy.r_elbow_y.goto_position(-120, 1)
            time.sleep(1)

        poppy.r_arm_z.goto_position(0, 1)
        poppy.r_shoulder_x.goto_position(0, 1)
        time.sleep(1)
        for m in r_arm:
            m.compliant = True
        time.sleep(1)
