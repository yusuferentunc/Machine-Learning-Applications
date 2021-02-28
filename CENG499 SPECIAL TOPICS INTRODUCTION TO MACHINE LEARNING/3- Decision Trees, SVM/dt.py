import math # To calculate logarithm


def divide(data, attr_index, attr_vals_list):
    #Creating a list with length of selected attribute
    result = []
    for i in range(len(attr_vals_list[attr_index])):
        result.append([attr_vals_list[attr_index][i]])
    #Passing data to result list with specified attribute
    for item in data:
        index = attr_vals_list[attr_index].index(item[attr_index])
        result[index].append(item)
    #Deleting unnecessary variables that given at creating stage of list
    for i in range(len(attr_vals_list[attr_index])):
        result[i].pop(0)

    return result


def entropy(data, attr_vals_list):    
    occur_list = [0]*len(attr_vals_list[-1])
    #Updating occurance list
    for item in data:
        index = attr_vals_list[-1].index(item[-1])
        occur_list[index] += 1
    result = 0
    data_size = len(data)
    #Calculating entropy with occurance list
    for value in occur_list:
        if value != 0:
            result += (value/data_size)*math.log(value/data_size,2)

    return -result



def info_gain(data, attr_index, attr_vals_list):
    total_entropy = entropy(data,attr_vals_list)
    buckets = divide(data,attr_index,attr_vals_list)
    division_entropy = 0
    data_size = len(data)
    for item in buckets:
        division_entropy += (len(item)/data_size)*entropy(item,attr_vals_list)
    result = total_entropy - division_entropy

    return [result,buckets]


def gain_ratio(data, attr_index, attr_vals_list):
    total_entropy = entropy(data,attr_vals_list)
    buckets = divide(data,attr_index,attr_vals_list)
    division_entropy = 0
    data_size = len(data)
    intrinsic_value = 0
    information_gain = info_gain(data,attr_index,attr_vals_list)[0]
    for item in buckets:
        value = len(item)/data_size
        if value != 0:
            intrinsic_value += (value)*math.log(value,2)
    if intrinsic_value == 0:
        return [-1,buckets]
    result = information_gain/intrinsic_value
    return [-result,buckets]



def gini(data, attr_vals_list):
    occur_list = [0]*len(attr_vals_list[-1])
    #Updating occurance list
    for item in data:
        index = attr_vals_list[-1].index(item[-1])
        occur_list[index] += 1
    gini_index = 0
    data_size = len(data)
    #Calculating gini index with occurance list
    for value in occur_list:
        if value != 0:
            gini_index += (value/data_size)**2

    return 1-gini_index



def avg_gini_index(data, attr_index, attr_vals_list):
    buckets = divide(data,attr_index,attr_vals_list)
    average_gini = 0
    data_size = len(data)
    for item in buckets:
        average_gini += (len(item)/data_size)*gini(item,attr_vals_list)

    return [average_gini,buckets]
    


def chi_squared_test(data, attr_index, attr_vals_list):
    #Creating a list with length of selected attribute
    result = []
    for i in range(len(attr_vals_list[attr_index])+1):
        result.append([0])
        for j in range(len(attr_vals_list[-1])):
            result[i].append(0)
    #Matrix creation for test calculatin
    for item in data:
        col = attr_vals_list[-1].index(item[-1])
        row = attr_vals_list[attr_index].index(item[attr_index])
        result[row][col] += 1
        result[row][-1] += 1 #n_i
        result[-1][col] += 1 #n_j
        result[-1][-1] += 1  #n
    
    for i in range(len(result)-1):
        if result[i][-1] == 0:
            result.pop(i)
    k = len(result)-1
    m = len(result[0])-1
    for i in range(len(result[-1])-1):
        if result[-1][i] == 0:
            m -= 1
    chi = 0
    for i in range(len(result)-1):
        for j in range(len(result[0])-1):
            if result[-1][j] != 0 and result[i][-1] != 0 :
                obs = result[i][j]
                exp = (result[i][-1]*result[-1][j])/(result[-1][-1])
                chi += ((obs-exp)**2)/(exp)

    return [chi,(k-1)*(m-1)]

