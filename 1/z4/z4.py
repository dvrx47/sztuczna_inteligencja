def ones( binary_word ):
	count = 0
	for x in binary_word:
		if x=='1':
			count += 1
	return count

def opt_dist( binary_word, D):
	min_val = len(binary_word)
	
	for i in range(0, len(binary_word) - D+1):
		cost = 0
		cost += ones( binary_word[:i] )
		cost += D - ones(binary_word[i:i+D])
		cost += ones(binary_word[i+D:])
		if cost < min_val:
			min_val = cost
	return min_val

for i in [5,4,3,2,1,0]:
	print(opt_dist('0010001000', i))