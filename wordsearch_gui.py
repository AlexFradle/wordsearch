from wordsearch_solver import Solver
from wordsearch_creator import Creator
import pygame
from win32api import GetSystemMetrics
import pyautogui
from itertools import chain, cycle
pygame.init()


class Space(pygame.Rect):
    def __init__(self, char, l, r, w, h):
        super().__init__(l, r, w, h)
        self.char = char
        self.colour = (0, 0, 0)


# Get width and height of monitor
width, height = GetSystemMetrics(0), GetSystemMetrics(1)

# Create display, clock and fonts
display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier", 30, bold=True)
menu_font = pygame.font.SysFont("Courier", 50, bold=True)

# Creating key
key_main = font.render("Key:", True, (255, 255, 255))
controls = [
    font.render(txt, True, (255, 255, 255)) for txt in [
        "L_MOUSE - select space", "F - show ans", "C - auto complete", "ESC - quit"
    ]
]
key_box = pygame.Rect(0, 850, 400, 230)

# Creating game end menu
menu_outer = pygame.Rect(0, 0, 800, 400)
menu_outer.center = (width // 2, height // 2)
menu_inner = pygame.Rect(0, 0, 700, 300)
menu_inner.center = (width // 2, height // 2)
menu_button = pygame.Rect(0, 0, 500, 100)
menu_button.center = (width // 2, (height // 2) + 75)

menu_text = menu_font.render("You win!", True, (0, 0, 0))
menu_text_pos = pygame.Rect(0, 0, 0, 0)
menu_text_pos.center = ((width // 2) - 120, (height // 2) - 70)
menu_button_text = font.render("Restart", True, (0, 0, 0))
menu_button_text_pos = pygame.Rect(0, 0, 0, 0)
menu_button_text_pos.center = ((width // 2) - 55, (height // 2) + 60)

# Setting click pause to be lower
pyautogui.PAUSE = 0.02


def main():
    # Initialising misc variables
    border_width = 8
    clicked_chars = []
    solved_word_spaces = []
    found_words = []
    show_ans = False
    running = True
    finished = False
    auto = False

    # Create wordsearch to be solved and get the correct coords
    creator = Creator(20, 20, word_name="words.txt", puz_name="puz.txt", out_to_file=True)
    word_pos = creator.words_solved

    # Solve wordsearch
    solver = Solver("words.txt", puz_file="puz.txt")
    solver.out_to_file()

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

    # Auto complete places
    auto_spaces = list(
        chain.from_iterable([[space for s_pos, space in enumerate(row) if space.char == solved_chars[r_pos][s_pos]] for r_pos, row in enumerate(spaces)])
    )
    auto_spaces_iter = cycle(auto_spaces)

    # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC ends game
                    return True

                elif event.key == pygame.K_f:
                    # Shows answers if F is pressed
                    if not finished:
                        show_ans = not show_ans
                        clicked_chars = []
                        for row in spaces:
                            for space in row:
                                if space not in solved_word_spaces:
                                    space.colour = (0, 0, 0)
                                else:
                                    space.colour = (0, 255, 0)
                elif event.key == pygame.K_c:
                    auto = not auto

            if event.type == pygame.MOUSEBUTTONUP:
                mx, my = pygame.mouse.get_pos()

                # Append clicked spaces and change space colour
                if not show_ans and not finished:
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
                if finished:
                    if menu_button.collidepoint(mx, my):
                        running = False

        display.fill((255, 255, 255))

        # Auto complete
        if auto:
            space = next(auto_spaces_iter)
            pyautogui.click(space.x + 2, space.y + 2)
            if space == auto_spaces[len(auto_spaces) - 1]:
                auto = False

        # |                                      |
        # | Anything being drawn should be below |
        # V                                      V

        # Found word logic
        if not show_ans and not finished:
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

        # Draw solved grid spaces
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

        # Draw word list
        display.blit(font.render("           Words:", True, (0, 0, 0)), pygame.Rect(0, 0, 200, 50))
        for pos, word in enumerate(solver.words):
            if word in found_words:
                font_colour = (0, 255, 0)
            else:
                font_colour = (0, 0, 0)
            display.blit(font.render(word, True, font_colour), pygame.Rect(0, 50 * (pos + 1), 0, 0))

        # Draw key
        pygame.draw.rect(display, (255, 0, 0), key_box)
        display.blit(key_main, pygame.Rect(0, 850, 0, 0))
        for k_pos, key in enumerate(controls):
            display.blit(key, pygame.Rect(0, 850 + (50 * (k_pos + 1)), 0, 0))

        # End of game
        if len(found_words) == len(solver.words):
            finished = True
            pygame.draw.rect(display, (0, 255, 0), pygame.Rect(menu_outer))
            pygame.draw.rect(display, (255, 255, 255), pygame.Rect(menu_inner))
            pygame.draw.rect(display, (0, 0, 0), pygame.Rect(menu_button), border_width)
            display.blit(menu_text, menu_text_pos)
            display.blit(menu_button_text, menu_button_text_pos)

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    while True:
        quit_ = main()
        if quit_:
            break
    pygame.quit()
