from io import TextIOWrapper

from puzzleshelf import PuzzleShelf

shelf = PuzzleShelf('test')


@shelf.parser(1)
def parse(file: TextIOWrapper):
    return [int(x) for x in file.readlines()]


@shelf.solver(1)
def solve(nums: list[int]):
    return sum(nums)


if __name__ == '__main__':
    print(shelf.run(1))
