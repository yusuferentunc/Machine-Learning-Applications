import numpy as np
from nb import vocabulary, train, test

#Input Preparation
input_file = open("./hw4_data/news/train_data.txt", "r")
train_data = []
for l in input_file:
	line = l.strip()
	line = line.translate({ord(i): None for i in '.,():;[]‘!*'})
	line_list = line.split()
	train_data.append(line_list)
input_file.close()

input_file = open("./hw4_data/news/train_labels.txt", "r")
train_labels = []
for l in input_file:
	line = l.strip()
	line = line.translate({ord(i): None for i in '.,():;[]‘!*'})
	line_list = line.split()
	train_labels.append(line_list[0])
input_file.close()

input_file = open("./hw4_data/news/test_data.txt", "r")
test_data = []
for l in input_file:
	line = l.strip()
	line = line.translate({ord(i): None for i in '.,():;[]‘!*'})
	line_list = line.split()
	test_data.append(line_list)
input_file.close()

input_file = open("./hw4_data/news/test_labels.txt", "r")
test_labels = []
for l in input_file:
	line = l.strip()
	line = line.translate({ord(i): None for i in '.,():;[]‘!*'})
	line_list = line.split()
	test_labels.append(line_list[0])
input_file.close()
#--------------------------------------------------------------------------------

#Naive Bayes Model 
print("Vocabulary is creating...")
vocab = vocabulary(train_data)

print("Theta and pi values are calculating...")
theta, pi = train(train_data, train_labels, vocab)

print("Scores are calculating...")
scores = test(theta, pi, vocab, test_data)

print("Accuracy is calculating...")
accuracy = 0
for i in range(len(test_data)):
	pred = dict(scores[i])
	if test_labels[i] == pred[max(pred)]:
		accuracy += 1

print("Accuracy of Naive Bayes Model is : ",round(accuracy/len(test_data),2))
#--------------------------------------------------------------------------------
