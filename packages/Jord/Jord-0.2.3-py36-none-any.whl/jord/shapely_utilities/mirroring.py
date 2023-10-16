__all__ = ["reflection"]


# pts = numpy.array([[0, 0], [1, 1], [1, 2], [0, 1]])
# display(Polygon(pts.dot([[1,0],[0,-1]])))


def principal_axis():
    ...


from shapely.affinity import scale
from shapely.geometry import Polygon
from shapely.ops import transform


def reflection(x0):
    return lambda x, y: (2 * x0 - x, y)


P = Polygon([[0, 0], [1, 1], [1, 2], [0, 1]])
print(P)  # POLYGON ((0 0, 1 1, 1 2, 0 1, 0 0))

Q1 = scale(P, xfact=-1, origin=(1, 0))  # X-axis
# scale(P, yfact = -1, origin = (1, 0)) # Y-axis
Q2 = transform(reflection(1), P)

print(Q1)  # POLYGON ((2 0, 1 1, 1 2, 2 1, 2 0))
print(Q2)  # POLYGON ((2 0, 1 1, 1 2, 2 1, 2 0))
