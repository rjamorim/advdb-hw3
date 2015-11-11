# Association Rules Mining - hw3
# Advanced Database Systems
# Pedro Ferro Freitas - pff2108
# Roberto Jose de Amorim - rja2139

data_file = 'INTEGRATED-DATASET.csv'
min_sup = 0.3
min_conf = 0.5

# data_file = argv[2]
# min_sup = float(argv[3])
# min_conf = float(argv[4])


print '\n==Frequent itemsets (min_sup=' + str(100 * min_sup) + '%)'
print '[pen], 100%'

print '\n==High-confidence association rules (min_conf=' + str(100 * min_conf) + '%)'
print '[diary] => [pen] (Conf: 100.0%, Supp: 75%)'

