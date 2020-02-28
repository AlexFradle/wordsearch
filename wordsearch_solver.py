class Solver:
    def __init__(self, word_file, puzzle=None, puz_file=None):
        # Checks whether puzzle can be assigned
        assert (
                not(puzzle is None and puz_file is None) or (puzzle is not None and puz_file is not None)
        ), "Not able to get puzzle or provided both puzzle and file"

        # Assigns attributes
        self.words = sorted(self.load_words_to_find(word_file), key=len, reverse=True)
        self.puzzle = puzzle if puz_file is None else self.load_puzzle(puz_file)
        self.found = []
        self.solved_puzzle = self.search_for_words()
        self.missing = self.missing_words()

    def __str__(self):
        rows = list(zip(
                [" ".join(i) for i in self.puzzle],
                [" ".join(j) for j in self.solved_puzzle],
                [" ".join(k) for k in self.show_only_words()]
        ))
        return "\n".join(
            [f" {'-'*7}> ".join(row) if pos + 1 == (len(rows) // 2) else f"{' '*10}".join(row) for pos, row in enumerate(rows)]
        ) + f"\n\nMissing Words {self.missing}"

    @staticmethod
    def load_words_to_find(file_name: str) -> list:
        """
        Loads words to find in the word search from a txt file
        :param file_name: File name of txt file
        :return: List of words
        """
        assert (file_name.find(".") >= 1 and file_name[file_name.find(".") + 1:] == "txt"), "File not txt or incorrect"
        with open(file_name) as f:
            word_list = [i.replace("\n", "") for i in f.readlines()]
        return word_list

    @staticmethod
    def load_puzzle(file_name: str) -> list:
        """
        Loads puzzle to use from txt file
        :param file_name: File name of the txt file
        :return: Rows of puzzle
        """
        assert (file_name.find(".") >= 1 and file_name[file_name.find(".") + 1:] == "txt"), "File not txt or incorrect"
        with open(file_name) as f:
            puz = [i.replace("\n", "").replace(" ", "") for i in f.readlines()]
        return puz

    @staticmethod
    def rotate_puzzle(puzzle: list) -> list:
        """
        Rotates puzzle 90 degrees anti-clockwise then 90 degrees clockwise
        :param puzzle: Puzzle to be rotated
        :return: Rotated puzzle
        """
        rotate_puz = ["".join(row) for row in list(zip(*[list(i) for i in puzzle][::1]))]
        return rotate_puz

    def out_to_file(self, file_name="out_puz.txt") -> None:
        """
        Writes string representation of puzzle out to file
        :param file_name: File name of the txt file
        :return: None
        """
        assert (file_name.find(".") >= 1 and file_name[file_name.find(".") + 1:] == "txt"), "File not txt or incorrect"
        with open(file_name, "w") as out_file:
            out_file.writelines(repr(self))

    def show_only_words(self) -> list:
        """
        Outputs puzzle with only found words showing
        :return: Converted puzzle
        """
        # Load solved and unsolved puzzles to compare
        unsolved = [list(i) for i in self.puzzle]
        puzzle = [list(i) for i in self.solved_puzzle]

        # Loop through unsolved to replace where the not used letters are
        for r_pos in range(len(unsolved)):
            for l_pos in range(len(unsolved[r_pos])):
                if puzzle[r_pos][l_pos] not in [".", "|", "+"]:
                    unsolved[r_pos][l_pos] = "*"

        # Convert 2D list to 1D
        unsolved = ["".join(i) for i in unsolved]
        return unsolved

    def search_for_words(self) -> list:
        """
        Main function to solve puzzle
        :return: Solved puzzle
        """
        puzzle = self.puzzle
        puzzle = self.find_horizontal(puzzle, ".")
        puzzle = self.find_vertical(puzzle)
        puzzle = self.find_diagonal(puzzle)
        return puzzle

    def missing_words(self) -> list:
        """
        Finds out what words haven't been found
        :return: Missing words
        """
        return [i for i in self.words if i not in self.found]

    def find_horizontal(self, puzzle: list, replace_with: str) -> list:
        """
        Finds words horizontally
        :param puzzle: Puzzle to be searched
        :param replace_with: Character to replace the found word with
        :return: Puzzle with replaced characters where the horizontal words where
        """
        # Load copy of puzzle
        outpuz = [i for i in puzzle]

        # Loop through puzzle getting row and pos to know where to replace in copy
        for r_pos, row in enumerate(puzzle):
            # Check all words
            for word in self.words:
                # Check if word is left to right if so append to found and replace in copy
                if row.find(word) > -1:
                    self.found.append(word)
                    new_row = "".join([replace_with if row.find(word) <= pos < len(word) + row.find(word) else letter for pos, letter in enumerate(row)])
                    outpuz[r_pos] = [new_row[l_pos] if let != replace_with else let for l_pos, let in enumerate(outpuz[r_pos])]

                # Check if words is reversed if so append to found and replace in copy
                elif "".join(list(reversed(row))).find(word) > -1:
                    self.found.append(word)
                    rev_row = "".join(list(reversed(row)))
                    new_row = "".join(list(reversed([replace_with if rev_row.find(word) <= pos < len(word) + rev_row.find(word) else letter for pos, letter in enumerate(rev_row)])))
                    outpuz[r_pos] = [new_row[l_pos] if let != replace_with else let for l_pos, let in enumerate(outpuz[r_pos])]
        return outpuz

    def find_vertical(self, puzzle: list) -> list:
        """
        Finds words vertically by rotating and then searching horizontally
        :param puzzle: Puzzle to be searched
        :return: Puzzle with replaced characters where the vertical words where
        """
        # Rotate puzzle to make vertical horizontal
        rot_puz = self.rotate_puzzle(puzzle)

        # Find words horizontally
        outpuz = self.find_horizontal(rot_puz, "|")

        # Rotate puzzle 90 degrees to get it back to normal orientation
        outpuz = self.rotate_puzzle(outpuz)
        return outpuz

    def find_diagonal(self, puzzle: list) -> list:
        """
        Finds words diagonally by skewing puzzle
        :param puzzle: Puzzle to be searched
        :return: Puzzle with replaced characters where the diagonal words where
        """
        # Makes puzzle 2D list
        puzzle = [list(i) for i in puzzle]

        # Loops through puzzle backwards to skew \ shape to | shape
        for pos in range(len(puzzle) - 1, -1, -1):
            for i in range(len(puzzle) - pos - 1):
                puzzle[pos].insert(0, "/")
            for i in range(pos):
                puzzle[pos].insert(len(puzzle[pos]), "/")

        # Make skewed puzzle 1D list
        puzzle = ["".join(i) for i in puzzle]

        # Rotate to change from vertical to horizontal
        puzzle = self.rotate_puzzle(puzzle)
        puzzle = self.find_horizontal(puzzle, "+")

        # Make puzzle normal orientation
        puzzle = self.rotate_puzzle(puzzle)

        # Un-skew puzzle
        puzzle = [row.replace("/", "") for row in puzzle]

        # |                             |
        # | Same as above just reversed |
        # V                             V

        # Make puzzle 2D list
        puzzle = [list(i) for i in puzzle]

        # Loop through puzzle backwards to skew / shape to | shape
        for pos in range(len(puzzle) - 1, -1, -1):
            for i in range(len(puzzle) - pos - 1):
                puzzle[pos].insert(len(puzzle), "/")
            for i in range(pos):
                puzzle[pos].insert(0, "/")

        # Make skewed puzzle 1D list
        puzzle = ["".join(i) for i in puzzle]

        # Rotate to make vertical horizontal
        puzzle = self.rotate_puzzle(puzzle)
        puzzle = self.find_horizontal(puzzle, "+")

        # Make puzzle normal orientation
        puzzle = self.rotate_puzzle(puzzle)

        # Un-skew puzzle
        puzzle = [row.replace("/", "") for row in puzzle]

        return puzzle


if __name__ == '__main__':
    solv = Solver("words.txt", puz_file="puz.txt")
    print(solv)
    solv.out_to_file()
