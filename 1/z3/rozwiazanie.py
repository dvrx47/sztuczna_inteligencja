figurant_baza = ['as', 'król', 'dama', 'walet']
blotkarz_baza = [str(x) for x in range(1,11)]

kolory = ['kier', 'pik', 'karo', 'trefl']

figurant_talia = [(x,y) for x in figurant_baza for y in kolory]
blotkarz_talia = [(x,y) for x in blotkarz_baza for y in kolory]

liczba_testow = 10000

import numpy as np
from modul import runda

wygrane_figurant = 0
wygrane_blotkarz = 0
for test in range(liczba_testow):
    #losowanie kart
    figurant_karty = list(np.random.permutation( figurant_talia ) [:5])
    blotkarz_karty = list(np.random.permutation( blotkarz_talia ) [:5])
    p_f, p_b = runda(figurant_karty, blotkarz_karty)
    wygrane_figurant += p_f
    wygrane_blotkarz += p_b

print('szansa na wygrana figuranta:', wygrane_figurant/liczba_testow*100, '%'  )
print('szansa na wygrana blotkarza:', wygrane_blotkarz/liczba_testow*100, '%'  )
