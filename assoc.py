# Association Rules Mining - hw3
# Advanced Database Systems
# Pedro Ferro Freitas - pff2108
# Roberto Jose de Amorim - rja2139

import csv
from collections import defaultdict
from sys import argv

# data_file = 'INTEGRATED-DATASET.csv'
# min_sup = 0.4
# min_conf = 0.7

data_file = argv[1]
min_sup = float(argv[2])
min_conf = float(argv[3])


class MiningAlgorithm(object):
    # Object responsible for the association rules mining

    def __init__(self):
        self.elements = set()
        self.max_elements = 0
        self.n_transactions = 0
        self.transactions = defaultdict(set)
        self.counts = defaultdict(int)
        self.l_itemsets = defaultdict(list)
        self.c_itemsets = defaultdict(list)
        self.sorted_support_list = []
        self.sorted_confidence_list = []

    def read_dataset(self, name):
        # P1: Read and process dataset file.
        try:
            with open(name, 'rb') as csvfile:
                data = csv.reader(csvfile, delimiter=',')
                t_id = 0
                for row in data:
                    t_id += 1
                    # # Compute number of elements of the transaction with the largest number of elements
                    n_elements = len(row)
                    if n_elements > self.max_elements:
                        self.max_elements = n_elements
                    # Process each line of csv file
                    for key in row:
                        self.elements.add(key)
                        self.transactions[t_id].add(key)
                        self.counts[(key,)] += 1
        except IOError:
            print "File not found or unreadable"
            exit(1)
        self.n_transactions = t_id

    def association_rules_mining(self):
        # P2: Algorithm core, calling the most important functions.
        # Compute L_1:
        for entry in sorted(self.elements):
            support = float(self.counts[(entry,)]) / self.n_transactions
            if support >= min_sup:
                self.l_itemsets[1].append([entry])
        # Compute L_k for k>1:
        # # Largest itemset has, at most, number of elements equal to transaction with the largest number of elements
        for i in range(2, self.max_elements + 1):
            self.candidate_generation(i)
            self.support_update(i)
            self.compute_large_itemsets(i)
            # Interrupt the loop if L_k is empty
            if len(self.l_itemsets[i]) == 0:
                break

    def candidate_generation(self, iteration):
        # P2-a: Generate new candidates from the large itemsets from last iteration.
        # Join step:
        for element1 in self.l_itemsets[iteration - 1]:
            for element2 in self.l_itemsets[iteration - 1]:
                if element1[0:iteration - 2] == element2[0:iteration - 2]:
                    if element1[iteration - 2] < element2[iteration - 2]:
                        self.c_itemsets[iteration].append(element1 + element2[iteration - 2:])
        # Prune step:
        for entry in self.c_itemsets[iteration]:
            for bkpoint in range(len(entry)):
                subset = entry[:bkpoint] + entry[bkpoint + 1:]
                if subset not in self.l_itemsets[iteration - 1]:
                    bkpoint2 = self.c_itemsets[iteration].index(entry)
                    temp = self.c_itemsets[iteration][:bkpoint2] + self.c_itemsets[iteration][bkpoint2 + 1:]
                    self.c_itemsets[iteration] = temp
                    break

    def support_update(self, iteration):
        # P2-b: Calculate the support for the candidates in the k-th iteration.
        for t_id in self.transactions.keys():
            set1 = self.transactions[t_id]
            for entry in self.c_itemsets[iteration]:
                set2 = set(entry)
                if len(set1.intersection(set2)) == iteration:
                    self.counts[tuple(sorted(set1.intersection(set2)))] += 1

    def compute_large_itemsets(self, iteration):
        # P2-c: Determine the itemsets for the k-th iteration, with k elements.
        for entry in self.c_itemsets[iteration]:
            support = float(self.counts[tuple(entry)]) / self.n_transactions
            # Compare support for each candidate with threshold
            if support >= min_sup:
                self.l_itemsets[iteration].append(entry)

    def print_sorted_results(self):
        # P3: Print support and confidence in the desired format.
        # Priting Support:
        print '\n==Frequent itemsets (min_sup=%.0f%%)' % (100 * min_sup)
        support_list = []
        for iteration in self.l_itemsets.keys():
            for key in self.l_itemsets[iteration]:
                count = self.counts[tuple(key)]
                support_list.append((iteration, key, count))
        self.sorted_support_list = sorted(support_list, key=lambda entry: entry[2], reverse=True)
        for iteration, key, count in self.sorted_support_list:
            support = int(100. * count / self.n_transactions)
            print '[%s], %.0f%%' % (','.join(key), support)
        # Printing Confidence:
        print '\n==High-confidence association rules (min_conf=%.0f%%)' % (100 * min_conf)
        confidence_list = []
        for iteration in self.l_itemsets.keys():
            if iteration == 1:
                continue
            for key2 in self.l_itemsets[iteration]:
                count2 = self.counts[tuple(key2)]
                sup = float(count2) / self.n_transactions
                for key in key2:
                    temp = set(key2)
                    temp.remove(key)
                    temp2 = sorted(temp)
                    count = self.counts[tuple(temp2)]
                    conf = float(count2) / count
                    confidence_list.append((key, temp2, sup, conf))
        self.sorted_confidence_list = sorted(confidence_list, key=lambda entry: entry[3], reverse=True)
        for key, temp2, sup, conf in self.sorted_confidence_list:
            if conf >= min_conf and sup > min_sup:
                conf = round(100. * conf, 1)
                sup = round(100. * sup, 0)
                result = ','.join(list(temp2))
                print '[%s] => [%s] (Conf: %.1f%%, Supp: %.0f%%)' % (result, key, conf, sup)


ARMalgo = MiningAlgorithm()
ARMalgo.read_dataset(data_file)
ARMalgo.association_rules_mining()
ARMalgo.print_sorted_results()
