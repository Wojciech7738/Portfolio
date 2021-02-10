import numpy as np
import pandas as pd
import copy, sys, os.path

def Entropy_weights(performance_matrix, criteria, altern):
    ncrit = len(criteria) # Calculate length from Criteria list
    nalt = len(altern)
    sum = [0] * ncrit
    perf = copy.deepcopy(performance_matrix)
    # Calculate sum for each criteria
    for j in range(ncrit):
        for i in range(nalt):
            sum[j] += perf[i][j]

    # Normalize matrix
    for j in range(ncrit):
        for i in range(nalt):
            perf[i][j] /= sum[j]

    # Performance matrix multiplied by ln of each element (to calculate entropy)
    perf_log = copy.deepcopy(perf)
    for j in range(ncrit):
        for i in range(nalt):
            perf_log[i][j] *= np.log(perf_log[i][j])

    # -K
    K = -1 / np.log(nalt)

    # Calculate entropy
    sum = [0] * ncrit
    for j in range(ncrit):
        for i in range(nalt):
            sum[j] += perf_log[i][j]

    entr_sum = 0
    weights = [0] * ncrit
    for i in range(ncrit):
        weights[i] = sum[i] * K
        entr_sum += weights[i]

    # Finally calculate weights
    for i in range(ncrit):
        weights[i] = (1-weights[i]) / (ncrit-entr_sum)
    return weights, perf


def print_ranks(alternatives, ranks):
    for i in alternatives:
        print(i, end='\t')
    print("", end='\n')
    for i in ranks:
        print(i, end='\t')
    print("", end='\n')
    print()



class TOPSIS:
    def __init__(self, criteria, alternatives, weights, decision_matrix, benef):
        self.criteria = criteria
        self.weights = weights
        self.alternatives = alternatives
        self.decision_matrix = copy.deepcopy(decision_matrix)
        self.ncrit = len(criteria)
        self.nalt = len(alternatives)
        self.benef = benef
        self.PIS = []
        self.NIS = []
        self.Si_plus = []
        self.Si_minus = []

    def weightening(self):
        for j in range(self.ncrit):
            for i in range(self.nalt):
                self.decision_matrix[i][j] *= self.weights[j]
    def PIS_NIS(self):
        for j in range(self.ncrit):
            sum = []
            for i in range(self.nalt):
                sum.append(self.decision_matrix[i][j])
            if self.benef[j] == 0:
                self.PIS.append(min(sum))
                self.NIS.append(max(sum))
            else:
                self.PIS.append(max(sum))
                self.NIS.append(min(sum))
        # return PIS, NIS
    def Euclidean_distance(self):
        for i in range(self.nalt):
            sum1 = 0
            sum2 = 0
            for j in range(self.ncrit):
                sum1 += np.square(self.decision_matrix[i][j] - self.PIS[j])
                sum2 += np.square(self.decision_matrix[i][j] - self.NIS[j])
            self.Si_plus.append(np.sqrt(sum1))
            self.Si_minus.append(np.sqrt(sum2))
    def Performance_score_and_ranking(self):
        P = []
        for i in range(len(self.Si_minus)):
            P.append(self.Si_minus[i] / (self.Si_plus[i] + self.Si_minus[i]))
        K = sorted(range(len(P)), reverse=True, key=lambda k: P[k])
        for i in range(len(K)):
            K[i] += 1
        print('Ranking for TOPSIS:')
        print_ranks(self.alternatives, K)





class VIKOR:
    def __init__(self, criteria, alternatives, weights, decision_matrix, benef):
        self.criteria = criteria
        self.weights = weights
        self.alternatives = alternatives
        self.decision_matrix = copy.deepcopy(decision_matrix)
        self.ncrit = len(criteria)
        self.nalt = len(alternatives)
        self.benef = benef
        self.best = []
        self.worst = []
        self.S = []
        self.Q = []
        self.R = []

    def Best_worst(self):
        for j in range(self.ncrit):
            sum = []
            for i in range(self.nalt):
                sum.append(self.decision_matrix[i][j])
            if self.benef[j] == 0:
                self.best.append(min(sum))
                self.worst.append(max(sum))
            else:
                self.best.append(max(sum))
                self.worst.append(min(sum))

    def Weightening(self):
        for j in range(self.ncrit):
            for i in range(self.nalt):
                self.decision_matrix[i][j] = self.weights[j] * (self.best[j] - self.decision_matrix[i][j]) / (self.best[j] - self.worst[j])
        # Calculating Si
        for j in range(self.nalt):
            sum = 0
            Sum = []
            for i in range(self.ncrit):
                sum += self.decision_matrix[j][i]
                Sum.append(self.decision_matrix[j][i])
            self.S.append(sum)
            self.R.append(max(Sum))

    def SQR_and_ranking(self):
        S_star = min(self.S)
        S_dash = max(self.S)
        R_star = min(self.R)
        R_dash = max(self.R)
        ni = 0.5
        for i in range(len(self.S)):
            self.Q.append(ni * (self.S[i] - S_star)/(S_dash-S_star)+(1-ni)*(self.R[i]-R_star)/(R_dash-R_star))
        Ranks = sorted(range(len(self.Q)), key=lambda k: self.Q[k])
        for i in range(len(Ranks)):
            Ranks[i] += 1
        print('Ranking for VIKOR:')
        print_ranks(self.alternatives, Ranks)



