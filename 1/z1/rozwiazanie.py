from funkcje import get_arguments, load_data, checkmate, print_result

options = get_arguments()
turn = load_data()

modulo = 1
if turn[0] == 'black':
    modulo = 0


MAX_DEEP = 10

for deep in [x for x in range(MAX_DEEP) if x%2==modulo]:
    _, answer = checkmate(turn, deep)
    if  answer :
        print_result( options, answer)
        break