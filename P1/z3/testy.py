from rozwiazanie import *
from modul import *

print('figurant-baza: ', figurant_baza)
print('blotkarz-baza: ', blotkarz_baza)
print()
print('figurant-talia: ', figurant_talia)
print('blotkarz-talia: ', blotkarz_talia)
print()
print('figurant-karty-w-rece: ', figurant_karty)
print('blotkarz-karty-w-rece: ', blotkarz_karty)
print()
print()
print('testy wlasciwe')

def dodaj_kolor(talia, kolor):
    return [(x, kolor) for x in talia]




talia_strit = ['as', 'król', 'dama', 'walet', '10']
talia_nstrit = ['as', 'król', 'dama', 'walet', '9']

talia_para = ['as', 'król', '10', 'walet', '10']
talia_2para = ['as', 'król', '10', 'król', '10']
talia_trzy = ['10', 'król', '10', 'walet', '10']


#testowanie pary:
if para( dodaj_kolor(talia_strit, 'kier') ) == True :
    print('para 1 err')
else:
    print('para 1 ok')

if para( dodaj_kolor(talia_para, 'kier') ) == False :
    print('para 2 err')
else:
    print('para 2 ok')




#testowanie dwoch par
if dwie_pary( dodaj_kolor(talia_para, 'kier') ) == True :
    print('2para 1 err')
else:
    print('2para 1 ok')

if dwie_pary( dodaj_kolor(talia_2para, 'kier') ) == False :
    print('2para 2 err')
else:
    print('2para 2 ok')




#testowanie trojki
if trojka( dodaj_kolor(talia_2para, 'kier') ) == True :
    print('trojka 1 err')
else:
    print('trojka 1 ok')

if trojka( dodaj_kolor(talia_trzy, 'kier') ) == False :
    print('trojka 2 err')
else:
    print('trojka 2 ok')




#testowanie strita:
if strit( dodaj_kolor(talia_strit, 'kier') ) == True :
    print('strit 1 ok')
else:
    print('strit 1 err')

if strit( dodaj_kolor(talia_nstrit, 'kier') ) == False :
    print('strit 2 ok')
else:
    print('strit 2 err')




#testowanie koloru
if kolor( dodaj_kolor(talia_2para, 'kier') ) == False :
    print('kolor 1 err')
else:
    print('kolor 1 ok')

talia_nkolor = dodaj_kolor(['as', 'król', '10', 'walet'], 'kier')
talia_nkolor = talia_nkolor + [('as', 'trefl')]

if kolor( talia_nkolor ) == True :
    print('kolor 2 err')
else:
    print('kolor 2 ok')




#testowanie full
talia_full = ['10', 'król', '10', 'król', '10']
talia_nfull = ['10', 'król', '10', 'walet', '10']
if full( dodaj_kolor(talia_full, 'kier') ) == True :
    print('full 1 ok')
else:
    print('full 1 err')

if full( dodaj_kolor(talia_nfull, 'kier') ) == False :
    print('full 2 ok')
else:
    print('full 2 err')




#testowanie karety
talia_kareta = ['10', '10', '10', 'król', '10']
talia_nkareta = ['10', 'król', '10', 'walet', '10']
if kareta( dodaj_kolor(talia_kareta, 'kier') ) == True :
    print('kareta 1 ok')
else:
    print('kareta 1 err')

if kareta( dodaj_kolor(talia_nkareta, 'kier') ) == False :
    print('kareta 2 ok')
else:
    print('kareta 2 err')