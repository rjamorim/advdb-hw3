# Association Rules Mining - hw3
# Advanced Database Systems
# Pedro Ferro Freitas - pff2108
# Roberto Jose de Amorim - rja2139

data_file = 'test-dataset.csv'  # INTEGRATED-DATASET.csv
min_sup = 0.3
min_conf = 0.5

# data_file = argv[2]
# min_sup = float(argv[3])
# min_conf = float(argv[4])

from collections import defaultdict

class miningAlgorithm(object):

    def __init__(self):
        self.a = 0
        self.n_elements = 0
        self.candidates = defaultdict(set)

    def read_dataset(self):
        self.n_elements = 10

    def association(self):
        self.a += 1
        for i in range(self.n_elements):
            self.compute_large_itemsets(i)
            if self.candidates[i] == []:
                break

    def compute_large_itemsets(self, iteration):
        self.a *= 2
        self.candidate_generation(iteration)

    def candidate_generation(self, iteration):
        # Join step:
        self.a *= 0.5
        # Prune step:
        self.a += 3

        # Compare to thresholds..
        self.candidates[iteration].add(self.a)


ARMalgo = miningAlgorithm()

print '\n==Frequent itemsets (min_sup=' + str(100 * min_sup) + '%)'
print '[pen], 100%'

print '\n==High-confidence association rules (min_conf=' + str(100 * min_conf) + '%)'
print '[diary] => [pen] (Conf: 100.0%, Supp: 75%)'
