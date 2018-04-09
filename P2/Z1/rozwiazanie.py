import re
import random
import numpy as np
import itertools

MAX_ERRORS = 1000
MAX_COST = 100

def printTab(tab, end=''):
    for i in range(len(tab)):
        print( ''.join(map(lambda x: '#' if x else '.', tab[i])) )
    print(end=end)

def readTest(filename):
    test_content = open(filename).readlines()
    out = []
    for line in test_content:
        out.append(re.findall(r'\d+', line))
    return list(map(lambda x : list(map(int, x)), out))


def genCorrectLines(description, length):
    const_len = sum(description) + len(description) - 1
    extra_zeros = length - const_len
    zeros_len = list(range(extra_zeros+1))

    correctZeros = [z for z in itertools.product(zeros_len, repeat=len(description)+1) if sum(z) == extra_zeros]

    desc_lists = []

    for d in description[0:-1]:
        ones = list(np.repeat([1], d))
        ones.append(0)
        desc_lists.append(ones)

    ones = list(np.repeat([1], description[-1]))
    desc_lists.append(ones)
    desc_lists.append([])

    result = []
    for t in correctZeros:
        t = list(map(lambda x : list(np.repeat([0],x)), t))
        t = list(zip(t, desc_lists))
        t = itertools.chain.from_iterable(t)
        t = list(itertools.chain.from_iterable(t))

        result.append(t)
    return result


def createBoard(test_data):
    rows = test_data[0][0]
    columns = test_data[0][1]
    return [[0 for x in range(columns)] for y in range(rows)]


def fillSureFields(test_data):
    return createBoard(test_data)


def opt_dist(line, description):
    line = np.array(line)
    gc = np.array(genCorrectLines(description, len(line)))
    return np.amin(np.abs(gc-line).sum(axis=1))


def is_correct(board, test_data):
    if getBrokenRows(board, test_data):
        return False

    if getBrokenColumns(board, test_data):
        return False

    return True


def incrementError(error_counter):
    error_counter += 1
    if error_counter > MAX_ERRORS:
        raise ValueError
    return error_counter


def getColumn(board, col_index):
    res = []
    for row in range(len(board)):
        res.append(board[row][col_index])
    return res


def getBrokenRows(board, test_data):
    num_rows = test_data[0][0]
    num_columns = test_data[0][1]

    rows_description = test_data[1:num_rows+1]
    columns_description = test_data[num_rows+1:]

    broken_rows = []

    for row_index in range(num_rows):
        if opt_dist(board[row_index], rows_description[row_index]) > 0:
            broken_rows.append(row_index)

    return broken_rows


def getBrokenColumns(board, test_data):
    num_rows = test_data[0][0]
    num_columns = test_data[0][1]

    rows_description = test_data[1:num_rows+1]
    columns_description = test_data[num_rows+1:]

    broken_cols = []

    for col_index in range(num_columns):
        if opt_dist(getColumn(board, col_index), columns_description[col_index]):
            broken_cols.append(col_index)

    return broken_cols


def inverse(val):
    return 0 if val else 1


def walkSat(board, board_mask, test_data):
    num_rows = test_data[0][0]
    num_columns = test_data[0][1]

    rows_description = test_data[1:num_rows+1]
    columns_description = test_data[num_rows+1:]

    error_counter = 0
    try:
        while not is_correct(board, test_data):
            printTab(board, '\n')
            if random.choice([0,1]):

                broken_rows = getBrokenRows(board, test_data)
                if broken_rows:
                    row_index = random.choice(broken_rows)
                    broken_rows.remove(row_index)

                    min_cost = MAX_COST
                    best_index = -1

                    for col_index in range(num_columns):
                        if board_mask[row_index][col_index] == 0:
                            column = getColumn(board, col_index)

                            board[row_index][col_index] = inverse(board[row_index][col_index])
                            row_cost = opt_dist(board[row_index], rows_description[row_index])
                            col_cost = opt_dist(column, columns_description[col_index])
                            board[row_index][col_index] = inverse(board[row_index][col_index])

                            sum_cost = row_cost + col_cost
                            if min_cost > sum_cost:
                                min_cost = sum_cost
                                best_index = col_index

                    board[row_index][best_index] = inverse(board[row_index][best_index])
            else:
                broken_columns = getBrokenColumns(board, test_data)

                if broken_columns:

                    col_index = random.choice(broken_columns)
                    broken_columns.remove(col_index)

                    min_cost = MAX_COST
                    best_index = -1

                    for row_index in range(num_rows):
                        if board_mask[row_index][col_index] == 0:
                            column = getColumn(board, col_index)

                            board[row_index][col_index] = inverse(board[row_index][col_index])
                            row_cost = opt_dist(board[row_index], rows_description[row_index])
                            col_cost = opt_dist(column, columns_description[col_index])
                            board[row_index][col_index] = inverse(board[row_index][col_index])

                            sum_cost = row_cost + col_cost
                            if min_cost > sum_cost:
                                min_cost = sum_cost
                                best_index = row_index

                    board[best_index][col_index] = inverse(board[best_index][col_index])
                    if opt_dist(getColumn(board, col_index), columns_description[col_index]) > 0:
                        broken_columns.append(col_index)

            error_counter = incrementError(error_counter)

    except ValueError:
        printTab(board, '\n')
        return walkSat(createBoard(test_data), board_mask, test_data)

    return board


###########
## START ##
###########
test_data = readTest('test')
board = createBoard(test_data)
board_mask = fillSureFields(test_data)


result_board = walkSat(board, board_mask, test_data)
printTab(result_board)
