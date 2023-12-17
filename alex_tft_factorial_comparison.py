
import numpy as np
import matplotlib.pyplot as plt
import scipy.special

def nCk(n, k):
	return scipy.special.comb(n, k)

def AlexTFTChoices(n, k, L, Q):
	a = nCk(n-(L+Q), k)
	b = (L+Q) * nCk(n-(L+Q), k-1)
	c = (L*Q) * nCk(n-(L+Q), k-2)
	return a+b+c 

def ComparisonGenerator(n_max, k_max, L, Q):
	full_count_data = np.zeros((n_max-(L+Q), k_max))
	alex_method_data = np.zeros((n_max-(L+Q), k_max))
	for i in range((L+Q), n_max):
		# print i
		for j in range(k_max):
			# print j
			n = i+1
			k = j+1
			# if k > n:
			# 	break
			full_count_data[i-(L+Q), j] = nCk(n, k)
			alex_method_data[i-(L+Q),j] = AlexTFTChoices(n,k,L,Q)
	# 		if k == 9:
	# 			print "-------------------------------------------------------"
	# 			print "(n, k) = ({},{})".format(n,k)
	# 			print "nCk = {}".format(full_count_data[i-(L+Q),j])
	# 			print "Alex says # of valid teams is: {}".format(alex_method_data[i-(L+Q),j])
	# print "-------------------------------------------------------"
	ratio = np.divide(alex_method_data, full_count_data) * 100
	return ratio

def ManyLuxAndQiyanaVariants(n_max, k_max, L_max, Q_max):
	storage = []
	for l in range(1, L_max+1):
		for q in range(1, Q_max+1):
			storage.append(ComparisonGenerator(n_max, k_max, l, q))
	return storage

def ComparisonPlotter(ratio_array, n_max, k_max, l, q):
	im = plt.imshow(ratio_array, aspect = 'auto', extent = [0.5,k_max+0.5,(L+Q),n_max], origin = "lower")
	plt.colorbar()
	plt.title('Percentage of Teams Alex Says You Need to Check')
	plt.ylabel("Number of Characters")
	plt.xlabel("Maximum Team Size")
	plt.show()

def ManyLuxAndQiyanaPlotter(storage_array, n_max, k_max, L_max, Q_max):
	fig, axs = plt.subplots(L_max, Q_max, sharex = 'col', sharey = 'row')
	# print len(storage_array)
	fig.suptitle("Comparison Of Naive Method and Alex's Method For Counting TFT Teams")

	for l in range(L_max):
		for q in range(Q_max):
			# print storage_array[l+q].shape
			axs[l,q].imshow(storage_array[l+q], aspect = 'auto', extent = [0.5, k_max+0.5, (l+q), n_max], origin = 'lower')
			# axs[l,q].set_ylabel("Number of Characters")
			# axs[l,q].set_xlabel("Maximum Team Size")
			axs[l,q].set_title('{} Lux Variants and {} Qiyana Variants'.format(l,q))

	im = axs.flatten()[0]
	cbar = fig.colorbar(im, ax=axs.ravel().tolist(), shrink=0.95)
	plt.show()


Q = 4
L = 10

ratio = ComparisonGenerator(68, 9, L, Q)
ComparisonPlotter(ratio, 68, 9, L, Q)

# test = ManyLuxAndQiyanaVariants(68, 9, 5, 2)
# ManyLuxAndQiyanaPlotter(test, 68, 9, 5, 2)