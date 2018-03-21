def load_dic():
    set_of_words =  set(open('polish_words.txt').read().split())
    return set_of_words

def load_text():
    return open('text_testowy.txt').readlines()


def fix_text(text, dictionary):
	if text == "":
		return True, [], 0
		
	if len(text) == 1:
		if text in dictionary:
			return True, [text], 1
		else:
			return False, [], 0
	
	if text in dictionary:
		return True, [text], len(text)**2
	
	
	mid = len(text)//2
	

	max_complete, max_list, max_val = False, [], 1
	
	for i in range( max(0, mid-33), mid+1 ):
		for j in range(mid, min(mid+33, len(text) )+1 ):
			if j-i >= 33:
				break
			
			if text[i:j] in dictionary or text[i:j] == []:
				
				left_done, left_list, left_max = fix_text( text[0:i], dictionary )
				if left_done == False:
					continue
				
				right_done, right_list, right_max = fix_text( text[j:], dictionary )
				
				if right_done == False:
					continue
					
				if max_complete == False:
					max_complete = True
					max_list = left_list + [ text[i:j] ] + right_list
					max_val = left_max + len(text[i:j])**2 + right_max
					
				elif max_val < left_max + len(text[i:j])**2 + right_max:
					max_list = left_list + [ text[i:j] ] + right_list
					max_val = left_max + len(text[i:j])**2 + right_max
	
	
	return max_complete, max_list, max_val



def insert_space(text, dictionary):
    bol, slowa, val = fix_text(text, dictionary)
    if slowa :
        return slowa
