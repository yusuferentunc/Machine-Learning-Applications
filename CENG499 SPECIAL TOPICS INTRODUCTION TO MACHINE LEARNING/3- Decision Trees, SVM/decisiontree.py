import pickle
from graphviz import *
from dt import divide, entropy, info_gain, gain_ratio, gini, avg_gini_index, chi_squared_test
import random

#Chi-Square Distribution Table
#                        .995[0]  .99[1]   .975[2]  .95[3]   .9[4]    .1[5]    .05[6]   .025[7]  .01[8]   .005[9]
Distribution_Table = [[  0.000,   0.000,   0.001,   0.004,   0.016,   2.706,   3.841,   5.024,   6.635,   7.879],
       [  0.010,   0.020,   0.051,   0.103,   0.211,   4.605,   5.991,   7.378,   9.210,  10.597],
       [  0.072,   0.115,   0.216,   0.352,   0.584,   6.251,   7.815,   9.348,  11.345,  12.838],
       [  0.207,   0.297,   0.484,   0.711,   1.064,   7.779,   9.488,  11.143,  13.277,  14.860],
       [  0.412,   0.554,   0.831,   1.145,   1.610,   9.236,  11.070,  12.833,  15.086,  16.750],
       [  0.676,   0.872,   1.237,   1.635,   2.204,  10.645,  12.592,  14.449,  16.812,  18.548],
       [  0.989,   1.239,   1.690,   2.167,   2.833,  12.017,  14.067,  16.013,  18.475,  20.278],
       [  1.344,   1.646,   2.180,   2.733,   3.490,  13.362,  15.507,  17.535,  20.090,  21.955],
       [  1.735,   2.088,   2.700,   3.325,   4.168,  14.684,  16.919,  19.023,  21.666,  23.589],
       [  2.156,   2.558,   3.247,   3.940,   4.865,  15.987,  18.307,  20.483,  23.209,  25.188],
       [  2.603,   3.053,   3.816,   4.575,   5.578,  17.275,  19.675,  21.920,  24.725,  26.757],
       [  3.074,   3.571,   4.404,   5.226,   6.304,  18.549,  21.026,  23.337,  26.217,  28.300],
       [  3.565,   4.107,   5.009,   5.892,   7.042,  19.812,  22.362,  24.736,  27.688,  29.819],
       [  4.075,   4.660,   5.629,   6.571,   7.790,  21.064,  23.685,  26.119,  29.141,  31.319],
       [  4.601,   5.229,   6.262,   7.261,   8.547,  22.307,  24.996,  27.488,  30.578,  32.801],
       [  5.142,   5.812,   6.908,   7.962,   9.312,  23.542,  26.296,  28.845,  32.000,  34.267],
       [  5.697,   6.408,   7.564,   8.672,  10.085,  24.769,  27.587,  30.191,  33.409,  35.718],
       [  6.265,   7.015,   8.231,   9.390,  10.865,  25.989,  28.869,  31.526,  34.805,  37.156],
       [  6.844,   7.633,   8.907,  10.117,  11.651,  27.204,  30.144,  32.852,  36.191,  38.582],
       [  7.434,   8.260,   9.591,  10.851,  12.443,  28.412,  31.410,  34.170,  37.566,  39.997],
       [  8.034,   8.897,  10.283,  11.591,  13.240,  29.615,  32.671,  35.479,  38.932,  41.401],
       [  8.643,   9.542,  10.982,  12.338,  14.041,  30.813,  33.924,  36.781,  40.289,  42.796],
       [  9.260,  10.196,  11.689,  13.091,  14.848,  32.007,  35.172,  38.076,  41.638,  44.181],
       [  9.886,  10.856,  12.401,  13.848,  15.659,  33.196,  36.415,  39.364,  42.980,  45.559],
       [ 10.520,  11.524,  13.120,  14.611,  16.473,  34.382,  37.652,  40.646,  44.314,  46.928],
       [ 11.160,  12.198,  13.844,  15.379,  17.292,  35.563,  38.885,  41.923,  45.642,  48.290],
       [ 11.808,  12.879,  14.573,  16.151,  18.114,  36.741,  40.113,  43.195,  46.963,  49.645],
       [ 12.461,  13.565,  15.308,  16.928,  18.939,  37.916,  41.337,  44.461,  48.278,  50.993],
       [ 13.121,  14.256,  16.047,  17.708,  19.768,  39.087,  42.557,  45.722,  49.588,  52.336],
       [ 13.787,  14.953,  16.791,  18.493,  20.599,  40.256,  43.773,  46.979,  50.892,  53.672],
       [ 20.707,  22.164,  24.433,  26.509,  29.051,  51.805,  55.758,  59.342,  63.691,  66.766],
       [ 27.991,  29.707,  32.357,  34.764,  37.689,  63.167,  67.505,  71.420,  76.154,  79.490],
       [ 35.534,  37.485,  40.482,  43.188,  46.459,  74.397,  79.082,  83.298,  88.379,  91.952],
       [ 43.275,  45.442,  48.758,  51.739,  55.329,  85.527,  90.531,  95.023, 100.425, 104.215],
       [ 51.172,  53.540,  57.153,  60.391,  64.278,  96.578, 101.879, 106.629, 112.329, 116.321],
       [ 59.196,  61.754,  65.647,  69.126,  73.291, 107.565, 113.145, 118.136, 124.116, 128.299],
       [ 67.328,  70.065,  74.222,  77.929,  82.358, 118.498, 124.342, 129.561, 135.807, 140.169]]

