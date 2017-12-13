import Box2D
import random
from Box2D.b2 import (world, circleShape, staticBody, dynamicBody, polygonShape)

MAX_TORQUE = 1e4
WHEEL_FRICTION = 5.0
SPEED = 5

class Bipedal:

    def __init__(self, name, gene):
        self.genome = {'width': gene[0],'height': gene[1],'right_leg': gene[2],'left_leg': gene[2]}
        self.name = name

    def build(self, world, x0, y0):
        width = self.genome['width']
        height = self.genome['height']
        length1 = self.genome['right_leg']
        length2 = self.genome['left_leg']

        body = world.CreateDynamicBody(position=(x0, y0))
        body.CreatePolygonFixture(box=(width, height), density=1, friction=0.3)

        head = world.CreateDynamicBody(position=(x0, y0+4))
        head.CreateCircleFixture(radius = 1.8, density=1, friction=0.3)

        neck = world.CreateDynamicBody(position=(x0, y0+2.5))
        neck.CreatePolygonFixture(box = (0.5, 1), density=1, friction=WHEEL_FRICTION)

        world.CreateRevoluteJoint(bodyA=head, bodyB=neck, anchor = head.worldCenter, enableMotor = False)
        world.CreateRevoluteJoint(bodyA=neck, bodyB=body, anchor = body.worldCenter, enableMotor = False)

        right_leg = world.CreateDynamicBody(position=(x0+0.2, y0-2))
        right_leg.CreatePolygonFixture(box = (0.5,3), density=1, friction=WHEEL_FRICTION)
        world.CreateRevoluteJoint(bodyA=right_leg, bodyB=body,
                anchor = body.worldCenter,
                lowerAngle = -0.5 * 3.14, upperAngle = 0.5 * 3.14, enableLimit = True,
                maxMotorTorque = MAX_TORQUE, motorSpeed = SPEED,
                enableMotor = True)

        left_leg = world.CreateDynamicBody(position=(x0-0.2, y0-2))
        left_leg.CreatePolygonFixture(box = (0.5,3), density=1, friction=WHEEL_FRICTION)
        world.CreateRevoluteJoint(bodyA=left_leg, bodyB=right_leg,
                anchor = body.worldCenter,
                lowerAngle = -0.5 * 3.14, upperAngle = 0.5 * 3.14,
                enableLimit = True,
                maxMotorTorque = MAX_TORQUE, motorSpeed = SPEED,
                enableMotor = True)
        #left_leg = world.CreateDynamicBody(position=(x0+width*0.95, y0-height*0.85))
        #right_leg.CreatePolygonFixture(box= (3,6), density=1, friction=WHEEL_FRICTION)
        #world.CreateRevoluteJoint(bodyA=body, bodyB=left_leg,
        #        anchor = left_leg.worldCenter,
        #        maxMotorTorque = MAX_TORQUE, motorSpeed = SPEED,
        #        enableMotor = True)

        self.bodies = [body, head, neck, right_leg, left_leg]
        self.tracker = body.worldCenter
        # return the body object for tracking position
        return body
