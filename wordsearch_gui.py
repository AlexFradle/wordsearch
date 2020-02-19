from wordsearch_solver import Solver
from wordsearch_creator import Creator
import pygame
from win32api import GetSystemMetrics
pygame.init()


class Space(pygame.Rect):
    def __init__(self, char, l, r, w, h):
        super().__init__(l, r, w, h)
        self.char = char
        self.colour = (0, 0, 0)


# Get width and height of monitor
width, height = GetSystemMetrics(0), GetSystemMetrics(1)

# Create display and clock
display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Initialising misc variables
font = pygame.font.SysFont("Courier", 30, bold=True)
border_width = 8
clicked_chars = []
solved_word_spaces = []
found_words = []
show_ans = False
running = True

# Create wordsearch to be solved and get the correct coords
creator = Creator(20, 20, word_name="words.txt", puz_name="puz.txt", out_to_file=True)
word_pos = creator.words_solved

# Solve wordsearch
solver = Solver("words.txt", puz_file="puz.txt")

# Get characters to assign to spaces
chars = [list(i) for i in solver.puzzle]
solved_chars = [list(i) for i in solver.show_only_words()]

# Dimensions for grid
grid_size = len(solver.puzzle)
space_size = 980 // grid_size

# List of all spaces on the grid
spaces = [
    [Space(char, 860 + (space_size * c_pos), 50 + (space_size * r_pos), space_size, space_size) for c_pos, char in enumerate(j)] for r_pos, j in enumerate(chars)
]

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # ESC ends game
                running = False

            elif event.key == pygame.K_f:
                # Shows answers if F is pressed
                show_ans = not show_ans
                clicked_chars = []
                for row in spaces:
                    for space in row:
                        if space not in solved_word_spaces:
                            space.colour = (0, 0, 0)
                        else:
                            space.colour = (0, 255, 0)

        if event.type == pygame.MOUSEBUTTONUP:
            mx, my = pygame.mouse.get_pos()

            # Append clicked spaces and change space colour
            if not show_ans:
                for row in spaces:
                    for space in row:
                        if space.collidepoint(mx, my):
                            if space not in solved_word_spaces:
                                if space in clicked_chars:
                                    space.colour = (0, 0, 0)
                                    clicked_chars.remove(space)
                                else:
                                    space.colour = (255, 0, 0)
                                    clicked_chars.append(space)

    display.fill((255, 255, 255))

    # |                                      |
    # | Anything being drawn should be below |
    # V                                      V

    # Found word logic
    if not show_ans:
        for word in list(word_pos):
            solved_spaces = []
            for r_pos, row in enumerate(spaces):
                for s_pos, space in enumerate(row):
                    if [s_pos, r_pos] in word_pos[word] and space in clicked_chars:
                        solved_spaces.append(space)

            if len(solved_spaces) == len(word_pos[word]):
                for space in solved_spaces:
                    space.colour = (0, 255, 0)
                    solved_word_spaces.append(space)
                found_words.append(word)
                del word_pos[word]

    # Draw grid spaces
    if not show_ans:
        for row in spaces:
            for space in row:
                pygame.draw.rect(display, space.colour, space, border_width)
                display.blit(font.render(space.char, True, space.colour), space)
    else:
        for r_pos, row in enumerate(spaces):
            for c_pos, space in enumerate(row):
                if spaces[r_pos][c_pos].char == solved_chars[r_pos][c_pos]:
                    space.colour = (0, 0, 255)
                    pygame.draw.rect(display, space.colour, space, border_width)
                    display.blit(font.render(space.char, True, space.colour), space)
                else:
                    pygame.draw.rect(display, space.colour, space, border_width)
                    display.blit(font.render(space.char, True, space.colour), space)

    display.blit(font.render("           Words:", True, (0, 0, 0)), pygame.Rect(0, 0, 200, 50))
    for pos, word in enumerate(solver.words):
        if word in found_words:
            font_colour = (0, 255, 0)
        else:
            font_colour = (0, 0, 0)
        display.blit(font.render(word, True, font_colour), pygame.Rect(0, 50 * (pos + 1), 200, 50))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
