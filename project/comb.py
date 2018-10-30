from random import shuffle
class comb:
	def __init__(self):
		self.min_items = 3
		self.max_items = 6
		self.limit = 70

	def get_combinations(self,limit,min_items,max_items):
		self.min_items = min_items
		self.max_items = max_items
		self.limit = limit - 1
		combinations = self.combinations(self.limit,[])
		for i in range(len(combinations)-1,-1,-1):
			if not combinations[i]:
				combinations.pop(i)
				continue
			if len(combinations[i]) < self.min_items:
				combinations.pop(i)
		shuffle(combinations)
		return combinations

	def combinations(self,n,combs):
		if n == (self.limit - self.max_items):
			for i in range(n):
				combs.append([i])
			return combs
		else:
			combs = self.combinations(n-1,combs)
			ncombs = combs[0:]
			for c in combs:
				nc = (c + [n])
				nc.sort()
				if nc not in ncombs:
					ncombs.append(nc)
			ncombs.append([n])
			return ncombs


