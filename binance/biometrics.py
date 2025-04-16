from random import randint, uniform, randrange
from math import hypot

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
    def __init__(self, x, y, button_id, rel_x, rel_y):
        self.x = x
        self.y = y
        self.button_id = button_id
        self.rel_x = rel_x
        self.rel_y = rel_y

    def __str__(self):
        return f"({self.x}, {self.y}, {self.button_id}, {self.rel_x}, {self.rel_y})"


class MouseMovement:
    def __init__(self, solution: dict):
        self.sol = solution  # {0: [...], 1: [...]}
        self.points = []
        self.mm = []

        self.mm_count = 0
        self.cl_count = 0
        self.mu_count = 0

    def generate_points(self):
        def gen(page: int):
            for point in self.sol[page]:
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

    @staticmethod
    def random_delay() -> int:
        # overwhelmingly 1
        return randint(2, 5) if randint(1, 5) % 2 == 0 else 1

    def generate_mouse_movement_image(self):
        if len(self.points) == 0:
            self.generate_points()
        for (i, point) in enumerate(self.points):
            if i == 0:
                continue

            mms = MouseMovement.connect_points(self.points[i - 1], point)
            for mm in mms:
                if self.mm_count > 150:
                    self.mm_count += 1
                    continue
                self.mm_count += 1
                self.mm.append(f"|mm|{mm[0]},{mm[1]}|{MouseMovement.random_delay()}")

            self.mm.append(
                f"{point.button_id}|md|{point.x},{point.y}|{randint(80, 300)}|{point.rel_x},{point.rel_y}")
            self.mm.append(
                f"{point.button_id}|cl|{point.x},{point.y}|{MouseMovement.random_delay()}|{point.rel_x},{point.rel_y}")

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


if __name__ == "__main__":
    m = MouseMovement({0: [0, 2, 5, 7], 1: [1]})
    m.generate_points()
    print(m.generate_mouse_movement())
