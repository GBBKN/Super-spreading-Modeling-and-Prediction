import networkx as nx
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
import pandas as pd

from tqdm import trange
import numpy as np

import warnings
warnings.filterwarnings('ignore')

#Propagation method, add/change node status
class family(object):
    def __init__(self, x=0, y=0, state=0, label=0):
        super().__init__()
        self.x = x
        self.y = y
        self.state = state
        self.relations = set()
        self.label = label
        self.seal = False

    def relate(self, fam):
        """
        relate 2 families
        """
        self.relations.add(fam)
        fam.relations.add(self)

    def unrelate(self, fam):
        self.relations.discard(fam)
        fam.relations.discard(self)

    def isRelate(self, fam):
        if fam in self.relations:
            return True
        return False

    def infect(self):
        while True:
            latent = round(np.random.normal(7, 7))
            # latent ++ each day, if latent == 15, ill, state = -1
            if 1 <= latent <= 14:
                return latent


"""
S -> E -> I -> R
beta, 1-14, mu
"""


class Paras(object):
    def __init__(self):
        super().__init__()
        # infection rate when actioning with latent family
        self.BETA = 0.9
        # how family are willing to act with another
        self.THETA = 0.1
        # therapy
        self.MU = 0.1
        # R to S
        self.ETA = 0.01


paras = Paras()


class Calculator(object):
    def __init__(self, fam_list):
        super().__init__()
        self.fam_list = fam_list

    def next_iter(self, iterations=5):
        # [[], [], []]
        total_states = []
        for it in range(iterations):
            new_state = list()
            # action and infect
            for i, f_1 in enumerate(self.fam_list):
                state = f_1.state
                for f_2 in f_1.relations:
                    # S to E
                    if not f_1.seal and f_1.state == 0 and f_2.state > 0 and not f_2.seal:
                        # beta * theta
                        if np.random.binomial(1, paras.BETA) * np.random.binomial(1, paras.THETA):
                            state = f_1.infect()
                            break
                        else:
                            state = 0
                # E to I
                if f_1.state > 0:
                    state = f_1.state + 1
                    if state == 15:
                        state = -1
                # I to R
                if f_1.state == -1:
                    # mu
                    if np.random.binomial(1, paras.MU):
                        state = -2
                    else:
                        state = f_1.state
                # R to S
                if f_1.state == -2:
                    # eta
                    if np.random.binomial(1, paras.ETA):
                        state = 0
                    else:
                        state = f_1.state
                new_state.append(state)

            for i, f in enumerate(self.fam_list):
                f.state = new_state[i]

            total_states.append(new_state)
        return total_states

    def cls(self):
        for f in self.fam_list:
            f.state = 0
            f.seal = False


def return_family_list(G):
    # generate fam_list
    # n=1000, m=5, seed=0
    # G_gen = nx.random_graphs.barabasi_albert_graph(n, m, seed)

    # using contact_network
    G_gen = G

    fam_list = list()
    adj = list(G_gen.edges())
    match_list = list(G_gen.nodes)
    for g in G_gen:
        fam = family(label=g)
        fam_list.append(fam)
    for g_1, g_2 in adj:
        f_1 = fam_list[match_list.index(g_1)]
        f_2 = fam_list[match_list.index(g_2)]
        f_1.relate(f_2)

    return fam_list


def experiment_1_THETA(fam_list, THETAs, INFECT_INIT=30, days=10, runs=30):
    cal = Calculator(fam_list)
    states_each_experiment = list()

    states_each_experiment = np.zeros((runs, THETAs.shape[0], days, len(fam_list)))
    for r in range(runs):
        for t in trange(len(THETAs)):
            theta = THETAs[t]
            # print("theta: " + str(theta))
            paras.THETA = theta
            cal.cls()
            infects = []
            while len(infects) < INFECT_INIT:
                i = np.random.randint(0, len(fam_list))
                infects.append(i)
            for i in infects:
                fam_list[i].state = 5
            # cal.next_iter(days) returns [day:[state, state, state]]
            each_experiment = np.array(cal.next_iter(days))
            # each_experiment = [sum(data!=0) for data in each_experiment]
            states_each_experiment[r, t] = states_each_experiment[r, t] + each_experiment
    return states_each_experiment


#sys_path???
sys_path = './'
edgelist = pd.read_csv(sys_path +"Edgelist.csv", header=None,dtype={0:int,1:int,2:float})
edgelist = edgelist.rename(columns={0: "node1", 1:"node2", 2:"weight"})

#degree_dist = pd.read_csv(sys_path +"Edge_dist.csv")

G = nx.from_pandas_edgelist(edgelist, 'node1', 'node2', ['weight'])

fam_list = return_family_list(G)

# experiment 1.0
days = 50
THETAs = np.asarray([0.0001, 0.0005, 0.001, 0.005, 0.01, 0.02, 0.03, 0.05, 0.1, 0.5])
ex_0_data = experiment_1_THETA(fam_list, days=days, THETAs=THETAs)

# experiment 1.0
# data
run_theta_day_state = np.where(ex_0_data==0, 0, 1)

# show results
theta_day = run_theta_day_state.mean(axis=0).mean(axis=2)

fig, axes = plt.subplots(figsize=(13, 5))
for t, theta in enumerate(THETAs):
    plt.plot(np.arange(0, days+1), [30/1000] + list(theta_day[t, :]), '*-')
plt.xlabel('days')
plt.ylabel('percentage of infected people')
plt.legend([r'$\theta=$' + str(theta) for theta in THETAs])
plt.savefig( sys_path + “exp1_result.png”)
plt.show()