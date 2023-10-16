from enum import Enum

from shapely.geometry import (
    Point,
    LineString,
    LinearRing,
    Polygon,
    MultiPoint,
    MultiLineString,
    MultiPolygon,
    GeometryCollection,
)

__all__ = ["ShapelyGeometryTypesEnum"]


class ShapelyGeometryTypesEnum(Enum):
    """
    This enum is useful for exhaustively iterating possible shapely types.
    """

    point = Point  # Point(*args) # A geometry type that represents a single coordinate with x,y and possibly z values.

    line_string = LineString  # LineString([coordinates]) # A geometry type composed of one or more line segments.

    linear_ring = LinearRing  # LinearRing([coordinates]) # A geometry type composed of one or more line segments that forms a closed loop.

    polygon = Polygon  #  Polygon([shell, holes]) # A geometry type representing an area that is enclosed by a linear ring.

    multi_point = (
        MultiPoint  # MultiPoint([points]) # A collection of one or more Points.
    )

    multi_line_string = MultiLineString  # MultiLineString([lines]) # A collection of one or more LineStrings.

    multi_polygon = (
        MultiPolygon  # MultiPolygon([polygons]) # A collection of one or more Polygons.
    )

    geometry_collection = GeometryCollection  # GeometryCollection([geoms]) # A collection of one or more geometries that  may contain more than  one type of geometry.


if __name__ == "__main__":
    print([p.value.__name__ for p in ShapelyGeometryTypesEnum])
