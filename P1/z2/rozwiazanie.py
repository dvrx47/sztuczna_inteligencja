from modul import load_dic, load_text, insert_space

slownik = load_dic()

text = load_text()
slowa = insert_space(text, slownik)

print(slowa)
