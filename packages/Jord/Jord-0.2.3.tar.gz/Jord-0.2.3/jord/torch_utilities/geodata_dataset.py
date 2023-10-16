from shapely.geometry import Polygon
from shapely.ops import clip_by_rect

polygon = Polygon(
    shell=[(0, 0), (0, 30), (30, 30), (30, 0), (0, 0)],
    holes=[[(10, 10), (20, 10), (20, 20), (10, 20), (10, 10)]],
)
clipped_polygon = clip_by_rect(polygon, 5, 5, 15, 15)
