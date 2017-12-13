import Box2D
import random
from Box2D.b2 import (world, circleShape, staticBody, dynamicBody, polygonShape)

MAX_TORQUE = 1e4
WHEEL_FRICTION = 5.0
SPEED = 5

class Bipedal:

    def __init__(self, name, gene):
        self.genome = {'wheel1_r': gene[0],'wheel2_r': gene[0],'body_length': gene[1],'body_width': gene[2]}
        self.name = name

    def build(self, world, x0, y0):
        width = self.genome['body_length']
        height = self.genome['body_width']
        radius1 = self.genome['wheel1_r']
        radius2 = self.genome['wheel2_r']

        body = world.CreateDynamicBody(position=(x0, y0))
        body.CreatePolygonFixture(box=(width, height), density=1, friction=0.3)

        wheel1 = world.CreateDynamicBody(position=(x0-width*0.95, y0-height*0.85))
        wheel1.CreateCircleFixture(radius=radius1, density=1, friction=WHEEL_FRICTION)
        world.CreateRevoluteJoint(bodyA=body, bodyB=wheel1,
                anchor = wheel1.worldCenter,
                maxMotorTorque = MAX_TORQUE, motorSpeed = SPEED,
                enableMotor = True)

        wheel2 = world.CreateDynamicBody(position=(x0+width*0.95, y0-height*0.85))
        wheel2.CreateCircleFixture(radius=radius2, density=1, friction=WHEEL_FRICTION)
        world.CreateRevoluteJoint(bodyA=body, bodyB=wheel2,
                anchor = wheel2.worldCenter,
                maxMotorTorque = MAX_TORQUE, motorSpeed = SPEED,
                enableMotor = True)

        self.bodies = [body, wheel1, wheel2]
        self.tracker = body.worldCenter
        # return the body object for tracking position
        return body
