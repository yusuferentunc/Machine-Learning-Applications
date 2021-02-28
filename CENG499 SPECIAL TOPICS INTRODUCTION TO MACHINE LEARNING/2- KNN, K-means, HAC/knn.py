import numpy as np
import matplotlib.pyplot as plt



def distance_calculator(p1,p2):
	distance = np.sqrt(np.sum((p1-p2)*(p1-p2))) # Euclidean formula in 4 dimension
	return distance

def neighbor_selection(neighbor,candidate,distance,k):
	if k > len(neighbor[0]): # Neighbor list's length is less than k value -> get canditate directly to neighbor list
		neighbor[0].append(candidate) # candidate index
		neighbor[1].append(distance)
	else: 
		index = neighbor[1].index(max(neighbor[1]))
		neighbor[0][index] = candidate
		neighbor[1][index] = distance
	return neighbor


def result_calculator(neighbor,train_labels):
	#Since our labels are not too large numbers, we prefer to take their values as an index in count list
	count = [[train_labels[neighbor[0][0]]],[1]]
	for i in range(1,len(neighbor[0])):
		label = train_labels[neighbor[0][i]]
		if label not in count[0]:
			count[0].append(label)
			count[1].append(1)
		else:
			index = count[0].index(label)
			count[1][index] += 1
	return count


def knn_classification(k,train_data,train_labels,input):
	# To initialize 2 dimension neighbor list first element of train_data handle outside of loop
	distance = distance_calculator(input,train_data[0])
	neighbor = [[0],[distance]] # 0 represents index number of train data
	for i in range(1,len(train_data)):
		distance = distance_calculator(input,train_data[i])
		neighbor = neighbor_selection(neighbor,i,distance,k)
	result_list = result_calculator(neighbor,train_labels)
	return result_list[0][result_list[1].index(max(result_list[1]))]


def data_preperation(data_split,index):
	#Spliting data to 10 K fold where each fold has 25 data
	temp = [[-1,-1,-1]]
	for i in range(10):
		if i != index:
			temp = np.append(temp,data_split[i], axis = 0)
	return temp[1:]

def label_preperation(label_split,index):
	#Splitting label to 10 K fold where each fold has 25 label
	temp = [-1]
	for i in range(10):
		if i != index:
			temp = np.append(temp,label_split[i], axis = 0)
	return temp[1:]

def test_execution(data_split,label_split,k):
	#Testing KNN with given k value
	accuracy_sum = 0
	for i in range(10):
		data = data_preperation(data_split,i)
		label = label_preperation(label_split,i)
		for j in range(len(data_split[i])):
			if knn_classification(k,data,label,data_split[i][j]) == label_split[i][j]:
				accuracy_sum += 1
	return accuracy_sum

def k_fold_cross_validation(train_data,train_label):
	total = np.c_[train_data,train_label]
	np.random.shuffle(total)
	data = total[:,:3]
	label = total[:,-1]
	data_split = np.split(data,10) # Since K fold is 10
	label_split = np.split(label,10)
	liste = []
	for k in range(1,200): # Cross validation testing between 1 to 200 k
		accuracy_sum = test_execution(data_split,label_split,k)
		liste.append(accuracy_sum/len(train_label))
	return liste

	"""
	Selected K = 5 ----- Accuracy = 0.76
	"""

def main():

	train_data = np.load('hw2_data/knn/train_data.npy')
	train_label = np.load('hw2_data/knn/train_labels.npy')
	test_data = np.load('hw2_data/knn/test_data.npy')
	test_label = np.load('hw2_data/knn/test_labels.npy')

	print("Cross Validation applying...")
	liste = k_fold_cross_validation(train_data,train_label)
	plt.figure()
	plt.plot(liste, color = 'red',marker = "." ,markerfacecolor = 'white', linestyle = 'dashed')
	plt.xlabel('k')
	plt.ylabel('Accuracy')
	plt.title('K-Nearest Neighbor Accuracy vs k Plot')
	plt.show()

	k = liste.index(max(liste))+1
	print("Selected k value is ",k)
	accuracy_sum = 0 
	for i in range(len(test_label)):
		if knn_classification(k,train_data,train_label,test_data[i]) == test_label[i]:
				accuracy_sum += 1
	print("Accuracy of Test Data Prediction is ",accuracy_sum/len(test_label))


if __name__ == '__main__':
	main()
