from puzzleshelf import PuzzleShelf

shelf = PuzzleShelf('test')


@shelf.parser(1)
def parse():
    return 1, 2


@shelf.solver(1)
def solve(a: int, b: int):
    return a + b


if __name__ == '__main__':
    print(shelf.run(1))
