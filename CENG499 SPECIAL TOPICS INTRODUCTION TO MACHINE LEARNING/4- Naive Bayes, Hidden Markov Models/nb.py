import numpy as np

def vocabulary(data):
    """
    Creates the vocabulary from the data.
    :param data: List of lists, every list inside it contains words in that sentence.
                 len(data) is the number of examples in the data.
    :return: Set of words in the data
    """
    words = []
    for l in data:
        for item in l:
            if item not in words:
                words += [item]
    return set(words)


def train(train_data, train_labels, vocab):
    """
    Estimates the probability of a specific word given class label using additive smoothing with smoothing constant 1.
    :param train_data: List of lists, every list inside it contains words in that sentence.
                       len(train_data) is the number of examples in the training data.
    :param train_labels: List of class names. len(train_labels) is the number of examples in the training data.
    :param vocab: Set of words in the training set.
    :return: theta, pi. theta is a dictionary of dictionaries. At the first level, the keys are the class names. At the
             second level, the keys are all of the words in vocab and the values are their estimated probabilities.
             pi is a dictionary. Its keys are class names and values are their probabilities.
    """
    pi = dict([])
    theta = dict([])
    length = len(train_labels)
    for label in train_labels:
        if label in pi:
            pi[label] += 1/length
        else:
            pi[label] = 1/length
            theta[label] = dict.fromkeys(vocab,1)
            theta[label]['length'] = len(vocab)

    for i in range(len(train_data)):
        label = train_labels[i]
        for item in train_data[i]:
            theta[label][item] += 1
            theta[label]['length'] += 1
    for label in theta:
        for val in theta[label]:
            theta[label][val] /= theta[label]['length']
        del theta[label]['length']
    return theta, pi


def test(theta, pi, vocab, test_data):
    """
    Calculates the scores of a test data given a class for each class. Skips the words that are not occurring in the
    vocabulary.
    :param theta: A dictionary of dictionaries. At the first level, the keys are the class names. At the second level,
                  the keys are all of the words in vocab and the values are their estimated probabilities.
    :param pi: A dictionary. Its keys are class names and values are their probabilities.
    :param vocab: Set of words in the training set.
    :param test_data: List of lists, every list inside it contains words in that sentence.
                      len(test_data) is the number of examples in the test data.
    :return: scores, list of lists. len(scores) is the number of examples in the test set. Every inner list contains
             tuples where the first element is the score and the second element is the class name.
    """
    result_dict = []

    for i in range(len(test_data)):
        result_dict += [[]]
        for label in theta:
            result = 0
            for word in test_data[i]:
                if word in theta[label]:
                    result += np.log(theta[label][word])
            result += np.log(pi[label])
            result_dict[i] += [(result,label)]
    return result_dict
