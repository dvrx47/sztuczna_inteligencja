from modul import load_dic, load_text, insert_space

slownik = load_dic()

text = load_text()

for row in text:
	slowa = insert_space(row.strip(), slownik)
	print(slowa)
