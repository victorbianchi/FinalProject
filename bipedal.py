import Box2D
import random
from Box2D.b2 import (world, circleShape, staticBody, dynamicBody, polygonShape)

MAX_TORQUE = 1e4
WHEEL_FRICTION = 5.0
SPEED = 5

class Bipedal:

    def __init__(self, name, gene):
        self.genome = {'head': gene[0],'torso': gene[1],'right_leg': gene[2],'left_leg': gene[3]}
        self.name = name

    def build(self, world, x0, y0):
        width = self.genome['body_length']
        height = self.genome['body_width']
        length1 = self.genome['right_leg_length']
        length2 = self.genome['left_lef_length']

        body = world.CreateDynamicBody(position=(x0, y0))
        body.CreatePolygonFixture(box=(width, height), density=1, friction=0.3)

        torso = world.CreateDynamicBody(position=(x0-width*0.95, y0-height*0.85))
        torso.CreateCircleFixture(radius=length1, density=1, friction=WHEEL_FRICTION)
        world.CreateRevoluteJoint(bodyA=head, bodyB=torso,
                anchor = right_leg.worldCenter,
                maxMotorTorque = MAX_TORQUE, motorSpeed = SPEED,
                enableMotor = True)

        right_leg = world.CreateDynamicBody(position=(x0-width*0.95, y0-height*0.85))
        right_leg.CreateCircleFixture(radius=length1, density=1, friction=WHEEL_FRICTION)
        world.CreateRevoluteJoint(bodyA=body, bodyB=right_leg,
                anchor = right_leg.worldCenter,
                maxMotorTorque = MAX_TORQUE, motorSpeed = SPEED,
                enableMotor = True)

        left_leg = world.CreateDynamicBody(position=(x0+width*0.95, y0-height*0.85))
        right_leg.CreateCircleFixture(radius=length2, density=1, friction=WHEEL_FRICTION)
        world.CreateRevoluteJoint(bodyA=body, bodyB=left_leg,
                anchor = left_leg.worldCenter,
                maxMotorTorque = MAX_TORQUE, motorSpeed = SPEED,
                enableMotor = True)

        self.bodies = [body, torso, right_leg, left_leg]
        self.tracker = body.worldCenter
        # return the body object for tracking position
        return body
