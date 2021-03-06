import re
import numpy as np
import itertools
import functools
import sys
import os

def readTest():
    test_content = sys.stdin.readlines()
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


def V(x):
    i = x[0]
    j = x[1]
    return 'V{}_{}'.format(i,j)


def printPredLabel(nrow, ncol, rdesc, cdesc):
    ar,ac = 'ar', 'ac'
    if nrow == ncol:
        ar = ac = 'a'
    variables = [V(x) for x in itertools.product(range(nrow), range(ncol))]
    print('solve(['+', '.join(variables)+']):-')
    rows = []
    for i in range(nrow):
        variables = [V(x) for x in itertools.product([i], range(ncol))]
        rows.append('\t'+ar+'i'.join(map(str,rdesc[i]))+'(['+', '.join(variables)+']),')

    cols = []
    for i in range(ncol):
        variables = [V(x) for x in itertools.product(range(nrow), [i])]
        cols.append('\t'+ac+'i'.join(map(str,cdesc[i]))+'(['+', '.join(variables)+']),')

    toprint = functools.reduce(lambda x,y:x+y, map(lambda x,y: [x,y], rows, cols))
    list(map(print, toprint))
    print('\t!.')


def genDictionary(nrow, ncol, rdesc, cdesc):
    d = {}
    ar, ac = 'r', 'c'
    if nrow == ncol:
        ar = ac = 'e'
    for i in range(nrow):
        k = (tuple(rdesc[i]), ncol, ar)
        if k not in d:
            d[k] = genCorrectLines(rdesc[i], ncol)

    for i in range(ncol):
        k = (tuple(cdesc[i]), nrow, ac)
        if k not in d:
            d[k] = genCorrectLines(cdesc[i], nrow)

    return d


def printDict(d):
    for k in d:
        l = d[k]
        for sl in l:
            a = ''
            if k[2] == 'r':
                a = 'ar'
            elif k[2] == 'c':
                a = 'ac'
            elif k[2] == 'e':
                a = 'a'
            print(a+'i'.join(map(str,k[0]))+'(['+', '.join(map(str,sl))+']).')


def printFooter():
    print('\n\n:- solve(X), write(X), halt(0).')


def fixListSize(raw_list, num_row):
    return list(map(list, np.array_split(raw_list,num_row)))

def printTab(tab, end=''):
    for i in range(len(tab)):
        print( ''.join(map(lambda x: '#' if x else '.', tab[i])) )
    print(end=end)


################
## START HERE ##
################

s = sys.stdout
sys.stdout = open('.solver.pl', 'w')

test_data = readTest()

num_rows = test_data[0][0]
num_columns = test_data[0][1]

rows_description = test_data[1:num_rows+1]
columns_description = test_data[num_rows+1:]

printPredLabel(num_rows, num_columns, rows_description, columns_description)
print()

printDict(genDictionary(num_rows, num_columns, rows_description, columns_description))

printFooter()

sys.stdout.close()
sys.stdout = s

os.system('prolog .solver.pl > .out && rm -f .solver.pl')

with open(".out") as f:
    raw_list = eval(f.readline())

printTab(fixListSize(raw_list, num_rows))
os.system('rm -f .out')