def label_selection(node,attr_vals_list):
	l = [0]*len(attr_vals_list[-1])
	for item in node:
		l[attr_vals_list[-1].index(item[-1])] +=1
	return attr_vals_list[-1][l.index(max(l))]

#Information Gain 


def dec_ig_helper(node,attr_vals_list,attr_names,depth):
	if len(node) == 0:
		return[attr_vals_list[-1][0]]
	if depth == 0:
		return label_selection(node,attr_vals_list)
	tree = []
	temp = 0
	selected_index = -1
	selected_division = []
	for i in range(len(attr_vals_list)-1):
		if attr_vals_list[i] == "PassThatAttribute":
			continue
		[gain,buckets] = info_gain(node,i,attr_vals_list)
		if gain > temp :
			temp = gain
			selected_index = i
			selected_division = buckets
	tree.append(attr_names[selected_index])
	if selected_index == -1:
		if entropy(node,attr_vals_list) < 10 ** -5:
			if len(node) != 0:
				return node[0][-1]
		else:
			return[attr_vals_list[-1][0]]

	attr_vals_list[selected_index] = "PassThatAttribute"
	attr_names[selected_index] = "PassThatName"
	depth -= 1
	for bucket in selected_division:
		list_temp = attr_vals_list[:]
		list_temp2 = attr_names[:]
		tree.append(dec_ig_helper(bucket,list_temp,list_temp2,depth))
	return tree 

def dec_ig(train_data,attr_vals_list,attr_names):
	depth = len(attr_names)
	tree = []
	temp = 0
	selected_index = -1
	selected_division = []
	for i in range(len(attr_vals_list)-1):
		[gain,buckets] = info_gain(train_data,i,attr_vals_list)
		if gain > temp :
			temp = gain
			selected_index = i
			selected_division = buckets
	tree.append(attr_names[selected_index])
	attr_vals_list[selected_index] = "PassThatAttribute"
	attr_names[selected_index] = "PassThatName"
	depth -= 1 
	for bucket in selected_division:
		list_temp = attr_vals_list[:]
		list_temp2 = attr_names[:]
		tree.append(dec_ig_helper(bucket,list_temp,list_temp2,depth))
	return(tree)
#---------------------------------------------------------------------------

#Gain Ratio

