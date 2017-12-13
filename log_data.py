"""
History of simulation states
Objects of class StateHistory keep the shapes (in correct positions) of all the
simulated bodies at each time step, so it can be saved and visualised
separately. See documentation of StateHistory.
Additional helper functions serve to extract the transformed shapes from body
attributes.
"""

import shelve
import Box2D  # The main library
from Box2D.b2 import (world, polygonShape, circleShape, edgeShape, vec2)
from collections import namedtuple


class Data:
    """
    History of simulation states - stores shapes for each time step
    To save memory, all static bodies are stored once for all history, an
    object with a collection of those in the .bodies attribute should be passed
    to the constructor. Dynamic bodies can be saved at each timestep via the
    save_state method, which can be called for many named timelines.
    """
    def __init__(self, terrain=None, name="history"):
        """
        Create state history
        Arguments:
            terrain:  Object with a list of static bodies in terrain.bodies
            name:   Identifier for finding in save files
        """
        self.name = name
        if terrain:
            self.terrain = get_shapes(terrain)
        else:
            self.terrain = None
        self.timelines = {}

    def set_terrain(self, terrain):
        """
        Set terrain if not given at construction (or reset)
        """
        self.terrain = get_shapes(terrain)

    Timeline = namedtuple('timeline', ['vehicle', 'vehicle_states',
        'tracker_states'])

    def new_timeline(self, vehicle, name='timeline'):
        if name in self.timelines:
            print('Warning, overwriting existing timeline "%s"' %name)
        timeline = self.Timeline(vehicle, [], [])
        self.timelines[name] = timeline
        return timeline

    def save_state(self, vehicle, timename='timeline'):
        """
        Save current state of vehicle bodies. Can also call as a method of a
        timeline without the vehicle argument.
        Arguments:
            vehicle:    Object with list of dynamic bodies in vehicle.bodies
            timename:   Name of the timeline
        """
        if timename not in self.timelines:
            self.new_timeline(vehicle, timename)
        shapes = get_shapes(vehicle)
        self.timelines[timename].vehicle_states.append(shapes)
        tracker = vec2(vehicle.tracker)
        self.timelines[timename].tracker_states.append(tracker)

    def _save_state_timeline(timeline):
        """
        Alternative way of saving a state, called as a method of a timeline
        """
        shapes = get_shapes(timeline.vehicle)
        timeline.vehicle_states.append(shapes)
        tracker = vec2(timeline.vehicle.tracker)
        timeline.tracker_states.append(tracker)
    Timeline.save_state = _save_state_timeline

    @property
    def max_length(self):
        if self.timelines:
            return max([len(self.timelines[key].vehicle_states) for key in
                                self.timelines])

    def write_to_file(self, filename):
        """
        NOT IMPLEMENTED! Store history in a file
        """
        #open file for storing the history
        shelf = shelve.open(filename)
        # TODO: use self.name?
        shelf.setdefault('histories', [])
        hist_list = shelf['histories']
        hist_list.append(history)
        shelf['histories'] = hist_list
        shelf.close()

    def read_from_file(self, filename):
        """
        NOT IMPLEMENTED! Load history from a file
        """
        pass

    def get_shapes(self, index, timeline='timeline'):
        """
        Return all shapes of the vehicle in correct positions
        Arguments:
            index:      index of the entry in the history
            timeline:   name of the timeline ('timeline' by default)
        """
        return self.timelines[timeline].vehicle_states[index]


# Module function to get the shapes from bodies
def get_shapes(instance):
    shapes = []
    for body in instance.bodies:
        for fixture in body:
            shapes.append( fixture.shape.get_transformed_shape(body) )
    return shapes

# Helper functions to extract shapes in their correct positions
#   Add them as methods to the shape classes for 'polymorphic' calls
def get_transformed_edge(edge, body):
    new_vertices = [tuple(body.transform * v) for v in edge.vertices]
    return edgeShape(vertices=new_vertices)
edgeShape.get_transformed_shape = get_transformed_edge

def get_transformed_polygon(polygon, body):
    new_vertices = [tuple(body.transform * v) for v in polygon.vertices]
    return polygonShape(vertices=new_vertices)
polygonShape.get_transformed_shape = get_transformed_polygon

def get_transformed_circle(circle, body):
    new_pos = tuple(body.transform * circle.pos)
    return circleShape(pos=new_pos, radius=circle.radius)
circleShape.get_transformed_shape = get_transformed_circle


# Old version, keep for debugging
def get_params_polygon(polygon, body):
    vertices = [tuple(body.transform * v) for v in polygon.vertices]
    return 'polygon', vertices
polygonShape.get_params = get_params_polygon

def get_params_circle(circle, body):
    position = tuple(body.transform * circle.pos)
    radius = circle.radius
    return 'circle', (position, radius)
circleShape.get_params = get_params_circle
