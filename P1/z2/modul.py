def load_dic():
    set_of_words =  set(open('polish_words.txt').read().split())
    return set_of_words

def load_text():
    return open('text_testowy.txt').read().split() [0]


def fix_text(text, dictionary, suma):
    max_word_length = 33

    if text in dictionary and suma == len(text)*len(text):
        return True, [text]

    for length in reversed(range(1, min(max_word_length, len(text)))):
        if text[:length] in dictionary:
            whole_word, words_list = fix_text(text[length:], dictionary, suma - len(text[:length])*len(text[:length]))
            if whole_word : 
                return True, [text[:length]] + words_list
    
    return False, []



def insert_space(text, dictionary):
    l2 = len(text)*len(text)
    for sq in reversed( range(l2) ):
        _, slowa = fix_text(text, dictionary, sq)
        if slowa :
            return slowa