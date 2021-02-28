import numpy as np
import matplotlib.pyplot as plt
import timeit

def distance_calculator(p1,p2):
	distance = np.sqrt(np.sum((p1-p2)*(p1-p2))) # Euclidean formula in 2 dimension
	return distance


#distance function for non-numpy arrays
def distance_list(p1,p2): 
	p1 = np.array(p1)
	p2 = np.array(p2)
	distance = np.sqrt(np.sum((p1-p2)*(p1-p2))) # Euclidean formula in 2 dimension
	return distance

def random_centers(cluster,k):
	l = [[]]*1
	for i in range(k):
		#In case of "empty" cluster problem, maximum and minimum values has an error rate which is 0.1
		max_x = max(cluster[:,0])-0.1
		min_x = min(cluster[:,0])+0.1
		random_x = np.random.uniform(min_x,max_x)
		max_y = max(cluster[:,1])-0.1
		min_y = min(cluster[:,1])+0.1
		random_y = np.random.uniform(min_y,max_y)
		# Round x and y to 8 decimal point (which is decimal #s of inputs) to prevent possible failures
		l.append([round(random_x,8),round(random_y,8)])
	return l[1:]


def closest_center(point,centers):
	#Find nearest centroid to given point
	min_distance = 999999 # reference max value
	index = -1
	for i in range(len(centers)):
		distance = distance_calculator(point,centers[i])
		if distance < min_distance:
			min_distance = distance
			index = i
	return index

def mean_calculators(data,centers,k):
	#Find closest center for each data point
	clusters = []
	for i in range(k):
		clusters.append([[-99],[-99]])

	for i in range(len(data)):
		index = closest_center(data[i],centers)
		clusters[index][0].append(data[i][0])
		clusters[index][1].append(data[i][1])

	for i in range(k):
		clusters[i][0] = clusters[i][0][1:]
		clusters[i][1] = clusters[i][1][1:]

	return clusters

def centroid_updates(clusters,k,centers):
	for i in range(k):
		if len(clusters[i][0]) != 0 and len(clusters[i][1]) != 0: #To prevent empty cluster failures
			x_mean = sum(clusters[i][0])/len(clusters[i][0])
			y_mean = sum(clusters[i][1])/len(clusters[i][1])
			centers[i] = [x_mean,y_mean]
	return centers 


def k_mean_clustering(data,k,bool_plot):
	centers = random_centers(data,k)
	#First clustering with respect to random centroids
	clusters = mean_calculators(data,centers,k)
	centers = centroid_updates(clusters,k,centers)
	#Iteration part
	while True:
		new_clusters = mean_calculators(data,centers,k)
		if(clusters == new_clusters):
			break
		else:
			clusters = new_clusters
			centers = centroid_updates(clusters,k,centers)
	#If bool_plt is True, plot K-mean clusters
	if(bool_plot):
		colors = ['blue','magenta','green','red','yellow','black']
		for i in range(k):
			plt.plot(clusters[i][0],clusters[i][1],color = colors[i], marker = 'o')	
		for i in range(k):
			plt.plot(centers[i][0],centers[i][1],'black', marker = "s")
		plt.title('Cluster')
		plt.xlabel('x')
		plt.ylabel('y')
		plt.show()
	
	return [centers,clusters]




def objection_function(result,k):
	#Finding objection function value with summing each clusters centroid-data distance
	objection_value = 0
	centers = result[0]
	clusters = result[1]
	for i in range(k):
		center_point = centers[i]
		for j in range(len(clusters[i][0])):
			point = [clusters[i][0][j],clusters[i][1][j]]
			objection_value += distance_list(point,center_point)
	return objection_value


def elbow_testing(cluster):
	objection_value_list = []
	objection_value = 0
	for k in range(1,7): # I selected a range between 1 to 6  for k due to given input data shapes and my computer's performance issues
		for times in range(10): # 10 times testing
			result = k_mean_clustering(cluster,k,False)
			objection_value += objection_function(result,k)	
		objection_value_list.append(objection_value/10) # Division with 10 due to "10" times testing
		objection_value = 0
	
	print(objection_value_list)
	k = [1,2,3,4,5,6]
	plt.plot(k,objection_value_list,linestyle = 'dashed')
	plt.xlabel('k')
	plt.ylabel('Objection Value')
	plt.title('Elbow Plot for Optimal k')
	plt.show()




def main():
	#Elbow testing and plot of K-mean with selected k value
	#CLUSTERING1
	print("Cluster_1")
	cluster_1 = np.load('hw2_data/kmeans/clustering1.npy')
	print("Elbow applying...")
	elbow_testing(cluster_1)
	print("Selected k value is 2")
	print("Result of Clustering is")
	k_mean_clustering(cluster_1,2,True)
	#-----------------------------------------------------
	#CLUSTERING2
	print("Cluster_2")
	cluster_2 = np.load('hw2_data/kmeans/clustering2.npy')
	print("Elbow applying...")
	elbow_testing(cluster_2)
	print("Selected k value is 3")
	print("Result of Clustering is")
	k_mean_clustering(cluster_2,3,True)
	#-----------------------------------------------------
	#CLUSTERING3
	print("Cluster_3")
	cluster_3 = np.load('hw2_data/kmeans/clustering3.npy')
	print("Elbow applying...")
	elbow_testing(cluster_3)
	print("Selected k value is 4")
	print("Result of Clustering is")
	k_mean_clustering(cluster_3,4,True)
	#-----------------------------------------------------
	#CLUSTERING4
	print("Cluster_4")
	cluster_4 = np.load('hw2_data/kmeans/clustering4.npy')
	print("Elbow applying...")
	elbow_testing(cluster_4)
	print("Selected k value is 5")
	print("Result of Clustering is")
	k_mean_clustering(cluster_4,5,True)
	#-----------------------------------------------------



if __name__ == '__main__':
	main()