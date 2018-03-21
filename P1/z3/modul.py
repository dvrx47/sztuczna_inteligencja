def para(karty):
    sl_k = dict()
    for k in karty:
        if k[0] in sl_k:
            sl_k[ k[0] ] += 1
        else:
            sl_k[ k[0] ] = 1
    
    for w in sl_k:
        if sl_k[w] >= 2:
            return True
    return False


def dwie_pary(karty):
    sl_k = dict()
    for k in karty:
        if k[0] in sl_k:
            sl_k[ k[0] ] += 1
        else:
            sl_k[ k[0] ] = 1
    
    ilosc_par=0    
    for w in sl_k:
        if sl_k[w] >= 2:
            ilosc_par += 1
    
    if ilosc_par == 2:
        return True
    
    return False


def trojka(karty):
    sl_k = dict()
    for k in karty:
        if k[0] in sl_k:
            sl_k[ k[0] ] += 1
        else:
            sl_k[ k[0] ] = 1
    
    for w in sl_k:
        if sl_k[w] >= 3:
            return True

    return False


def strit(karty):
    karty_set = set([x[0] for x in karty ])
    order = [str(x) for x in range(1,11)] + ['walet', 'dama', 'król', 'as']

    for i in range(5, len(order)+1):
        if karty_set == set( order[i-5 : i] ):
            return True
    return False


def kolor(karty):
    aktualny_kolor = karty[0][1]

    for k in karty:
        if aktualny_kolor != k[1]:
            return False

    return True


def full(karty):
    sl_k = dict()
    for k in karty:
        if k[0] in sl_k:
            sl_k[ k[0] ] += 1
        else:
            sl_k[ k[0] ] = 1
    
    dwa = False
    trzy = False   
    for w in sl_k:
        if sl_k[w] == 2:
            dwa = True
        elif sl_k[w] == 3:
            trzy = True

    return trzy and dwa
    


def kareta(karty):
    sl_k = dict()
    for k in karty:
        if k[0] in sl_k:
            sl_k[ k[0] ] += 1
        else:
            sl_k[ k[0] ] = 1
    
    for w in sl_k:
        if sl_k[w] >= 4:
            return True

    return False


def poker(karty):
    return kolor(karty) and strit(karty)


def runda(figurant, blotkarz):
    if poker(blotkarz) :
        return 0, 1

    reguly = [kareta, full, kolor, strit, trojka, dwie_pary, para]

    for regula in reguly:
        if regula(figurant):
            return 1, 0
        
        if regula(blotkarz):
            return 0, 1

    return 1, 0