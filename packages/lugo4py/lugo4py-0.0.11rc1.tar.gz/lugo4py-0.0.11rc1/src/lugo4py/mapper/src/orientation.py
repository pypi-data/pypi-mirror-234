from ...protos import physics_pb2
from ...src import geo

east_vector = physics_pb2.Vector()
east_vector.x = 1
east_vector.y = 0
west_vector = physics_pb2.Vector()
west_vector.x = -1
west_vector.y = 0
south_vector = physics_pb2.Vector()
south_vector.x = 0
south_vector.y = -1
north_vector = physics_pb2.Vector()
north_vector.x = 0
north_vector.y = 1
northeast_vector = physics_pb2.Vector()
northeast_vector.x = 1
northeast_vector.y = 1
northwest_vector = physics_pb2.Vector()
northwest_vector.x = -1
northwest_vector.y = 1
southeast_vector = physics_pb2.Vector()
southeast_vector.x = 1
southeast_vector.y = -1
southwest_vector = physics_pb2.Vector()
southwest_vector.x = -1
southwest_vector.y = -1

EAST = geo.normalize(east_vector)
WEST = geo.normalize(west_vector)
SOUTH = geo.normalize(south_vector)
NORTH = geo.normalize(north_vector)

NORTH_EAST = geo.normalize(northeast_vector)
NORTH_WEST = geo.normalize(northwest_vector)
SOUTH_EAST = geo.normalize(southeast_vector)
SOUTH_WEST = geo.normalize(southwest_vector)

class Orientation(object):
    pass

ORIENTATION = Orientation()
ORIENTATION.EAST = EAST
ORIENTATION.WEST = WEST
ORIENTATION.SOUTH = SOUTH
ORIENTATION.NORTH = NORTH
ORIENTATION.NORTH_EAST = NORTH_EAST
ORIENTATION.NORTH_WEST = NORTH_WEST
ORIENTATION.SOUTH_EAST = SOUTH_EAST
ORIENTATION.SOUTH_WEST = SOUTH_WEST