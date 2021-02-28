import numpy as np
import matplotlib.pyplot as plt


def distance_calculator(p1,p2):
	distance = np.sqrt(np.sum((p1-p2)*(p1-p2))) # Euclidean formula in 2 dimension
	return distance

#distance function for non-numpy arrays
def distance_list(p1,p2): 
	p1 = np.array(p1)
	p2 = np.array(p2)
	distance = np.sqrt(np.sum((p1-p2)*(p1-p2))) # Euclidean formula in 2 dimension
	return distance

def distance_closest_points(cluster_x,clusters):
	distance = 99999 # max value
	for c_point in clusters:
		for x_point in cluster_x:
			dist = distance_calculator(x_point,c_point)
			if dist < distance:
				distance = dist
	return distance


#Applying Single linkage criterion method
def singe_linkage(clusters,k):
	while len(clusters) != k:
		distance = 99999 # max value 
		index = [-1,-1]
		#Finds appropriate closest cluster for cluster[0]
		for i in range(len(clusters)):
			for j in range(len(clusters)):
				if i < j:
					dist = distance_closest_points(clusters[i],clusters[j])
					if dist < distance:
						distance = dist
						index = [i,j]
		i = index[0]
		j = index[1]
		clusters[i] = clusters[i]+clusters[j]
		clusters.pop(j)

	return clusters

#Finding maximum distance between two cluster
def distance_farest_points(cluster_x,clusters):
	distance = -1 # max value
	for c_point in clusters:
		for x_point in cluster_x:
			dist = distance_calculator(x_point,c_point)
			if dist > distance:
				distance = dist
	return distance

#Applying Complete Linkage Criterion method
def complete_linkage(clusters,k):
	while len(clusters) != k:
		distance = 99999 # max value 
		index = [-1,-1]
		#Finds appropriate closest cluster for cluster[0]
		for i in range(len(clusters)):
			for j in range(len(clusters)):
				if i < j: # To prevent same cluster's faced twice
					dist = distance_farest_points(clusters[i],clusters[j])
					if dist < distance:
						distance = dist
						index = [i,j]
		i = index[0]
		j = index[1]
		clusters[i] = clusters[i]+clusters[j]
		clusters.pop(j)

	return clusters

#Finding average distance between two cluster
def average_distance(cluster_x,clusters):
	distance = 0 # max value
	for c_point in clusters:
		for x_point in cluster_x:
			dist = distance_calculator(x_point,c_point)
			distance += dist
	return distance/(len(cluster_x)+len(clusters))	

#Applying Average Linkage Criterion method
def average_linkage(clusters,k):
	while len(clusters) != k:
		distance = 99999 # max value 
		index = [-1,-1]
		#Finds appropriate closest cluster for cluster[0]
		for i in range(len(clusters)):
			for j in range(len(clusters)):
				if i < j: # To prevent same cluster's faced twice
					dist = average_distance(clusters[i],clusters[j])
					if dist < distance:
						distance = dist
						index = [i,j]
		i = index[0]
		j = index[1]
		clusters[i] = clusters[i]+clusters[j]
		clusters.pop(j)

	return clusters

def centroid_helper(cluster_x,clusters):

	centroid_x = [0,0]
	centroid_c = [0,0]
	for points in cluster_x:
		centroid_x[0] += points[0]
		centroid_x[1] += points[1]
	length = len(cluster_x)
	centroid_x[0] = centroid_x[0]/length
	centroid_x[1] = centroid_x[1]/length
	for points in clusters:
		centroid_c[0] += points[0]
		centroid_c[1] += points[1]
	length = len(clusters)
	centroid_c[0] = centroid_c[0]/length
	centroid_c[1] = centroid_c[1]/length
	return distance_list(centroid_x,centroid_c)

#Applying Centroid Linkage Criterion method
def centroid(clusters,k):
	while len(clusters) != k:
		distance = 99999 # max value 
		index = [-1,-1]
		#Finds appropriate closest cluster for cluster[0]
		for i in range(len(clusters)):
			for j in range(len(clusters)):
				if i < j: # To prevent same cluster's faced twice
					dist = centroid_helper(clusters[i],clusters[j])
					if dist < distance:
						distance = dist
						index = [i,j]
		i = index[0]
		j = index[1]
		clusters[i] = clusters[i]+clusters[j]
		clusters.pop(j)

	return clusters

