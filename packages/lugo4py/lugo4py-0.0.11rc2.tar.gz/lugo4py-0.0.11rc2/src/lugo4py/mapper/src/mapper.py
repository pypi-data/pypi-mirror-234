from ...protos import physics_pb2
from ...protos import server_pb2

from ...src import specs

from math import floor

# ErrMinCols defines an error for invalid number of cols
ERR_MIN_COLS = AttributeError("number of cols lower the minimum")
# ErrMaxCols defines an error for invalid number of cols
ERR_MAX_COLS = AttributeError("number of cols higher the maximum")
# ErrMinRows defines an error for invalid number of rows
ERR_MIN_ROWS = AttributeError("number of rows lower the minimum")
# ErrMaxRows defines an error for invalid number of rows
ERR_MAX_ROWS = AttributeError("number of rows higher the maximum")

# MinCols Define the min number of cols allowed on the field division by the Mapper
MIN_COLS = 4
# MinRows Define the min number of rows allowed on the field division by the Mapper
MIN_ROWS = 2
# MaxCols Define the max number of cols allowed on the field division by the Mapper
MAX_COLS = 200
# MaxRows Define the max number of rows allowed on the field division by the Mapper
MAX_ROWS = 100


def mirror_coords_to_away(center):
    mirrored = physics_pb2.Point()
    mirrored.x = (specs.MAX_X_COORDINATE - center.x)
    mirrored.y = (specs.MAX_Y_COORDINATE - center.y)
    return mirrored


class Region:
    def __init__(self, col: int, row: int, side: server_pb2.Team.Side, center: physics_pb2.Point, mapper):
        self.col = col
        self.row = row
        self.side = side
        self.center = center
        self.positioner = mapper

    def eq(self, region):
        return region.get_col() == self.col and region.side == self.side and region.get_row() == self.row

    def get_col(self):
        return self.col

    def get_row(self):
        return self.row

    def get_center(self):
        return self.center

    def to_string(self):
        return f"{{{self.col}, {self.row}}}"

    def front(self):
        return self.positioner.get_region(max(self.col + 1, 0), self.row)

    def back(self):
        return self.positioner.get_region(max(self.col - 1, 0), self.row)

    def left(self):
        return self.positioner.get_region(self.col, max(self.row + 1, 0))

    def right(self):
        return self.positioner.get_region(self.col, max(self.row - 1, 0))


class Mapper:
    def __init__(self, cols: int, rows: int, side: server_pb2.Team.Side):
        if cols < MIN_COLS:
            raise ERR_MIN_COLS

        if cols > MAX_COLS:
            raise ERR_MAX_COLS

        if rows < MIN_ROWS:
            raise ERR_MIN_ROWS

        if rows > MAX_ROWS:
            raise ERR_MAX_ROWS

        self.cols = cols
        self.rows = rows
        self.side = side
        self.regionWidth = specs.MAX_X_COORDINATE / cols
        self.regionHeight = specs.MAX_Y_COORDINATE / rows

    def get_region(self, col: int, row: int) -> Region:
        col = max(0, col)
        col = min(self.cols - 1, col)

        row = max(0, row)
        row = min(self.rows - 1, row)

        center = physics_pb2.Point()
        center.x = (round((col * self.regionWidth) + (self.regionWidth / 2)))
        center.y = (round((row * self.regionHeight) + (self.regionHeight / 2)))

        if self.side == server_pb2.Team.Side.AWAY:
            center = mirror_coords_to_away(center)

        return Region(
            col,
            row,
            self.side,
            center,
            self,
        )

    def get_region_from_point(self, point: physics_pb2.Point):
        if self.side == server_pb2.Team.Side.AWAY:
            point = mirror_coords_to_away(point)

        cx = floor(point.x / self.regionWidth)
        cy = floor(point.y / self.regionHeight)
        col = min(cx, self.cols - 1)
        row = min(cy, self.rows - 1)
        return self.get_region(col, row)