def dec_gr_helper(node,attr_vals_list,attr_names,depth):
	if len(node) == 0:
		return[attr_vals_list[-1][0]]
	if depth == 0:
		return label_selection(node,attr_vals_list)
	tree = []
	temp = 0
	selected_index = -1
	selected_division = []
	for i in range(len(attr_vals_list)-1):
		if attr_vals_list[i] == "PassThatAttribute":
			continue
		[gain,buckets] = gain_ratio(node,i,attr_vals_list)
		if gain > temp :
			temp = gain
			selected_index = i
			selected_division = buckets
	tree.append(attr_names[selected_index])
	if selected_index == -1:
		if entropy(node,attr_vals_list) == 0:
			if len(node) != 0:
				return node[0][-1]
		else:
			return[attr_vals_list[-1][0]]

	attr_vals_list[selected_index] = "PassThatAttribute"
	attr_names[selected_index] = "PassThatName"
	depth -= 1
	for bucket in selected_division:
		list_temp = attr_vals_list[:]
		list_temp2 = attr_names[:]
		tree.append(dec_gr_helper(bucket,list_temp,list_temp2,depth))
	return tree 

def dec_gr(train_data,attr_vals_list,attr_names):
	depth = len(attr_names)
	tree = []
	temp = 0
	selected_index = -1
	selected_division = []
	for i in range(len(attr_vals_list)-1):
		[gain,buckets] = gain_ratio(train_data,i,attr_vals_list)
		if gain > temp :
			temp = gain
			selected_index = i
			selected_division = buckets
	tree.append(attr_names[selected_index])
	attr_vals_list[selected_index] = "PassThatAttribute"
	attr_names[selected_index] = "PassThatName"
	depth -= 1 
	for bucket in selected_division:
		list_temp = attr_vals_list[:]
		list_temp2 = attr_names[:]
		tree.append(dec_gr_helper(bucket,list_temp,list_temp2,depth))
	return(tree)
#---------------------------------------------------------------------------

#Average Gini Index

def dec_gi_helper(node,attr_vals_list,attr_names,depth):
	if len(node) == 0:
		return[attr_vals_list[-1][0]]
	if depth == 0:
		return label_selection(node,attr_vals_list)
	tree = []
	temp = 9999999 #max
	selected_index = -1
	selected_division = []
	for i in range(len(attr_vals_list)-1):
		if attr_vals_list[i] == "PassThatAttribute":
			continue
		[agi,buckets] = avg_gini_index(node,i,attr_vals_list)
		if agi < temp :
			temp = agi
			selected_index = i
			selected_division = buckets
	tree.append(attr_names[selected_index])
	if selected_index == -1:
		if entropy(node,attr_vals_list) == 0:
			if len(node) != 0:
				return node[0][-1]
		else:
			return[attr_vals_list[-1][0]]

	attr_vals_list[selected_index] = "PassThatAttribute"
	attr_names[selected_index] = "PassThatName"
	depth -= 1
	for bucket in selected_division:
		list_temp = attr_vals_list[:]
		list_temp2 = attr_names[:]
		tree.append(dec_gi_helper(bucket,list_temp,list_temp2,depth))
	return tree 

def dec_gi(train_data,attr_vals_list,attr_names):
	depth = len(attr_names)
	tree = []
	temp = 99999
	selected_index = -1
	selected_division = []
	for i in range(len(attr_vals_list)-1):
		[agi,buckets] = avg_gini_index(train_data,i,attr_vals_list)
		if agi < temp :
			temp = agi
			selected_index = i
			selected_division = buckets
	tree.append(attr_names[selected_index])
	attr_vals_list[selected_index] = "PassThatAttribute"
	attr_names[selected_index] = "PassThatName"
	depth -= 1 
	for bucket in selected_division:
		list_temp = attr_vals_list[:]
		list_temp2 = attr_names[:]
		tree.append(dec_gi_helper(bucket,list_temp,list_temp2,depth))
	return(tree)