#Turns each data to a cluster
def agglomerative_division(data):
	clusters = [[]]
	for point in data:
		clusters.append([point])
	return clusters[1:]


def plotting_k_2(cluster,linkage):
	cluster_1_x = []
	cluster_1_y = []
	for i in range(len(cluster[0])):
		cluster_1_x.append(cluster[0][i][0])
		cluster_1_y.append(cluster[0][i][1])

	cluster_2_x = []
	cluster_2_y = []
	for i in range(len(cluster[1])):
		cluster_2_x.append(cluster[1][i][0])
		cluster_2_y.append(cluster[1][i][1])
	if linkage == 1:
		plt.title('Single Linkage Criterion')
	if linkage == 2:
		plt.title('Complete Linkage Criterion')
	if linkage == 3:
		plt.title('Average Linkage Criterion')
	if linkage == 4:
		plt.title('Centroid Criterion')
	plt.plot(cluster_1_x,cluster_1_y,'ro')
	plt.plot(cluster_2_x,cluster_2_y,'bo')
	plt.show()


def plotting_k_4(cluster,linkage):
	cluster_1_x = []
	cluster_1_y = []
	for i in range(len(cluster[0])):
		cluster_1_x.append(cluster[0][i][0])
		cluster_1_y.append(cluster[0][i][1])

	cluster_2_x = []
	cluster_2_y = []
	for i in range(len(cluster[1])):
		cluster_2_x.append(cluster[1][i][0])
		cluster_2_y.append(cluster[1][i][1])

	cluster_3_x = []
	cluster_3_y = []
	for i in range(len(cluster[2])):
		cluster_3_x.append(cluster[2][i][0])
		cluster_3_y.append(cluster[2][i][1])

	cluster_4_x = []
	cluster_4_y = []
	for i in range(len(cluster[3])):
		cluster_4_x.append(cluster[3][i][0])
		cluster_4_y.append(cluster[3][i][1])

	plt.plot(cluster_1_x,cluster_1_y,'ro')
	plt.plot(cluster_2_x,cluster_2_y,'bo')
	plt.plot(cluster_3_x,cluster_3_y,'mo')
	plt.plot(cluster_4_x,cluster_4_y,'go')
	if linkage == 1:
		plt.title('Single Linkage Criterion')
	if linkage == 2:
		plt.title('Complete Linkage Criterion')
	if linkage == 3:
		plt.title('Average Linkage Criterion')
	if linkage == 4:
		plt.title('Centroid Criterion')
	plt.show()

#Try all criterion types for data with given k value
def hac(data,k):
	print("Criterions applying")
	clusters = agglomerative_division(data)
	single_cluster = singe_linkage(clusters,k)
	clusters = agglomerative_division(data)
	complete_cluster = complete_linkage(clusters,k)
	clusters = agglomerative_division(data)
	average_cluster = average_linkage(clusters,k)
	clusters = agglomerative_division(data)
	centroid_cluster = centroid(clusters,k)
	if k == 2:
		plotting_k_2(single_cluster,1)
		plotting_k_2(complete_cluster,2)
		plotting_k_2(average_cluster,3)
		plotting_k_2(centroid_cluster,4)
	if k == 4:
		plotting_k_4(single_cluster,1)
		plotting_k_4(complete_cluster,2)
		plotting_k_4(average_cluster,3)
		plotting_k_4(centroid_cluster,4)

def main():
	
	data1 = np.load('hw2_data/hac/data1.npy')
	print("DATA 1")
	hac(data1,2)
	data2 = np.load('hw2_data/hac/data2.npy')
	print("DATA 2")
	hac(data2,2)
	data3 = np.load('hw2_data/hac/data3.npy')
	print("DATA 3")
	hac(data3,2)
	data4 = np.load('hw2_data/hac/data4.npy')
	print("DATA 4")
	hac(data4,4)

if __name__ == "__main__":
	main()