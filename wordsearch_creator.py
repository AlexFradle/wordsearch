from random import randint, choice
from string import ascii_uppercase


class Creator:
    def __init__(self, w: int, h: int, words: list=None, word_name: str="words.txt", puz_name: str="puz.txt", out_to_file: bool=False):
        # Checks for duplicate words
        assert (not any([True if words.count(i) > 1 else False for i in set(words)])), "Same word multiple times"

        # Checks whether files are acceptable
        assert (word_name.find(".") >= 1 and word_name[word_name.find(".") + 1:] == "txt"), "File not txt or incorrect"
        assert (puz_name.find(".") >= 1 and puz_name[puz_name.find(".") + 1:] == "txt"), "File not txt or incorrect"

        # Creates wordsearch grid
        self.__grid = [["*" for _ in range(w)] for _ in range(h)]
        self.__words_solved = {}

        # Gets words from file if not provided
        if words is None:
            with open(word_name) as f:
                words = [i for i in f.readlines()]

        # Loops through words adding them to grid
        for word in words:
            self.__add_word(word)

        # Adds random letters to scramble puzzle
        self.__scramble()

        # Outputs puzzle to file if needed
        if out_to_file:
            with open(puz_name, "w") as f:
                f.writelines(self.grid)

    @property
    def grid(self):
        return "\n".join([" ".join(i) for i in self.__grid])

    @property
    def words_solved(self):
        return self.__words_solved

    def __add_word(self, word: str) -> None:
        """
        Adds word to wordsearch
        :param word: Word to add
        :return: None
        """
        assert (len(word) < len(self.__grid[0])), "Word too long"
        assert (type(word) != int), "str expected, got int"
        word = word.upper()

        # Directions for the words to be incremented by
        x_changes = [0, 1, 1, 1, 0, -1, -1, -1]
        y_changes = [-1, -1, 0, 1, 1, 1, 0, -1]

        # Continuously loops until word can be placed
        while True:
            count = 0
            start_pos = [randint(0, len(self.__grid[0]) - 1), randint(0, len(self.__grid) - 1)]
            cur_pos = start_pos
            dir_ = randint(0, 7)
            for i in range(len(word)):
                # Checks if position is possible
                if (0 <= cur_pos[0] + x_changes[dir_] <= len(self.__grid[0]) and 0 <= cur_pos[1] + y_changes[dir_] <= len(self.__grid)) and (self.__grid[cur_pos[1]][cur_pos[0]] == "*"):
                    # Increments for next position
                    cur_pos = [cur_pos[0] + x_changes[dir_], cur_pos[1] + y_changes[dir_]]
                    count += 1

            # Checks if all the word was able to be placed, if not it loops again
            if count == len(word):
                break

        # Adds word to solved dict
        self.__words_solved[word] = {"start_pos": start_pos, "x_change": x_changes[dir_], "y_change": y_changes[dir_]}

        # Places letters in the grid
        for i in word:
            self.__grid[start_pos[1]][start_pos[0]] = i
            start_pos = [start_pos[0] + x_changes[dir_], start_pos[1] + y_changes[dir_]]

    def __scramble(self) -> None:
        """
        Adds random letters to scramble puzzle
        :return: None
        """
        for r_pos, row in enumerate(self.__grid):
            for s_pos, space in enumerate(row):
                if space == "*":
                    self.__grid[r_pos][s_pos] = choice(ascii_uppercase)


if __name__ == '__main__':
    c = Creator(20, 20, ["alex", "python"], out_to_file=True)