#---------------------------------------------------------------------------

#Information Gain with Chi-Squared


def dec_gr_chi_helper(node,attr_vals_list,attr_names,depth):
	if len(node) == 0:
		return[attr_vals_list[-1][0]]
	if depth == 0:
		return label_selection(node,attr_vals_list)
	tree = []
	temp = 0
	selected_index = -1
	selected_division = []
	for i in range(len(attr_vals_list)-1):
		if attr_vals_list[i] == "PassThatAttribute":
			continue
		if len(node) > 3 and chi_squere_hyp(node,i,attr_vals_list):
			attr_vals_list[i] = "PassThatAttribute"
			attr_names[i] = "PassThatName"
			continue
		[gain,buckets] = gain_ratio(node,i,attr_vals_list)
		if gain > temp :
			temp = gain
			selected_index = i
			selected_division = buckets
	tree.append(attr_names[selected_index])
	if selected_index == -1:
		if entropy(node,attr_vals_list) < 10 ** -5:
			if len(node) != 0:
				return node[0][-1]
		else:
			return[attr_vals_list[-1][0]]

	attr_vals_list[selected_index] = "PassThatAttribute"
	attr_names[selected_index] = "PassThatName"
	depth -= 1
	for bucket in selected_division:
		list_temp = attr_vals_list[:]
		list_temp2 = attr_names[:]
		tree.append(dec_gr_chi_helper(bucket,list_temp,list_temp2,depth))
	return tree 

def dec_gr_chi(train_data,attr_vals_list,attr_names):
	depth = len(attr_names)
	tree = []
	temp = 0
	selected_index = -1
	selected_division = []
	for i in range(len(attr_vals_list)-1):
		if len(train_data) > 3 and chi_squere_hyp(train_data,i,attr_vals_list):
			attr_vals_list[i] = "PassThatAttribute"
			attr_names[i] = "PassThatName"
			continue
		[gain,buckets] = gain_ratio(train_data,i,attr_vals_list)
		if gain > temp :
			temp = gain
			selected_index = i
			selected_division = buckets
	tree.append(attr_names[selected_index])
	attr_vals_list[selected_index] = "PassThatAttribute"
	attr_names[selected_index] = "PassThatName"
	depth -= 1 
	for bucket in selected_division:
		list_temp = attr_vals_list[:]
		list_temp2 = attr_names[:]
		tree.append(dec_gr_chi_helper(bucket,list_temp,list_temp2,depth))
	return(tree)
#---------------------------------------------------------------------------
def drawer(tree,index,dot,vals,names):
	if not isinstance(tree,str):
		dot.node(index,tree[0])
		if len(tree) > 1:
			for i in range(1,len(tree)):
				lab = vals[names.index(tree[0])][i-1]
				dot.edge(index,index+str(i),label = str(lab))
				drawer(tree[i],index+str(i),dot,vals,names)
	else:
		dot.node(index,tree)


def test_tree_helper(tree,test_data,attr_vals_list,attr_names):

	if len(tree) == 1 and isinstance(tree[0],str):
		return tree[0]
	elif isinstance(tree,str):
		return tree

	attr_index = attr_names.index(tree[0])
	selected_path = attr_vals_list[attr_index].index(test_data[attr_index])

	return test_tree_helper(tree[selected_path+1],test_data,attr_vals_list,attr_names)



def test_tree(tree,test_data,attr_vals_list,attr_names):
	accuracy = 0
	for i in range(len(test_data)):
		if test_tree_helper(tree,test_data[i][:-1],attr_vals_list,attr_names) == test_data[i][-1]:
			accuracy += 1
	accuracy /= len(test_data)
	return accuracy

def chi_squere_hyp(data,attr_index,attr_vals_list):
	[chi,df] = chi_squared_test(data,attr_index,attr_vals_list)
	result = False
	if df != 0:
		if Distribution_Table[df-1][4] > chi:
			result = True
	return result


