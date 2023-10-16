import statistics
from typing import Union, Tuple, List, Sequence, Generator

from shapely.geometry import (
    LineString,
    LinearRing,
    MultiLineString,
    MultiPolygon,
    Polygon,
)
from shapely.geometry.base import BaseGeometry

__all__ = [
    "zero_buffer",
    "sanitise",
    "deflimmer",
    "clean_geometry",
    "explode_polygons",
    "polygon_has_interior_rings",
    "iter_polygons",
]

from warg import pairs
from jord.shapely_utilities.morphology import opening, closing
from jord.shapely_utilities.rings import ensure_ccw_ring, ensure_cw_ring


def zero_buffer(
    geom: BaseGeometry,
) -> Union[
    BaseGeometry
    # Point,
    # LineString,
    # Polygon,
    # MultiPolygon
]:
    return geom.buffer(0)


def polygon_has_interior_rings(polygon: Polygon) -> bool:
    return len(polygon.interiors) > 0


def deflimmer(geom: BaseGeometry, eps: float = 1e-7) -> BaseGeometry:
    return opening(closing(geom, eps), eps)


clean_geometry = unflimmer = deflimmer


def extract_poly_coords(geom: BaseGeometry) -> Tuple[List, List]:
    if geom.type == "Polygon":
        exterior_coords = geom.exterior.coords[:]
        interior_coords = []
        for interior in geom.interiors:
            interior_coords += interior.coords[:]
    elif geom.type == "MultiPolygon":
        exterior_coords = []
        interior_coords = []
        for part in geom:
            epc = extract_poly_coords(part)  # Recursive call
            exterior_coords += epc[0]
            interior_coords += epc[1]
    else:
        raise ValueError(f"Unhandled geometry type: {repr(geom.type)}")
    return exterior_coords, interior_coords


def extract_poly_rings(geom: BaseGeometry) -> Tuple[List, List]:
    interior_rings = []
    exterior_rings = []
    if isinstance(geom, Polygon):
        exterior_rings.append(geom.exterior)
        interior_rings.extend(geom.interiors)
    elif isinstance(geom, MultiPolygon):
        for part in geom.geoms:
            exterior_rings.append(part.exterior)
            interior_rings.extend(part.interiors)
    else:
        raise ValueError(f"Unhandled geometry type: {repr(geom.type)}")

    return exterior_rings, interior_rings


def segments(curve: Union[LinearRing, LineString]) -> List[LineString]:
    return list(map(LineString, zip(curve.coords[:-1], curve.coords[1:])))


def mean_std_dev_line_length(geom: BaseGeometry) -> Tuple[float, float]:
    line_lengths = []
    if isinstance(geom, LineString):
        for segment in segments(geom):
            line_lengths.append(segment.length)
    elif isinstance(geom, MultiLineString):
        for li in geom.geoms:
            for segment in segments(li):
                line_lengths.append(segment.length)
    elif isinstance(geom, (Polygon, MultiPolygon)):
        exterior_rings, interior_rings = extract_poly_rings(geom)
        for ex_ring in exterior_rings:
            for segment in segments(ex_ring):
                line_lengths.append(segment.length)
        for in_ring in interior_rings:
            for segment in segments(in_ring):
                line_lengths.append(segment.length)
    else:
        raise ValueError(f"Unhandled geometry type: {repr(geom.type)}")

    return (
        statistics.mean(line_lengths),
        statistics.stdev(line_lengths) if len(line_lengths) > 1 else 0,
    )


def mean_std_dev_area(geom: BaseGeometry) -> Tuple[float, float]:
    poly_areas = []
    if isinstance(geom, Polygon):
        poly_areas.append(geom.area)
    elif isinstance(geom, MultiPolygon):
        for po in geom.geoms:
            poly_areas.append(po.area)
    else:
        raise ValueError(f"Unhandled geometry type: {repr(geom.type)}")

    return (
        statistics.mean(poly_areas),
        statistics.stdev(poly_areas) if len(poly_areas) > 1 else 0,
    )


def prune_area(geom: BaseGeometry, eps: float = 1e-7) -> BaseGeometry:
    raise NotImplementedError
    poly_areas = []
    if isinstance(geom, Polygon):
        poly_areas.append(geom.area)

    elif isinstance(geom, MultiPolygon):
        for po in geom.geoms:
            poly_areas.append(po.area)

    return poly_areas


def prune_rings(geom: BaseGeometry, eps: float = 1e-7) -> BaseGeometry:
    raise NotImplementedError
    poly_areas = []
    if isinstance(geom, Polygon):
        poly_areas.append(geom.area)
    elif isinstance(geom, MultiPolygon):
        for po in geom.geoms:
            poly_areas.append(po.area)

    return poly_areas


def sanitise(geom: BaseGeometry, *args: callable) -> BaseGeometry:
    """

    #A positive distance produces a dilation, a negative distance an erosion. A very small or zero distance may sometimes be used to “tidy” a polygon.

    """

    if not len(args):
        args = (zero_buffer, deflimmer)

    for f in args:
        geom = f(geom)

    return geom


