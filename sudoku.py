import random


def group(values, n: int):
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    s = -1
    list2 = list()
    for i in range(n):
        b = []
        for k in range(len(values) // n):
            s += 1
            b.append(values[s])
        list2.append(b)
    return (list2)


def read_sudoku(filename: str):
    """ Прочитать Судоку из указанного файла """
    with open(filename) as f:
        content = f.read()
    digits = [c for c in content if c in '123456789.']
    grid = group(digits, 9)
    return grid


def get_row(grid: list, pos: tuple):
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row, col = pos
    a = grid[row]
    return (a)


def get_col(grid: list, pos: tuple):
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    row, col = pos
    b = []
    for i in range(len(grid)):
        k = grid[i]
        b.append(k[col])
    return (b)


def get_block(grid: list, pos: tuple):
    """ Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row, col = pos
    br = 3 * (row // 3)
    bc = 3 * (col // 3)
    return [grid[br + r][bc + c] for r in range(3) for c in range(3)]


def find_empty_positions(grid: list):
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == '.':
                return (row, col)
    return None


def find_possible_values(grid: list, pos: tuple):
    """ Вернуть множество всех возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> set(values) == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> set(values) == {'2', '5', '9'}
    True
    """
    a = get_row(grid, pos)
    b = get_col(grid, pos)
    c = get_block(grid, pos)
    variants = []
    f = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in f:
        s = 0
        for l in range(9):
            if (i != a[l]) and (i != b[l]) and (i != c[l]):
                s += 1
        if s == 9:
            variants.append(i)
    return (variants)


def solve(grid: list):
    """ Решение пазла, заданного в grid
    Как решать Судоку?
    1. Найти свободную позицию
    2. Найти все возможные значения, которые могут находиться на этой позиции
    3. Для каждого возможного значения:
        3.1. Поместить это значение на эту позицию
        3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)
    if not pos:
        return grid
    row, col = pos
    for value in find_possible_values(grid, pos):
        grid[row][col] = value
        solution = solve(grid)
        if solution:
            return solution
    grid[row][col] = '.'
    return None


def check_solution(solution) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    for i in range(len(solution)):
        i_values = set(get_row(solution, (i, 0)))
        if i_values != set('123456789'):
            return False

    for i in range(len(solution)):
        i_values = set(get_col(solution, (0, i)))
        if i_values != set('123456789'):
            return False

    for i in (0, 3, 6):
        for l in (0, 3, 6):
            blk_values = set(get_block(solution, (i, l)))
            if blk_values != set('123456789'):
                return False

    return True


def generate_sudoku(N: int):
    """ Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid = solve([['.'] * 9 for _ in range(9)])
    N = 81 - min(81, max(0, N))
    while N:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid[row][col] != '.':
            grid[row][col] = '.'
            N -= 1
    return grid