def find_label(tree,labels):
	l = [0]*len(labels)
	if tree in labels:
		l[labels.index(tree)] += 1
		return l
	for item in tree:
		l = [sum(x) for x in zip(l,find_label(item,labels))]
	return l

def main():
	
	with open ( 'hw3_data/dt/data.pkl', 'rb' ) as f :
		train_data , test_data , attr_vals_list , attr_names = pickle . load ( f )
	
	#Information Gain
	
	ig_train_backup = train_data[:]
	ig_attr_vals_backup = attr_vals_list[:]
	ig_attr_names_backup = attr_names[:]
	tree = dec_ig(ig_train_backup,ig_attr_vals_backup,ig_attr_names_backup)
	dot = Digraph()
	draw_backup = tree[:]
	ig_attr_vals_backup = attr_vals_list[:]
	ig_attr_names_backup = attr_names
	drawer(draw_backup,'1',dot,ig_attr_vals_backup,ig_attr_names_backup)
	dot.render('Information_Gain_Decision_Tree')
	ig_test_backup = test_data[:]
	print("Accuracy of Information Gain Decision Tree is: %",round(test_tree(tree,ig_test_backup,ig_attr_vals_backup,ig_attr_names_backup)*100,2))
	#Gain Ratio 
	ig_train_backup = train_data[:]
	ig_attr_vals_backup = attr_vals_list[:]
	ig_attr_names_backup = attr_names[:]
	tree = dec_gr(ig_train_backup,ig_attr_vals_backup,ig_attr_names_backup)
	dot = Digraph()
	draw_backup = tree[:]
	ig_attr_vals_backup = attr_vals_list[:]
	ig_attr_names_backup = attr_names
	drawer(draw_backup,'1',dot,ig_attr_vals_backup,ig_attr_names_backup)
	dot.render('Gain_Ratio_Decision_Tree')
	ig_test_backup = test_data[:]
	print("Accuracy of Gain Ratio Decision Tree is: %",round(test_tree(tree,ig_test_backup,ig_attr_vals_backup,ig_attr_names_backup)*100,2))
	#Average Gini Index
	ig_train_backup = train_data[:]
	ig_attr_vals_backup = attr_vals_list[:]
	ig_attr_names_backup = attr_names[:]
	tree = dec_gi(ig_train_backup,ig_attr_vals_backup,ig_attr_names_backup)
	dot = Digraph()
	draw_backup = tree[:]
	ig_attr_vals_backup = attr_vals_list[:]
	ig_attr_names_backup = attr_names
	drawer(draw_backup,'1',dot,ig_attr_vals_backup,ig_attr_names_backup)
	dot.render('Average_Gini_Index_Decision_Tree')
	ig_test_backup = test_data[:]
	print("Accuracy of Average Gini Index Decision Tree is: %",round(test_tree(tree,ig_test_backup,ig_attr_vals_backup,ig_attr_names_backup)*100,2))
	
	#Gain Ratio with Chi-Squared
	ig_train_backup = train_data[:]
	ig_attr_vals_backup = attr_vals_list[:]
	ig_attr_names_backup = attr_names[:]
	tree = dec_gr_chi(ig_train_backup,ig_attr_vals_backup,ig_attr_names_backup)
	dot = Digraph()
	draw_backup = tree[:]
	ig_attr_vals_backup = attr_vals_list[:]
	ig_attr_names_backup = attr_names
	drawer(draw_backup,'1',dot,ig_attr_vals_backup,ig_attr_names_backup)
	dot.render('Gain_Ratio_Decision_Chi_Squearred_Tree')
	ig_test_backup = test_data[:]
	print("Accuracy of Gain Ratio Decision Tree with Chi-Squared Pre-Prunning is: %",round(test_tree(tree,ig_test_backup,ig_attr_vals_backup,ig_attr_names_backup)*100,2))

	#Gain Ratio with Reduced Error

if __name__ == '__main__':
	main()

