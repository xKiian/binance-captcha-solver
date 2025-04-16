from random import randint, uniform, randrange
from math import hypot
from time import time

"""
I initially wanted to make a solver for type IMAGE, but my python version always gets type SLIDE lmfao
"""

TILE_SIZE = 110
TILES = {  # "pos" is top left position
    0: {"id": "10", "pos": (145, 311)},
    1: {"id": "11", "pos": (259, 311)},
    2: {"id": "12", "pos": (373, 311)},

    3: {"id": "13", "pos": (145, 425)},
    4: {"id": "14", "pos": (259, 425)},
    5: {"id": "15", "pos": (373, 425)},

    6: {"id": "16", "pos": (145, 539)},
    7: {"id": "17", "pos": (259, 539)},
    8: {"id": "18", "pos": (373, 539)},

    # verify/next button
    "vb": {"id": "vb", "pos": (355, 673), "size": (127 - 2, 40 - 2)},
}


class Point:
    def __init__(self, x, y, button_id="", rel_x=-1, rel_y=-1):
        self.x = x
        self.y = y
        self.button_id = button_id
        self.rel_x = rel_x
        self.rel_y = rel_y

    def __str__(self):
        return f"({self.x}, {self.y}, {self.button_id}, {self.rel_x}, {self.rel_y})"


class MouseMovement:
    def __init__(self, ):
        self.points = []
        self.mm = []

        self.mm_count = 0
        self.cl_count = 0
        self.mu_count = 0

        self.first = True

    def _generate_points_image(self, solution: dict):
        def gen(page: int):
            for point in solution[page]:
                tile = TILES[point]
                rand_x = randint(10, 100)
                rand_y = randint(10, 100)

                pos = tile["pos"]

                self.points.append(Point(pos[0] + rand_x, pos[1] + rand_y, tile["id"], rand_x, rand_y))

        def next_page():
            vb_tile = TILES["vb"]
            vb_rand_x = randint(2, vb_tile["size"][0])
            vb_rand_y = randint(2, vb_tile["size"][1])
            self.points.append(
                Point(vb_tile["pos"][0] + vb_rand_x,
                      vb_tile["pos"][1] + vb_rand_y,
                      "vb", vb_rand_x, vb_rand_y)
            )

        self.points.append(Point(
            312 + randrange(-100, 100),
            307 + randrange(-20, 20),
            "", -1, -1)
        )

        gen(0)
        next_page()
        gen(1)
        next_page()

    def _generate_points_slide(self):
        self.points.append(Point(
            312 + randrange(-100, 100),
            307 + randrange(-20, 20),
            "", -1, -1)
        )

        self.points.append(Point(
            757 + randrange(-10, 10),
            354 + randrange(-20, 20),
            "", -1, -1)
        )

        self.points.append(Point(
            806 + randrange(-10, 10),
            349 + randrange(-20, 20),
            "", -1, -1)
        )

    @staticmethod
    def connect_points(p1: Point, p2: Point):
        x0, y0 = (p1.x, p1.y)
        x1, y1 = (p2.x, p2.y)

        distance = hypot(x1 - x0, y1 - y0)
        steps = int(max(distance, 10)) + 5
        max_offset = 120
        mid_x, mid_y = (x0 + x1) / 2, (y0 + y1) / 2

        dx, dy = x1 - x0, y1 - y0
        length = hypot(dx, dy)

        perp_x = -dy / length
        perp_y = dx / length

        offset = uniform(-max_offset, max_offset)
        ctrl_x = mid_x + perp_x * offset
        ctrl_y = mid_y + perp_y * offset

        path = []

        for i in range(steps + 1):
            t = i / steps
            x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * ctrl_x + t ** 2 * x1
            y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * ctrl_y + t ** 2 * y1

            x += uniform(-0.5, 0.5)
            y += uniform(-0.5, 0.5)

            pos = (round(x), round(y))
            if not path or pos != path[-1]:
                path.append(pos)

        return path

    def random_delay(self) -> int:
        if self.first:
            self.first = False
            return int(time() * 1000)
        # overwhelmingly 1
        return randint(2, 5) if randint(1, 5) % 2 == 0 else 1

    def generate_mouse_movement_image(self, solution: dict):
        self._generate_points_image(solution)

        for (i, point) in enumerate(self.points):
            if i == 0:
                continue

            mms = MouseMovement.connect_points(self.points[i - 1], point)
            for mm in mms:
                if self.mm_count > 150:
                    self.mm_count += 1
                    continue
                self.mm_count += 1
                self.mm.append(f"|mm|{mm[0]},{mm[1]}|{self.random_delay()}")

            self.mm.append(
                f"{point.button_id}|md|{point.x},{point.y}|{randint(80, 300)}|{point.rel_x},{point.rel_y}")
            self.mm.append(
                f"{point.button_id}|cl|{point.x},{point.y}|{self.random_delay()}|{point.rel_x},{point.rel_y}")

            self.cl_count += 1

            if self.mm_count <= 150 and point.button_id != "vb":
                self.mm.append(
                    f"{point.button_id}|mu|{point.x},{point.y}|{randint(100, 300)}|{point.rel_x},{point.rel_y}")
                self.mm_count += 1
                self.mu_count += 1

        self.mm.pop()  # last click doesn't count somehow

        return {
            "ec": {
                "mm": self.mm_count - self.mu_count,
                "md": self.cl_count + 1,
                "mu": self.cl_count + 1,
                "cl": self.cl_count
            },
            "el": self.mm.copy()
        }

    def generate_mouse_movement_slide(self, pos):
        self._generate_points_slide()
        for (i, point) in enumerate(self.points):
            if i == 0:
                continue

            mms = MouseMovement.connect_points(self.points[i - 1], point)
            for mm in mms:
                if self.mm_count > 150:
                    break
                self.mm_count += 1
                self.mm.append(f"|mm|{mm[0]},{mm[1]}|{self.random_delay()}|1")

        th = MouseMovement.connect_points(
            Point(43 + randrange(-2, 2), 16 + randrange(-2, 2)),
            Point(29 + randrange(-2, 2), 18 + randrange(-2, 2)))

        if len(th) > 30:
            th = th[:30]

        th_mm = []
        for mm in th:
            th_mm.append(f"mm|{mm[0]},{mm[1]}")

        return {
            "ec": {
                "mm": randint(700, 800),
                "md": 1,
                "mu": 1
            },
            "el": self.mm.copy(),
            "th": {
                "el": th_mm.copy(),  # this can be empty btw
                "si": {
                    "w": 44,
                    "h": 44
                }
            }
        }
