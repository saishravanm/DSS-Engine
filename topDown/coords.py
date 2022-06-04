from typing import Tuple


class CoordConverter:

    def __init__(self, scale: Tuple[float, float], viewport: Tuple[Tuple[int, int], Tuple[int, int]]):
        self.scale = scale
        self.viewport = viewport

    def from_universe(self, point: Tuple[int, int]) -> Tuple[int, int]:
        (x_scale, y_scale) = self.scale
        (x, y) = point
        ((xv, yv), (_, _)) = self.viewport

        return (int((x - xv) / x_scale), int((y - yv) / y_scale))

    def to_universe(self, point: Tuple[int, int]) -> Tuple[int, int]:
        (x_scale, y_scale) = self.scale
        (x, y) = point
        ((xv, yv), (_, _)) = self.viewport

        return (int(x * x_scale + xv), int(y * y_scale + yv))