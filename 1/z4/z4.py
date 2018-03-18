def ones( binary_word ):
	res = [0]
	for i in binary_word:
		res.append( res[-1] + i )
	return res
	

def opt_dist( binary_word, D):
	min_val = len(binary_word)
	ca = ones( binary_word )
	
	for i in range(1, len(binary_word) - D + 1):
		cost = D + ca[-1] - 2*ca[i+D-1]+2*ca[i-1]
		if cost < min_val:
			min_val = cost
	return min_val
