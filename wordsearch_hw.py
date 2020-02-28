#
# Github link to game I made using this
# https://github.com/AlexFradle/wordsearch
#


def get_name(): return "198520|Alex_Goodall"


def print_puzzle(Puzzle): print("\n".join([" ".join(i) for i in Puzzle]))


def load_words_to_find(file_name): return [i.replace("\n", "") for i in open(file_name).readlines()]


def find_horizontal(Puzzle, Words, ReplaceWith, Found):
    Outpuz = [i for i in Puzzle]
    for r_pos, row in enumerate(Puzzle):
        for word in Words:
            if row.find(word) > -1:
                Found.append(word)
                new_row = "".join([ReplaceWith if row.find(word) <= pos < len(word) + row.find(word) else letter for pos, letter in enumerate(row)])
                Outpuz[r_pos] = [new_row[l_pos] if let != ReplaceWith else let for l_pos, let in enumerate(Outpuz[r_pos])]
            elif "".join(list(reversed(row))).find(word) > -1:
                Found.append(word)
                rev_row = "".join(list(reversed(row)))
                new_row = "".join(list(reversed([ReplaceWith if rev_row.find(word) <= pos < len(word) + rev_row.find(word) else letter for pos, letter in enumerate(rev_row)])))
                Outpuz[r_pos] = [new_row[l_pos] if let != ReplaceWith else let for l_pos, let in enumerate(Outpuz[r_pos])]
    return Outpuz, Found


def rotate_puzzle(Puzzle): return ["".join(row) for row in list(zip(*[list(i) for i in Puzzle]))]


def find_vertical(Puzzle, Words, Found): return tuple([rotate_puzzle(i) if p == 0 else i for p, i in enumerate(find_horizontal(rotate_puzzle(Puzzle), Words, "|", Found))])


def find_diagonal(Puzzle, Words, Found):
    def make_vert(Puzzle, dir_):
        for pos in range(len(Puzzle) - 1, -1, -1):
            for i in range(len(Puzzle) - pos - 1):
                Puzzle[pos].insert(0 if dir_ == 1 else len(Puzzle), "/")
            for i in range(pos):
                Puzzle[pos].insert(len(Puzzle[pos]) if dir_ == 1 else 0, "/")
        return Puzzle
    Puzzle, Found = find_horizontal(rotate_puzzle(["".join(i) for i in make_vert([list(i) for i in Puzzle], 1)]), Words, "+", Found)
    Puzzle = [row.replace("/", "") for row in rotate_puzzle(Puzzle)]
    Puzzle, Found = find_horizontal(rotate_puzzle(["".join(i) for i in make_vert([list(i) for i in Puzzle], 2)]), Words, "+", Found)
    return [row.replace("/", "") for row in rotate_puzzle(Puzzle)], Found


def show_only_words(Original, Puzzle):
    Original, Puzzle = [list(i) for i in Original], [list(i) for i in Puzzle]
    return ["".join(["*" if Puzzle[r_pos][l_pos] not in [".", "|", "+"] else Original[r_pos][l_pos] for l_pos in range(len(Original[r_pos]))]) for r_pos in range(len(Original))]


def Missing_Words(Words, Found): return [i for i in Words if i not in Found]


def search_for_words(Puzzle, Words):
    Found = []
    Puzzle, Found = find_horizontal(Puzzle, Words, ".", Found)
    Puzzle, Found = find_vertical(Puzzle, Words, Found)
    Puzzle, Found = find_diagonal(Puzzle, Words, Found)
    return Puzzle, Missing_Words(Words, Found)


if __name__ == '__main__':
    Puzzle = ["FUNCTIONRRIRAI",
              "RAIOONFRCCPWON",
              "PTCSNOBEUITOLO",
              "BNCACIANTOSLIH",
              "RBYOLILYNREFBT",
              "HYYNOGESTIBRIY",
              "AATTSIONCMCENP",
              "UORTENRRCBFVAU",
              "CEBEECVWIERORI",
              "PROCESSORTOPYF",
              "OHCOMPUTERHSOS",
              "YCYPRESREOSMRW",
              "OATHBRMVTHHCTR",
              "PGORWOOUIPSCHP"]

    Words = load_words_to_find("words.txt")
    answer, missing = search_for_words(Puzzle, Words)
    only_words = show_only_words(Puzzle, answer)
    print_puzzle(only_words)
    print("Missing Words:", missing)
