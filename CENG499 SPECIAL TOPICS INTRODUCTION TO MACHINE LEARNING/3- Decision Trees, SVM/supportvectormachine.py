import numpy as np
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
from draw import draw_svm




def svm1():
	train_data = np.load('hw3_data/linsep/train_data.npy')
	train_labels = np.load('hw3_data/linsep/train_labels.npy')
	c_list = [0.01,0.1,1,10,100]
	for i in range(len(c_list)):
		clf = svm.SVC(kernel = 'linear',C = c_list[i])
		clf.fit(train_data,train_labels)
		draw_svm(clf,train_data,train_labels,-3,3,-3,3,'svm1_'+str(i))

def svm2():
	train_data = np.load('hw3_data/nonlinsep/train_data.npy')
	train_labels = np.load('hw3_data/nonlinsep/train_labels.npy')
	k_list = ['linear','rbf','poly','sigmoid']
	for k in k_list:
		clf = svm.SVC(kernel = k)
		clf.fit(train_data,train_labels)
		draw_svm(clf,train_data,train_labels,-3,3,-3,3,'svm1_'+k)

def svm3():
	train_data = np.load('hw3_data/catdog/train_data.npy')
	train_labels = np.load('hw3_data/catdog/train_labels.npy')
	test_data = np.load('hw3_data/catdog/test_data.npy')
	test_labels = np.load('hw3_data/catdog/test_labels.npy')
	train_data =train_data/255
	test_data=test_data/255
	svc = svm.SVC()
	print("Linear Kernel Grid Search")
	params = {'kernel':['linear'],'C':[0.01,0.1,1,10,100]}
	clf = GridSearchCV(svc,params,cv = KFold(n_splits = 5))
	clf.fit(train_data,train_labels)
	print(clf.cv_results_)
	print("----------------------------------------------")
	print("RBF Kernel Grid Search")
	params = {'kernel':['rbf'],'C':[0.01,0.1,1,10,100],'gamma':[0.00001,0.0001,0.001,0.01,0.1,1]}
	clf = GridSearchCV(svc,params,cv = KFold(n_splits = 5))
	clf.fit(train_data,train_labels)
	print(clf.cv_results_)
	print("----------------------------------------------")
	print("Polynomial Kernel Grid Search")
	params = {'kernel':['poly'],'C':[0.01,0.1,1,10,100],'gamma':[0.00001,0.0001,0.001,0.01,0.1,1]}
	clf = GridSearchCV(svc,params,cv = KFold(n_splits = 5))
	clf.fit(train_data,train_labels)
	print(clf.cv_results_)
	print("----------------------------------------------")
	print("Sigmoid Kernel Grid Search")
	params = {'kernel':['sigmoid'],'C':[0.01,0.1,1,10,100],'gamma':[0.00001,0.0001,0.001,0.01,0.1,1]}
	clf = GridSearchCV(svc,params,cv = KFold(n_splits = 5))
	clf.fit(train_data,train_labels)
	print(clf.cv_results_)
	#Selected hyperparameters are RBF kernel with 1 C and 1 Gamma
	svc = svm.SVC(kernel = 'rbf',C = 1, gamma = 1)
	svc.fit(train_data,train_labels)
	result_labels = svc.predict(test_data)
	accuracy = (np.sum(result_labels == test_labels))/len(test_labels)
	print("Accuracy of model at part 2 is",accuracy)

	
def svm4():
	train_data = np.load('hw3_data/catdogimba/train_data.npy')
	train_labels = np.load('hw3_data/catdogimba/train_labels.npy')
	test_data = np.load('hw3_data/catdogimba/test_data.npy')
	test_labels = np.load('hw3_data/catdogimba/test_labels.npy')
	train_data =train_data/255
	test_data=test_data/255
	#Initial
	clf = svm.SVC(kernel = 'rbf',C = 1)
	clf.fit(train_data,train_labels)
	accuracy = 0
	result_labels = clf.predict(test_data)
	accuracy = (np.sum(result_labels == test_labels))/len(test_labels)
	print("Accuracy of model without handling the imbalance problem is",accuracy)
	print("Confusion Matrix of model without handling the imbalance problem is")
	print(confusion_matrix(test_labels,result_labels))
	
	#OverSample
	sum_0 = sum(train_labels == 0)
	sum_1 = sum(train_labels == 1)
	if sum_0 > sum_1:
		l = np.random.choice(np.where(train_labels == 1)[0],sum_0-sum_1)
	else:
		l = np.random.choice(np.where(train_labels == 0)[0],sum_1-sum_0)
	
	train_data = np.append(train_data,train_data[l],axis = 0)
	train_labels = np.append(train_labels,train_labels[l],axis = 0)
	clf = svm.SVC(kernel = 'rbf',C = 1)
	clf.fit(train_data,train_labels)
	accuracy = 0
	result_labels = clf.predict(test_data)
	accuracy = (np.sum(result_labels == test_labels))/len(test_labels)
	print("Accuracy of model with oversampling is",accuracy)
	print("Confusion Matrix of model with oversampling is")
	print(confusion_matrix(test_labels,result_labels))
	
	#Recovery
	train_data = np.load('hw3_data/catdogimba/train_data.npy')
	train_labels = np.load('hw3_data/catdogimba/train_labels.npy')
	test_data = np.load('hw3_data/catdogimba/test_data.npy')
	test_labels = np.load('hw3_data/catdogimba/test_labels.npy')
	train_data =train_data/255
	test_data=test_data/255

	#UnderSample
	sum_0 = sum(train_labels == 0)
	sum_1 = sum(train_labels == 1)
	if sum_0 > sum_1:
		l = np.random.choice(np.where(train_labels == 0)[0],sum_0-sum_1)
	else:
		l = np.random.choice(np.where(train_labels == 1)[0],sum_1-sum_0)
	
	train_data = np.delete(train_data,l,axis = 0)
	train_labels = np.delete(train_labels,l,axis = 0)
	clf = svm.SVC(kernel = 'rbf',C = 1)
	clf.fit(train_data,train_labels)
	accuracy = 0
	result_labels = clf.predict(test_data)
	accuracy = (np.sum(result_labels == test_labels))/len(test_labels)
	print("Accuracy of model with undersampling is",accuracy)
	print("Confusion Matrix of model with undersampling is")
	print(confusion_matrix(test_labels,result_labels))

	#Recovery
	train_data = np.load('hw3_data/catdogimba/train_data.npy')
	train_labels = np.load('hw3_data/catdogimba/train_labels.npy')
	test_data = np.load('hw3_data/catdogimba/test_data.npy')
	test_labels = np.load('hw3_data/catdogimba/test_labels.npy')
	train_data =train_data/255
	test_data=test_data/255

	#Balanced
	clf = svm.SVC(kernel = 'rbf',C = 1, class_weight = 'balanced')
	clf.fit(train_data,train_labels)
	accuracy = 0
	result_labels = clf.predict(test_data)
	accuracy = (np.sum(result_labels == test_labels))/len(test_labels)
	print("Accuracy of model with balanced class weight is",accuracy)
	print("Confusion Matrix of model with balanced class weight is")
	print(confusion_matrix(test_labels,result_labels))
	

def main():
	#svm1()
	#svm2()
	#svm3()
	svm4()

if __name__ == '__main__':
	main()