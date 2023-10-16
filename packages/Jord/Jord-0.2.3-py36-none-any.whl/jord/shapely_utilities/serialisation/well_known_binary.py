from pathlib import Path

import pandas
from shapely import wkb

__all__ = ["load_wkbs_from_csv", "csv_wkt_generator"]


def load_wkbs_from_csv(csv_file_path: Path, geometry_column: str = "Shape") -> wkb:
    """
    Well-Known Text
    """
    return pandas.read_csv(str(csv_file_path))[geometry_column].apply(wkb.loads)


def csv_wkt_generator(csv_file_path: Path, geometry_column: str = "Shape") -> wkb:
    """

    :param csv_file_path:
    :param geometry_column:
    :return:
    """
    for idx, g in pandas.read_csv(
        str(csv_file_path), usecols=[geometry_column]
    ).iterrows():
        yield wkb.loads(g)