# PROMETHEE II
class PROMETHEE:
    def __init__(self, criteria, alternatives, weights, decision_matrix, benef):
        self.criteria = criteria
        self.weights = weights
        self.alternatives = alternatives
        self.decision_matrix = copy.deepcopy(decision_matrix)
        self.ncrit = len(criteria)
        self.nalt = len(alternatives)
        self.benef = benef
        self.eval_matrix = []
        self.phi = []

    def start(self):
        self.normalization()
        self.eval_diff()
        self.pos_neg()
        return self.ranking()

    def normalization(self):
        # Calculate maximum and minimum for each criteria
        worst = []
        best = []
        for i in range(self.ncrit):
            sum = []
            for j in range(self.nalt):
                sum.append(self.decision_matrix[j][i])
            worst.append(min(sum))
            best.append(max(sum))
        # Normalize perf. table
        for i in range(self.ncrit):
            for j in range(self.nalt):
                if self.benef[i] == 0: # If non-beneficial
                    self.decision_matrix[j][i] = (best[i] - self.decision_matrix[j][i]) / (best[i] - worst[i])
                else:
                    self.decision_matrix[j][i] = (self.decision_matrix[j][i] - worst[i]) / (best[i] - worst[i])
        return self.decision_matrix

    def eval_diff(self):
        # Calculate evaluative differences
        for i in range(self.ncrit):
            vec = []
            for j in range(self.nalt):
                for k in range(self.nalt-1):
                    # if (self.nalt-1)*j != k:
                    vec.append(self.decision_matrix[j][i] - self.decision_matrix[k][i])
            if i == 0:
                self.eval_matrix = copy.deepcopy(vec)
            else:
                self.eval_matrix = np.vstack((self.eval_matrix, vec))
        self.eval_matrix = self.eval_matrix.T
        # Calculate preference function
        for i in range(self.ncrit):
            for j in range((self.nalt-1)*self.nalt): # ???
                if self.eval_matrix[j][i] < 0:
                    self.eval_matrix[j][i] = 0
                else:
                    self.eval_matrix[j][i] *= self.weights[i]
                    self.eval_matrix[j][i] /= sum(self.weights) # sum of weights should be equal to 1

    def pos_neg(self):
        #  Calculate positiv (phi+) and negativ (phi-) flow
        # Firstly: calculate sums of rows
        sum = [0] * (self.nalt-1)*self.nalt
        for i in range((self.nalt-1)*self.nalt):
            for j in range(self.ncrit):
                sum[i] += self.eval_matrix[i][j]

        aggr_matr = []
        for i in range(self.nalt):
            vec = []
            for j in range(self.nalt-1):
                temp = sum.pop(0)
                if i == j:
                    vec.append(0.0)
                    vec.append(temp)
                else:
                    vec.append(temp)
            if i == 0:
                aggr_matr = copy.deepcopy(vec)
            elif len(vec) < self.nalt:
                vec.append(0.0)
                aggr_matr = np.vstack((aggr_matr, vec))
            else:
                aggr_matr = np.vstack((aggr_matr, vec))

        # Flows
        phi_plus = [0] * self.nalt
        phi_minus = [0] * self.nalt
        for i in range(self.nalt):
            for j in range(self.nalt):
                phi_minus[i] += aggr_matr[j][i]
                phi_plus[i] += aggr_matr[i][j]
            phi_plus[i] /= self.nalt-1
            phi_minus[i] /= self.nalt-1

        # Calculate phi
        for i in range(self.nalt):
            self.phi.append(phi_plus[i] - phi_minus[i])

    def ranking(self):
        R = sorted(range(len(self.phi)), reverse=True, key=lambda k: self.phi[k])
        for i in range(len(R)):
            R[i] += 1
        print("Ranking for PROMETHEE II:")
        print_ranks(self.alternatives, R)
        return R

def read_file(filename):
    if not os.path.exists(filename):
        print("Error: file doesn't exists!")
        exit(1)
    return pd.read_excel(filename, header=None)

def create_labels(ncharacters, char):
    tab = [None] * ncharacters
    for i in range(ncharacters):
        tab[i] = char + str(i + 1)
    return tab

def Main():
    file = read_file(sys.argv[1])
    crit_benef = file.iloc[0]
    crit_benef = crit_benef.to_numpy()

    perf = file.iloc[1:]
    perf = perf.to_numpy()
    print("Decision matrix:")
    print(perf)
    print()

    ncrit = perf.shape[1]  # Number of criteria
    nalt = perf.shape[0]  # Number of alternatives
    criteria = create_labels(ncrit, 'C')
    altern = create_labels(nalt, 'A')

    weights, perf2 = Entropy_weights(perf, criteria, altern)
    top = TOPSIS(criteria, altern, weights, perf2, crit_benef)
    top.weightening()
    top.PIS_NIS()
    top.Euclidean_distance()
    top.Performance_score_and_ranking()
    vik = VIKOR(criteria, altern, weights, perf, crit_benef)
    vik.Best_worst()
    vik.Weightening()
    vik.SQR_and_ranking()
    pro = PROMETHEE(criteria, altern, weights, perf, crit_benef)
    pro.start()

if __name__ == '__main__':
    Main()

