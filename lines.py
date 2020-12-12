from random import randint
import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [['.'] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 50

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for j in range(self.height):
            for i in range(self.width):
                pygame.draw.rect(screen, pygame.Color('white'), (
                    self.left + i * self.cell_size, self.top + self.cell_size * j, self.cell_size,
                    self.cell_size), 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def on_click(self, cell):
        pass

    def get_cell(self, pos):
        cell_x = (pos[0] - self.left) // self.cell_size
        cell_y = (pos[1] - self.top) // self.cell_size
        if (0 <= cell_x < self.width) and (0 <= cell_y < self.height):
            return (cell_x, cell_y)


class Lines(Board):
    def __init__(self, width, height):
        super().__init__(width, height)

    def render(self, screen):
        colors = {'r': 'red', 'b': 'blue'}
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] in colors:
                    color = colors[self.board[y][x]]
                else:
                    color = 'black'
                pygame.draw.circle(screen, color, (
                    self.left + x * self.cell_size + self.cell_size // 2,
                    self.top + self.cell_size * y + self.cell_size // 2), self.cell_size // 2)
        super().render(screen)

    def on_click(self, cell):
        x, y = cell
        if self.board[y][x] != 'b':
            self.board[y][x] = 'b'
        else:
            self.board[y][x] = 'r'

    def count_near_circles(self, x, y):
        count = 0
        delta = [(delta_x, delta_y) for delta_x in [-1, 0, 1] for delta_y in [-1, 0, 1] if
                 (delta_x != 0) or (delta_y != 0)]
        for dx, dy in delta:
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                if self.board[y + dy][x + dx] == 10:
                    count += 1
        return count


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Линеечки')
    size = 700, 700
    screen = pygame.display.set_mode(size)
    board = Lines(8, 8)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
    pygame.quit()