def ensure_ccw_poly(polygon: Polygon) -> Polygon:
    """
    This function checks if the polygon is counter-clockwise if not it is reversed


    :param polygon: The polygon to check
    :return: Returns the polygon turned clockwise
    """

    return Polygon(
        shell=ensure_ccw_ring(polygon.exterior),
        holes=[ensure_ccw_ring(hole) for hole in polygon.interiors],
    )


def ensure_cw_poly(polygon: Polygon) -> Polygon:
    """
    This function checks if the polygon is clockwise if not it is reversed


    :param polygon: The polygon to check
    :return: Returns the polygon turned clockwise
    """

    return Polygon(
        shell=ensure_cw_ring(polygon.exterior),
        holes=[ensure_cw_ring(hole) for hole in polygon.interiors],
    )


def iter_polygons(
    _input_geometry: BaseGeometry,
) -> Union[Generator[Polygon, None, None], Tuple[BaseGeometry]]:
    if isinstance(_input_geometry, MultiPolygon):
        return (polygon for polygon in _input_geometry.geoms)

    # assert isinstance(_input_geometry, Polygon)

    return (_input_geometry,)


def explode_polygons(
    polygons: Union[Polygon, MultiPolygon, Sequence[Polygon]],
    return_index: bool = False,
) -> Union[Sequence[LineString], Tuple[Sequence[LineString], Sequence[int]]]:
    """
    returns main line features that make up the polygons

    :param polygons:
    :param return_index:
    :return:
    """
    lines_out = []
    index = []

    if isinstance(polygons, Polygon):
        polygons = [polygons]

    if isinstance(polygons, MultiPolygon):
        polygons = polygons.geoms

    for i, l in enumerate(polygons):
        for s in [LineString(s) for s in pairs(l.exterior.coords)]:
            lines_out.append(s)
            index.append(i)

        for p in l.interiors:
            lines_out.append(LineString(p.coords))
            index.append(i)

    if return_index:
        return lines_out, index

    return lines_out


if __name__ == "__main__":

    def aishdjauisd():
        # Import constructors for creating geometry collections
        from shapely.geometry import MultiPoint, MultiLineString

        # Import necessary geometric objects from shapely module
        from shapely.geometry import Point, LineString, Polygon

        # Create Point geometric object(s) with coordinates
        point1 = Point(2.2, 4.2)
        point2 = Point(7.2, -25.1)
        point3 = Point(9.26, -2.456)
        # point3D = Point(9.26, -2.456, 0.57)

        # Create a MultiPoint object of our points 1,2 and 3
        multi_point = MultiPoint([point1, point2, point3])

        # It is also possible to pass coordinate tuples inside
        multi_point2 = MultiPoint([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])

        # We can also create a MultiLineString with two lines
        line1 = LineString([point1, point2])
        line2 = LineString([point2, point3])
        multi_line = MultiLineString([line1, line2])
        polygon = Polygon([point2, point1, point3])

        from shapely.geometry import GeometryCollection
        from matplotlib import pyplot
        import geopandas

        geoms = GeometryCollection([multi_point, multi_point2, multi_line, polygon])
        print(mean_std_dev_line_length(geoms))
        geoms = sanitise(geoms)
        print(mean_std_dev_line_length(geoms))

        p = geopandas.GeoSeries(geoms)
        p.plot()
        pyplot.show()

    def ahsudh():
        # Import constructors for creating geometry collections
        from shapely.geometry import MultiPoint, MultiLineString

        # Import necessary geometric objects from shapely module
        from shapely.geometry import Point, LineString, Polygon

        # Create Point geometric object(s) with coordinates
        point1 = Point(2.2, 4.2)
        point2 = Point(7.2, -25.1)
        point3 = Point(9.26, -2.456)
        # point3D = Point(9.26, -2.456, 0.57)

        # Create a MultiPoint object of our points 1,2 and 3
        multi_point = MultiPoint([point1, point2, point3])

        # It is also possible to pass coordinate tuples inside
        multi_point2 = MultiPoint([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])

        # We can also create a MultiLineString with two lines
        line1 = LineString([point1, point2])
        line2 = LineString([point2, point3])
        multi_line = MultiLineString([line1, line2])
        polygon = Polygon([point2, point1, point3])
        polygon2 = Polygon([point3, point2, point1])
        multi_polygon = MultiPolygon([polygon, polygon2])

        print(mean_std_dev_line_length(line1))
        print(mean_std_dev_line_length(line2))
        print(mean_std_dev_line_length(multi_line))
        print(mean_std_dev_line_length(polygon))
        print(mean_std_dev_line_length(polygon2))
        print(mean_std_dev_line_length(multi_polygon))

        print(mean_std_dev_area(polygon))
        print(mean_std_dev_area(polygon2))
        print(mean_std_dev_area(multi_polygon))

        from shapely.geometry import GeometryCollection
        from matplotlib import pyplot
        import geopandas

        geoms = GeometryCollection(
            [multi_point, multi_point2, multi_line, polygon, polygon2, multi_polygon]
        )

        p = geopandas.GeoSeries(geoms)
        p.plot()
        pyplot.show()

    ahsudh()
    # aishdjauisd()
