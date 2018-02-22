def get_arguments():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-m", "--mode", dest='mode', default='batch' )

    (options, _) = parser.parse_args()

    return options


def load_data():
    turn =  open('input_1.1.txt').read().split()
    return turn


def make_move(turn, move):
    if turn[0] == 'black':
        return ['white'] + turn[1:3] + [ move[1:] ]
    else:
        if move[0] == 'K':
            return ['black'] + [ move[1:] ] + turn[2:4]  
        else:
            return ['black', turn[1], move[1:], turn[3] ]


def black_correct( turn ):
    if turn[3][0] == turn[2][0] or turn[3][1] == turn[2][1]:
        return False

    min_l = ord('a')
    max_l = ord('h')

    current_letter = ord( turn[1][0])
    current_index = int(turn[1][1])

    letters = [chr(x) for x in range(current_letter-1, current_letter+2 ) if min_l <= x <= max_l ]
    indexes = [str(x) for x in range(current_index-1, current_index+2) if 1 <= x <= 8 ]

    white_king_range = [l+i for l in letters for i in indexes] 

    if turn[3] in white_king_range:
        return False
    return True


def white_king_correct( turn ):
    min_l = ord('a')
    max_l = ord('h')

    current_letter = ord( turn[3][0])
    current_index = int(turn[3][1])

    letters = [chr(x) for x in range(current_letter-1, current_letter+2 ) if min_l <= x <= max_l ]
    indexes = [str(x) for x in range(current_index-1, current_index+2) if 1 <= x <= 8 ]

    black_king_range = [l+i for l in letters for i in indexes ]

    if turn[1] in black_king_range:
        return False

    if turn[1] == turn[2]:
        return False

    return True


def tower_correct( turn ):
    min_l = ord('a')
    max_l = ord('h')

    current_letter = ord( turn[3][0])
    current_index = int(turn[3][1])

    letters = [chr(x) for x in range(current_letter-1, current_letter+2 ) if min_l <= x <= max_l ]
    indexes = [str(x) for x in range(current_index-1, current_index+2) if 1 <= x <= 8 ]

    black_king_range = [l+i for l in letters for i in indexes ]

    if turn[2] in black_king_range:
        return False


    if turn[1] == turn[2]:
        return False
    return True


def black_king_moves(turn):
    min_l = ord('a')
    max_l = ord('h')

    current_letter = ord( turn[3][0])
    current_index = int(turn[3][1])

    letters = [chr(x) for x in range(current_letter-1, current_letter+2 ) if min_l <= x <= max_l ]
    indexes = [str(x) for x in range(current_index-1, current_index+2) if 1 <= x <= 8 ]

    moves = ['K'+l+i for l in letters for i in indexes if l+i != turn[3] ]

    return [m for m in moves if black_correct( make_move(turn, m) )]


def king_moves(turn):

    min_l = ord('a')
    max_l = ord('h')

    current_letter = ord( turn[1][0])
    current_index = int(turn[1][1])

    letters = [chr(x) for x in range(current_letter-1, current_letter+2 ) if min_l <= x <= max_l ]
    indexes = [str(x) for x in range(current_index-1, current_index+2) if 1 <= x <= 8 ]

    moves = ['K'+l+i for l in letters for i in indexes if l+i != turn[1] ]  

    return [m for m in moves if white_king_correct( make_move(turn, m) )]


def tower_moves(turn):

    lr_moves = ['T'+turn[2][0]+str(x) for x in range(1,9) if str(x) != turn[2][1]]
    up_moves = ['T'+chr(x)+turn[2][1] for x in range(ord('a'), ord('h')+1) if chr(x) != turn[2][0] ]
    moves = up_moves + lr_moves

    return [m for m in moves if tower_correct( make_move(turn, m) )]


def move_generator(turn):
    if turn[0] == 'black':
        return black_king_moves(turn)
    else:
        return king_moves(turn) + tower_moves(turn) 


def is_checkmate(turn):
    if turn[0] == 'white':
        return False
    else:
        if len( black_king_moves(turn) ) == 0 and (turn[3][0] == turn[2][0] or turn[3][1] == turn[2][1]):
            return True
        else:
            return False


def make_turn(turn, current_deep, max_deep):
    if current_deep == max_deep :
        if is_checkmate(turn):
            return True, []
        else:
            return False, []

    allowed_moves = move_generator( turn )

    for move in allowed_moves:
        mat, moves = make_turn( make_move(turn, move), current_deep+1, max_deep )
        if mat :
            return True, [move] + moves
    
    return False, []


def checkmate( turn, deep ):
    return make_turn(turn, 0, deep)


def print_result( args, result ):
    if args.mode == 'batch':
        print(len(result))
    elif args.mode == 'debug':
        print(result)
