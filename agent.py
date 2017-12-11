class Generation(object):
    def __init__(self, pop):
        self.terrain = terrain.Terrain()
        self.agents = [Agent(character) for character in pop]
        self.running = True
    def update(self):
        self.running = 0
        for agent in self.agents:
            agent.apply_force()
            agent.reward()
            agent.detect_contact()
            self.running += agent.walking
    def race(self):
        while running:
            self.update()
            self.terrain.draw_agents()
        return [agent.pos for agent in self.agents]

class Agent(object):

#pybox2d world setup, create world
#world = world(gravity = (0, -10), doSleep = True)

def _init_(self, character):
    self.right_leg = right_leg
    self.left_leg = left_leg
    self.hips = hips
    self.torso = torso
    self.neck = neck
    self.head = head

    #other class variables
    self.walking = True
    self.contacts = {}
    self.reward = 0
    self.pos = None

    #Use revoluteJoint to attach body use .getPosition()
    joint[1] = worldCreateRevoluteJoint(bodyA = head, bodyB = neck, anchor = head.worldCenter)
    joint[2] = worldCreateRevoluteJoint(bodyA = neck, bodyB = torso, anchor = torso.worldCenter)
    joint[3] = worldCreateRevoluteJoint(bodyA = torso, bodyB = right_thigh, anchor = torso.worldCenter)
    joint[4] = worldCreateRevoluteJoint(bodyA = torso, bodyB = lef_thigh, anchor = torso.worldCenter)
    joint[5] = worldCreateRevoluteJoint(bodyA = right_thigh, bodyB = right_tibia, anchor = right_thigh.worldCenter)
    joint[6] = worldCreateRevoluteJoint(bodyA = left_thigh, bodyB = left_tibia, anchor = left_thigh.worldCenter)

#joint limit and a motor enabled, setup to simulate joint friction

joint = world.CreateRevoluteJoint( bodyA=myBody1,
    bodyB=myBody2,
    anchor=myBody1.worldCenter,
    lowerAngle = -0.5 ** b2_pi, # -90 degrees
    upperAngle = 0.25 ** b2_pi, #  45 degrees
    enableLimit = True,
    maxMotorTorque = 10.0,
    motorSpeed = 0.0,
    enableMotor = True,)


#Create body shapes
#7 total = head, neck, torso, right(thigh/tibia), left(thigh/tibia)
#6 total joints
torso = world.CreateDynamicBody(position=(20, 45))
head = world.CreateDynamicBody(position=(10, 45))
#neck =
#body = world.CreateDynamicBody(position = (init_x, init_y), fixtures = fixtureDef (shape=polygonShape(vertices=[ (x/SCALE,y/SCALE) for x,y in BODY_SHAPE ]),
density=5.0, friction=0.1, categoryBits=0x0020, maskBits=0x001, restitution=0.0) # 0.99 bouncy)))


def walk(self):
    #apply forces to joints
    #joint.speed
    #joint.motorSpeed
    #joint.angle
    #joint.GetMotorTorque(inverse_dt)
    #joint.maxMotorTorque = 0

        self.joint[1].motorSpeed = float(SPEED_HIP * np.clip(action[0], -1, 1))
        self.joint[2].motorSpeed = float()
        self.joint[3].motorSpeed = float()
        self.joint[4].motorSpeed = float()
        self.joint[5].motorSpeed = float()


    #update current position

def reward(self):
    #updates self.reward to reflect head steadiness (rewards balance) and distance traveled

def detect_contact(self):
    #uses ContactDetector Class
    #when agent in contact with terrain
    #Return current contacts as dictionary
