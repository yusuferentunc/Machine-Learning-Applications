import numpy as np
def forward(A, B, pi, O):
    """
    Calculates the probability of an observation sequence O given the model(A, B, pi).
    :param A: state transition probabilities (NxN)
    :param B: observation probabilites (NxM)
    :param pi: initial state probabilities (N)
    :param O: sequence of observations(T) where observations are just indices for the columns of B (0-indexed)
        N is the number of states,
        M is the number of possible observations, and
        T is the sequence length.
    :return: The probability of the observation sequence and the calculated alphas in the Trellis diagram with shape
             (N, T) which should be a numpy array.
    """
    alpha_result  = np.zeros((len(pi),len(O)))

    for i in range(len(pi)):
    	alpha_result[i][0] = pi[i]*B[i][O[0]]
    
    for j in range(1,len(O)):
        for i in range(len(pi)):
            for z in range(len(alpha_result)):
                alpha_result[i][j] += alpha_result[z][j-1]*A[z][i]*B[i][O[j]]
    result = 0
    for i in range(len(pi)):
    	result += alpha_result[i][-1]
    	
    return result,np.asarray(alpha_result)


def viterbi(A, B, pi, O):
    """
    Calculates the most likely state sequence given model(A, B, pi) and observation sequence.
    :param A: state transition probabilities (NxN)
    :param B: observation probabilites (NxM)
    :param pi: initial state probabilities(N)
    :param O: sequence of observations(T) where observations are just indices for the columns of B (0-indexed)
        N is the number of states,
        M is the number of possible observations, and
        T is the sequence length.
    :return: The most likely state sequence with shape (T,) and the calculated deltas in the Trellis diagram with shape
             (N, T). They should be numpy arrays.
    """
    delta_result = np.zeros((len(pi),len(O)))

    for i in range(len(pi)):
    	delta_result[i][0] = pi[i]*B[i][O[0]]
    for j in range(1,len(O)):
        for i in range(len(pi)):
            delta_result[i][j] = 0
            for z in range(len(delta_result)):
                temp = delta_result[z][j-1]*A[z][i]*B[i][O[j]]
                if delta_result[i][j] < temp: 
                    delta_result[i][j] = temp
    viterbi_result = []
    for i in range(len(O)):
        temp = -1 
        for j in range(len(pi)):
            if delta_result[j][i] > temp:
            	temp = delta_result[j][i]
            	index = j
        viterbi_result.append(index)

    return np.asarray(viterbi_result), np.asarray(delta_result)




