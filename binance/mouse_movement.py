from random import randint

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

    def generate_points(self):
        def gen(page: int):
            for point in self.sol[page]:
                tile = TILES[point]
                rand_x = randint(10, 100)
                rand_y = randint(10, 100)

                pos = tile["pos"]

                self.points.append(Point(pos[0] + rand_x, pos[1] + rand_y, tile["id"], rand_x, rand_y))

        gen(0)

        vb_tile = TILES["vb"]
        vb_rand_x = randint(2, vb_tile["size"][0])
        vb_rand_y = randint(2, vb_tile["size"][1])
        self.points.append(
            Point(vb_tile["pos"][0] + vb_rand_x, vb_tile["pos"][1] + vb_rand_y, "vb", vb_rand_x, vb_rand_y)
        )

        gen(1)


if __name__ == "__main__":
    m = MouseMovement({0: [0, 2, 4], 1: [1, 2, 6]})
    m.generate_points()
