def generate_all_subsets(numbers):
	if numbers == []:
		return [[]]
	x = generate_all_subsets(numbers[1:])
	return x + [[numbers[0]] + y for y in x]

def generate_subsets(numbers, return_all=False):
	x = generate_all_subsets(numbers)
	if return_all:
		return [i for i in x if len(i)>0]
	return [i for i in x if len(i)>0 and len(i)<len(numbers)]

class Apriori:
	def __init__(self, path="./input.txt", min_support=2, max_lim=10):
		self.max_lim = max_lim
		self.path = path
		self.min_support = min_support
		self.k = 0
		self.frequent_item_sets = []

	def read_data(self):
		with open(self.path, "r") as f:
			data = [sorted(list(set([item for item in line.replace('\n', '').split(', ')]))) for line in f.readlines()]
		return data

	def degenerating_based_can_be_pruned(self, data, return_index=False):
		prunable_indices = []
		for index, itemset in enumerate(data):
			for subset in generate_subsets(itemset):
				if subset not in self.frequent_item_sets and len(self.frequent_item_sets)!=0:
					if not return_index:
						print("For itemset:", set(itemset), "subset:", set(subset), "was not found to be a Frequent Item Set. This itemset shall be pruned.")
					prunable_indices.append(index)
					break
		if return_index:
			return prunable_indices
		return len(prunable_indices)!=0

	def degenerating_based_prune(self, data):
		indices = self.degenerating_based_can_be_pruned(data, return_index=True)
		return [itemset for index, itemset in enumerate(data) if index not in indices]

	def count_support_based_can_be_pruned(self, original_transactions, previous_itemsets, return_index=False):
		prunable_indices = []
		candidate_count = {}
		for index, itemset in enumerate(previous_itemsets):
			itemset = sorted(itemset)
			count_support = 0
			for transaction in original_transactions:
				transaction_subsets = generate_subsets(transaction, return_all=True)
				transaction_subsets = [sorted(itemset) for itemset in transaction_subsets]
				if itemset in transaction_subsets:
					count_support += 1
			if count_support<self.min_support:
				if not return_index:
					print("For itemset:", itemset, "support found is:", count_support, ", failing the minimum support condition. This itemset shall be pruned.")
				prunable_indices.append(index)
			else:
				candidate_count.update({str(itemset): count_support})
		if not return_index:
			print("Computed Support Count for each itemset:")
			for itemset, count in candidate_count.items():
				print(itemset+":", count)
		if return_index:
			return prunable_indices
		else:
			return len(prunable_indices)!=0

	def count_support_based_prune(self, original_transactions, previous_itemsets):
		indices = self.count_support_based_can_be_pruned(original_transactions, previous_itemsets, return_index=True)
		return [itemset for index, itemset in enumerate(previous_itemsets) if index not in indices]

	def get_large_itemsets(self, original_transactions, previous_itemsets):
		if self.degenerating_based_can_be_pruned(previous_itemsets):
			previous_itemsets = self.degenerating_based_prune(previous_itemsets)
		if self.count_support_based_can_be_pruned(original_transactions, previous_itemsets):
			previous_itemsets = self.count_support_based_prune(original_transactions, previous_itemsets)
		return previous_itemsets

	def generate_future_candidate_sets(self, previous_itemsets):
		prev_len = len(previous_itemsets[0])
		all_attributes = []
		for itemset in previous_itemsets:
			all_attributes.extend(itemset)
			all_attributes = list(set(all_attributes))
		subsets = generate_subsets(all_attributes)
		self.k += 1
		return [subset for subset in subsets if len(subset)==self.k+1]

	def get_initial_candidate_itemsets(self, original_transactions):
		candidate_itemsets = []
		for transaction in original_transactions:
			candidate_itemsets.extend(transaction)
			candidate_itemsets = list(set(candidate_itemsets))
		return [[item] for item in sorted(candidate_itemsets)]

	def find(self, original_transactions):
		found = False
		candidate_itemsets = self.get_initial_candidate_itemsets(original_transactions)
		iter_round = 0
		while not found and iter_round<self.max_lim and len(candidate_itemsets)>1:
			print("ROUND:", self.k+1)
			print("Candidate Itemsets (C"+str(self.k+1)+"):", str(candidate_itemsets).replace("(", "{").replace(")", "}"))
			iter_round +=1
			large_itemsets = self.get_large_itemsets(original_transactions, candidate_itemsets)
			print("Large Itemsets (L"+str(self.k+1)+"):", str(large_itemsets).replace("(", "{").replace(")", "}"))
			if len(large_itemsets)==1:
				print("\n\nFound:", large_itemsets[0])
				exit()
			else:
				print("Running Generator...")
				candidate_itemsets = self.generate_future_candidate_sets(large_itemsets)

if __name__ == '__main__':
	apriori = Apriori(path="./input.txt", min_support=3, max_lim=4)
	data = apriori.read_data()
	apriori.find(data)