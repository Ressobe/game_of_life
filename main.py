from random import randint
import pygame
import math


class GameInfo():
    TITLE = "Game of Life"
    FPS = 10
    WIDTH = 1200
    HEIGHT = 800

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (169, 169, 169)
    BACKGROUND = WHITE


    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.x = math.floor(self.WIDTH / self.cols) 
        self.y = math.floor(self.HEIGHT / self.rows)

        self.surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def create_board(self) -> None:
        self.board = []
        for _ in range(0, self.cols):
            row = []
            for _ in range(0, self.rows):
                row.append(randint(0, 1))
            self.board.append(row)


    def count_neighbourhood(self, x: int, y: int) -> int:
        amount = 0
        if x == 0:
            middle = self.board[x][y - 1:y+2]
            bottom = self.board[x+1][y - 1:y+2]
            amount += sum(middle) + sum(bottom)

        if x == len(self.board) - 1 :
            top = self.board[x - 1][y - 1:y+2]
            middle = self.board[x][y - 1:y+2]
            amount += sum(middle) + sum(top)

        else:
            top = self.board[x - 1][y - 1:y+2]
            middle = self.board[x][y - 1:y+2]
            bottom = self.board[x+1][y - 1:y+2]
            amount = sum(top) + sum(middle) + sum(bottom)

        return  amount - self.board[x][y]


    def update_board(self) -> None:
        copy_board = self.board.copy()
        for i in range(0, len(self.board)):
            for j in range(1, len(self.board[i]) - 1):
                state = self.board[i][j]
                amount = self.count_neighbourhood(i, j)

                if state == 0 and amount == 3:
                    state = 1
                elif state == 1 and (amount > 3 or amount < 2):
                    state = 0

                copy_board[i][j] = state
        self.board = copy_board.copy()


    def render_board(self) -> None:
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                rect = pygame.Rect(col * self.x, row * self.y, self.x, self.y)
                if self.board[row][col]:
                    pygame.draw.rect(self.surface, self.BLACK, rect)
                else:
                    pygame.draw.rect(self.surface, self.GREY, rect, 1)


pygame.init()

COLS = 40
ROWS = 40

game = GameInfo(COLS, ROWS)
game.create_board()

pygame.display.set_caption(game.TITLE)


def draw_window():
    game.surface.fill(game.BACKGROUND)
    game.update_board()
    game.render_board()
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(game.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()

    pygame.quit()


if __name__ == '__main__':
    main()
