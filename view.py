"""
Simple visualisation using pygame.
start_game() initialises the pygame screen and clock
run(history, list_of_timelines, speed) draws the subsequent physics frames of a
    saved history for a list of timelines.
"""

import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, K_RETURN)
from pygame.color import Color
import random

import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, edgeShape, shape, vec2)

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 10.0  # pixels per meter
TARGET_FPS = 60 #60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 744

bkg_color = (255, 255, 255, 0) # white, transparent
def_color = (0, 0, 0, 255) # black, opaque

col_names = ['red', 'green', 'blue', 'orange', 'yellow', 'pink', 'azure']
obj_colors = [Color(name) for name in col_names]


def start():
    pygame.display.init()
    global screen
    # --- pygame setup ---
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Race visualisation')
    global clock
    clock = pygame.time.Clock()


# Remember to pass a list, even if single vertex
def shift_scale_revert(vertices, shift):
    """
    Take vertices and shift them, scale to pixel values and revert y coordinate
    for pygame drawing. Remember to pass a list of vertices even if one element.
    Return vertices as tuples (not vec2 anymore)
    """
    for i, vert in enumerate(vertices):
        vert = vec2(vert) + shift
        vert = [int(pos*PPM) for pos in vert]
        vert[1] = SCREEN_HEIGHT - vert[1]
        vertices[i] = tuple(vert)
    return vertices


# simple drawing (from defined points)
def draw_polygon(vertices, shift=(0,0), color=def_color, width=0):
    vertices = shift_scale_revert(vertices, shift)
    pygame.draw.polygon(screen, color, vertices, width)

def draw_circle(position, radius, shift=(0,0), color=def_color, width=0):
    position = shift_scale_revert([position], shift)
    radius = int(radius*PPM)
    pygame.draw.circle(screen, color, position, radius, width)


# shape drawing
def draw_polygonShape(polygon, shift=(0,0), color=def_color, width=0):
    vertices = shift_scale_revert(polygon.vertices, shift)
    pygame.draw.polygon(screen, color, vertices, width)
polygonShape.draw = draw_polygonShape

def draw_circleShape(circle, shift=(0,0), color=def_color, width=0):
    position = shift_scale_revert([circle.pos], shift)[0]
    radius = int(circle.radius*PPM)
    pygame.draw.circle(screen, color, position, radius, width)
circleShape.draw = draw_circleShape

def draw_edgeShape(edge, shift=(0,0), color=def_color, width=1):
    vertices = shift_scale_revert(edge.vertices, shift)
    pygame.draw.line(screen, color, vertices[0], vertices[1], width)
edgeShape.draw = draw_edgeShape


def draw_history(history, timelines, index):
    screen.fill(bkg_color)
    first = timelines[0]
    tracker = history.timelines[first].tracker_states[index]
    shift = vec2(40,20) - tracker
    drawing_func(history.terrain, shift=shift, color=def_color)
    for i, time in enumerate(reversed(timelines)):
        #objects = history.timelines[time].vehicle_states[index]
        objects = history.get_shapes(index=index, timeline=time)
        drawing_func(objects, shift=shift, color=obj_colors[i])

    # Update the screen
    pygame.display.flip()


def drawing_func(objects, shift, color):
    for obj in objects:
        # if the passed object is a b2Shape, draw it shape-wise
        if isinstance(obj, shape):
            obj.draw(shift, color)
            obj.draw(shift, def_color, width=2)


def run(history, timelines, speed=1.):
    draw_history(history, timelines, 0)

    start = False
    while not start:
        event = pygame.event.wait()
        if event.type == KEYDOWN and event.key == K_RETURN:
            start = True
        elif event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            #pygame.quit()
            return

    running = True
    n_states = history.max_length
    istate = 0

    while running:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # The user closed the window or pressed escape
                running = False

        istate += int(speed)
        if istate >= n_states:
            running = False
            continue

        try:
            draw_history(history, timelines, istate)
            clock.tick(TARGET_FPS)
        except(IndexError):
            print('Run out of bounds for first biped, finishing')
            return

    #pygame.quit()


def quit_game():
    pygame.display.quit()
pygame.quit()
