import matplotlib.pyplot as plt
import numpy as np
from q8_vgap import q8_vgap
from vgap_estimator import vgap_estimator
from random_sequence import random_sequence


class limit_estimator:
    def __init__(self, u, p):
        self.u = u
        self.p = p
        self.x_list = []
        self.y_list = []


    def generate_estimate(self, n):
        U_n = random_sequence(self.p, self.n).get_sequence()
        V_n = random_sequence(self.p, self.n).get_sequence()
        test = q8_vgap(U_n, V_n, self.u)
        score = test.get_score()

        estimate = score / n
        return estimate


    def generate_graph(self):
        n = 100
        self.x_list.append(n)
        self.y_list.append(self.generate_estimate(n))
        old_estimate = self.y_list[0]
        new_estimate = old_estimate + 3
        while n < 10000:
            n = int(n*1.25)
            print(n)
            self.x_list.append(n)
            self.y_list.append(self.generate_estimate(n))
            old_estimate = new_estimate
            new_estimate = self.y_list[-1]


    def plot(self):
        self.generate_graph()
        plt.rc('font', size = 32)
        plt.figure(1)
        plt.grid(linestyle = '--', linewidth = 0.5)
        plt.plot(self.x_list, self.y_list, color = 'C0')
        plt.xlabel('$n$')
        plt.ylabel('$Estimate$') 

        plt.show()


    def estimate_limit(self):
        max_runtime = 300  # 5 minutes
        no_estimates = 100  # will never reach this number

        calculator = vgap_estimator(-3, 1/2, 6000, 
                            no_estimates, max_runtime)

        result = calculator.get_results()

        return result[0], result[2]



if __name__ == '__main__':
    estimator = limit_estimator(-3, 1/2)
    # estimator.plot()
    results = estimator.estimate_limit()
    print('Estimate mean: ', results[0])
    print('Estimate std:  ', results[1])