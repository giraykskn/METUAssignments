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
    alphas = []
    for l in A:
        alphas.append([])
    for T in range(len(O)):
        for N in range(len(A)):
            if T == 0:
                prob = pi[N]
                prob *= B[N][O[T]]
                alphas[N].append(prob)
            else:
                prob = 0
                for N2 in range(len(A)):
                    prob += alphas[N2][T-1] * A[N2][N] * B[N][O[T]]
                alphas[N].append(prob)
    probObs = 0
    for l in alphas:
        probObs += l[-1]
    return probObs, np.array(alphas)


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
    deltas = []
    pointers = []
    path = []
    for l in A:
        deltas.append([])
        pointers.append([])
    for T in range(len(O)):
        for N in range(len(A)):
            if T == 0:
                prob = pi[N]
                prob *= B[N][O[T]]
                deltas[N].append(prob)
            else:
                maxProb = 0
                pointer = -1
                for N2 in range(len(A)):
                    prob = deltas[N2][T-1] * A[N2][N] * B[N][O[T]]
                    if prob > maxProb:
                        maxProb = prob
                        pointer = N2
                deltas[N].append(maxProb)
                pointers[N].append(pointer)
    finals = []
    for l in deltas:
        finals.append(l[-1])
    for T in range(len(O)):
        if T == 0:
            path.append(finals.index(max(finals)))
        elif T == len(O) - 1:
            path.append(pointers[path[T - 1]][0])
        else:
            path.append(pointers[path[T - 1]][-T])
    return np.array(path[::-1]), np.array(deltas)