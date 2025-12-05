from puzzleshelf import PuzzleShelf

shelf = PuzzleShelf('test')


@shelf.parser(1)
def parse():
    return 1


@shelf.solver(1)
def solve(num: int):
    return 2 * num


if __name__ == '__main__':
    print(shelf.run(1))
