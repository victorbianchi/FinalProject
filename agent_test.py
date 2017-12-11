import Box2D
from Box2D.b2 import (edgeShape, circleShape, fixtureDef, polygonShape, revoluteJointDef, contactListener)
import numpy as np

start = 20
wndw_height = 400
wndw_width = 600
step = 1
FPS = 40.0
grass_height = wndw_height/4
grass_length = 10

class ContactDetector(contactListener):
    def __init__(self, env):
        contactListener.__init__(self)
        self.env = env
    def BeginContact(self, contact):
        if self.env.hull==contact.fixtureA.body or self.env.hull==contact.fixtureB.body:
            self.env.game_over = True
        for leg in [self.env.legs[1], self.env.legs[3]]:
            if leg in [contact.fixtureA.body, contact.fixtureB.body]:
                leg.ground_contact = True
    def EndContact(self, contact):
        for leg in [self.env.legs[1], self.env.legs[3]]:
            if leg in [contact.fixtureA.body, contact.fixtureB.body]:
                leg.ground_contact = False

class Agent(object):

    def __init__(self, character, world):
        leg_h = character.gene[0]/5.0
        leg_w = character.gene[1]/5.0
        self.world = world
        self.hull = None
        self.legs = []
        self.joints = []
        self.init_x = step * start/2
        self.init_y = grass_height + 2*leg_h
        self.hull_density = 5.0
        self.leg_density = 1.0
        self.friction = 0.1
        self.hull_vertices = [(-30,+9), (+6,+9), (+34,+1),(+34,-8), (-30,-8)]
        self.leg_height = leg_h
        self.leg_width = leg_w
        self.motors_torque = 80
        self.leg_down = -0.25
        self.speed_hip = 4
        self.speed_knee = 6
        self.state = []
        self.game_over = False
        self.prev_shaping = None

    def define_hull(self):
        self.hull = self.world.CreateDynamicBody(
            position = (self.init_x, self.init_y),
            fixtures = fixtureDef(
                shape=polygonShape(vertices=self.hull_vertices),
                density=self.hull_density,
                friction=self.friction,
                categoryBits=0x0020,
                maskBits=0x001,  # collide only with ground
                restitution=0.0) # 0.99 bouncy
                )
        self.hull.color1 = (0.5,0.4,0.9)
        self.hull.color2 = (0.3,0.3,0.5)

    def define_legs(self):
        for i in [-1,+1]:
            leg = self.world.CreateDynamicBody(
                position = (self.init_x, self.init_y - self.leg_height/2 - self.leg_down),
                angle = (i*0.05),
                fixtures = fixtureDef(
                    shape=polygonShape(box=(self.leg_width/2, self.leg_height/2)),
                    density=1.0,
                    restitution=0.0,
                    categoryBits=0x0020,
                    maskBits=0x001)
                )
            leg.color1 = (0.6-i/10., 0.3-i/10., 0.5-i/10.)
            leg.color2 = (0.4-i/10., 0.2-i/10., 0.3-i/10.)
            rjd = revoluteJointDef(
                bodyA=self.hull,
                bodyB=leg,
                localAnchorA=(0, self.leg_down),
                localAnchorB=(0, self.leg_height/2),
                enableMotor=True,
                enableLimit=True,
                maxMotorTorque=self.motors_torque,
                motorSpeed = i,
                lowerAngle = -0.8,
                upperAngle = 1.1,
                )
            self.legs.append(leg)
            self.joints.append(self.world.CreateJoint(rjd))

            lower = self.world.CreateDynamicBody(
                position = (self.init_x, self.init_y - self.leg_height*3/2 - self.leg_down),
                angle = (i*0.05),
                fixtures = fixtureDef(
                    shape=polygonShape(box=(0.8*self.leg_width/2, self.leg_height/2)),
                    density=1.0,
                    restitution=0.0,
                    categoryBits=0x0020,
                    maskBits=0x001)
                )
            lower.color1 = (0.6-i/10., 0.3-i/10., 0.5-i/10.)
            lower.color2 = (0.4-i/10., 0.2-i/10., 0.3-i/10.)
            rjd = revoluteJointDef(
                bodyA=leg,
                bodyB=lower,
                localAnchorA=(0, -self.leg_height/2),
                localAnchorB=(0, self.leg_height/2),
                enableMotor=True,
                enableLimit=True,
                maxMotorTorque=self.motors_torque,
                motorSpeed = 1,
                lowerAngle = -1.6,
                upperAngle = -0.1,
                )
            lower.ground_contact = False
            self.legs.append(lower)
            self.joints.append(self.world.CreateJoint(rjd))


    def update_state(self, action):
        self.joints[0].motorSpeed     = float(self.speed_hip     * np.sign(action[0]))
        self.joints[0].maxMotorTorque = float(self.motors_torque * np.clip(np.abs(action[0]), 0, 1))
        self.joints[1].motorSpeed     = float(self.speed_knee    * np.sign(action[1]))
        self.joints[1].maxMotorTorque = float(self.motors_torque * np.clip(np.abs(action[1]), 0, 1))
        self.joints[2].motorSpeed     = float(self.speed_hip     * np.sign(action[2]))
        self.joints[2].maxMotorTorque = float(self.motors_torque * np.clip(np.abs(action[2]), 0, 1))
        self.joints[3].motorSpeed     = float(self.speed_knee    * np.sign(action[3]))
        self.joints[3].maxMotorTorque = float(self.motors_torque * np.clip(np.abs(action[3]), 0, 1))

        self.world.Step(1.0/FPS, 6*30, 2*30)

        pos = self.hull.position
        vel = self.hull.linearVelocity

        self.state = [
            self.hull.angle,        # body angle
            2.0*self.hull.angularVelocity/FPS, #
            0.3*vel.x*wndw_width/FPS,  # Normalized to get -1..1 range
            0.3*vel.y*wndw_height/FPS,
            self.joints[0].angle,   # This will give 1.1 on high up, but it's still OK (and there should be spikes on hiting the ground, that's normal too)
            self.joints[0].speed / self.speed_hip,
            self.joints[1].angle + 1.0,
            self.joints[1].speed / self.speed_knee,
            1.0 if self.legs[1].ground_contact else 0.0,
            self.joints[2].angle,
            self.joints[2].speed / self.speed_hip,
            self.joints[3].angle + 1.0,
            self.joints[3].speed / self.speed_knee,
            1.0 if self.legs[3].ground_contact else 0.0
            ]
        assert len(self.state)==14

        shaping  = 130*pos[0]   # moving forward is a way to receive reward (normalized to get 300 on completion)
        shaping -= 5.0*abs(self.state[0])  # keep head straight, other than that and falling, any behavior is unpunished

        reward = 0
        if self.prev_shaping is not None:
            reward = shaping - self.prev_shaping
        self.prev_shaping = shaping

        for a in action:
            reward -= 0.00035 * self.motors_torque * np.clip(np.abs(a), 0, 1)
            # normalized to about -50.0 using heuristic, more optimal agent should spend less

        done = False
        if self.game_over or pos[0] < 0:
            reward = -100
            done   = True
        if pos[0] > (wndw_width-grass_length)*step:
            done   = True
        return np.array(self.state), reward, done, {}

    def walk(self):
        steps = 0
        total_reward = 0
        STAY_ON_ONE_LEG, PUT_OTHER_DOWN, PUSH_OFF = 1,2,3
        state = STAY_ON_ONE_LEG
        past_speeds = []
        a = np.array([0.0, 0.0, 0.0, 0.0])
        SPEED = 0.29
        moving_leg = 0
        supporting_leg = 1 - moving_leg
        SUPPORT_KNEE_ANGLE = +0.1
        supporting_knee_angle = SUPPORT_KNEE_ANGLE
        while True:
            s, r, done, info = self.update_state(a)
            total_reward += r
            steps += 1

            past_speeds.append([self.joints[0].motorSpeed, self.joints[1].motorSpeed, self.joints[2].motorSpeed, self.joints[3].motorSpeed])
            if len(past_speeds) > 200:
                del past_speeds[0]
                if all(past_speeds[0] == rest for rest in past_speeds):
                    done = True
                    total_reward = total_reward - 100.0

            contact0 = s[8]
            contact1 = s[13]
            moving_s_base = 4 + 5*moving_leg
            supporting_s_base = 4 + 5*supporting_leg

            hip_targ  = [None,None]   # -0.8 .. +1.1
            knee_targ = [None,None]   # -0.6 .. +0.9
            hip_todo  = [0.0, 0.0]
            knee_todo = [0.0, 0.0]

            if state==STAY_ON_ONE_LEG:
                hip_targ[moving_leg]  = 1.1
                knee_targ[moving_leg] = -0.6
                supporting_knee_angle += 0.03
                if s[2] > SPEED: supporting_knee_angle += 0.03
                supporting_knee_angle = min( supporting_knee_angle, SUPPORT_KNEE_ANGLE )
                knee_targ[supporting_leg] = supporting_knee_angle
                if s[supporting_s_base+0] < 0.10: # supporting leg is behind
                    state = PUT_OTHER_DOWN
            if state==PUT_OTHER_DOWN:
                hip_targ[moving_leg]  = +0.1
                knee_targ[moving_leg] = SUPPORT_KNEE_ANGLE
                knee_targ[supporting_leg] = supporting_knee_angle
                if s[moving_s_base+4]:
                    state = PUSH_OFF
                    supporting_knee_angle = min( s[moving_s_base+2], SUPPORT_KNEE_ANGLE )
            if state==PUSH_OFF:
                knee_targ[moving_leg] = supporting_knee_angle
                knee_targ[supporting_leg] = +1.0
                if s[supporting_s_base+2] > 0.88 or s[2] > 1.2*SPEED:
                    state = STAY_ON_ONE_LEG
                    moving_leg = 1 - moving_leg
                    supporting_leg = 1 - moving_leg

            if hip_targ[0]: hip_todo[0] = 0.9*(hip_targ[0] - s[4]) - 0.25*s[5]
            if hip_targ[1]: hip_todo[1] = 0.9*(hip_targ[1] - s[9]) - 0.25*s[10]
            if knee_targ[0]: knee_todo[0] = 4.0*(knee_targ[0] - s[6])  - 0.25*s[7]
            if knee_targ[1]: knee_todo[1] = 4.0*(knee_targ[1] - s[11]) - 0.25*s[12]

            hip_todo[0] -= 0.9*(0-s[0]) - 1.5*s[1] # PID to keep head strait
            hip_todo[1] -= 0.9*(0-s[0]) - 1.5*s[1]
            knee_todo[0] -= 15.0*s[3]  # vertical speed, to damp oscillations
            knee_todo[1] -= 15.0*s[3]

            a[0] = hip_todo[0]
            a[1] = knee_todo[0]
            a[2] = hip_todo[1]
            a[3] = knee_todo[1]
            a = np.clip(0.5*a, -1.0, 1.0)
            if done:
                return total_reward
