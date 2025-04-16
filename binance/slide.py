#https://github.com/glizzykingdreko/Datadome-GeeTest-Captcha-Solver/blob/main/solver.py
"""
MIT LICENSE

Big thanks to glizzykingdreko for making this amazing solver

i modified it
"""
import numpy as np
import requests, cv2


class SlideSolver:
    def __init__(self, url):
        self.url = url

    def _split_piece(self):
        res = requests.get(self.url).content
        puzzle_piece_width = 60

        image = cv2.imdecode(np.frombuffer(res, np.uint8), cv2.IMREAD_ANYCOLOR)

        height, width = image.shape[:2]

        self.puzzle_piece = image[0:height, 0:puzzle_piece_width]

        self.background = image[0:height, puzzle_piece_width:width]

    def solve(self):
        self._split_piece()

        edge_puzzle_piece = cv2.Canny(self.puzzle_piece, 100, 200)
        edge_background = cv2.Canny(self.background, 100, 200)

        edge_puzzle_piece_rgb = cv2.cvtColor(edge_puzzle_piece, cv2.COLOR_GRAY2RGB)
        edge_background_rgb = cv2.cvtColor(edge_background, cv2.COLOR_GRAY2RGB)

        res = cv2.matchTemplate(edge_background_rgb, edge_puzzle_piece_rgb, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        h, w = edge_puzzle_piece.shape[:2]

        center_x = top_left[0] + w // 2

        cv2.line(self.background, (center_x, 0), (center_x, edge_background_rgb.shape[0]), (0, 255, 0), 2)
        #cv2.imwrite('output.png', self.background)

        return center_x  - 31


if __name__ == '__main__':
    result = SlideSolver("https://bin.bnbstatic.com/image/antibot/SLIDE/img/20250416/11/d4867651424d4c2994d65043a82b85d7.png").solve()
    print(result)