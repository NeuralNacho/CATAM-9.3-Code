from mimetypes import init
from random_sequence import random_sequence
from q8_vgap import q8_vgap
import time
import math
import numpy as np


class vgap_estimator:
    def __init__(self, u, p, n, no_estimates, max_runtime):
        self.u = u
        self.p = p
        self.n = n
        self.no_estimates = no_estimates
        self.max_runtime = max_runtime
        # this is the max time taken to get an estimate with
        # this object if estimate no. takes too long

    
    def generate_estimate(self):
        U_n = random_sequence(self.p, self.n).get_sequence()
        V_n = random_sequence(self.p, self.n).get_sequence()
        test = q8_vgap(U_n, V_n, self.u)
        score = test.get_score()
    
        estimate = score / self.n
        return estimate

    
    def get_results(self):
        # Finds error of the estimate
        # runtime in seconds
        estimate_list = []
        end_time = time.time() + self.max_runtime
        while len(estimate_list) < self.no_estimates and \
                 time.time() < end_time:
            estimate = self.generate_estimate()
            estimate_list.append(estimate)
        
        estimate_mean = sum(estimate_list) / \
                        len(estimate_list)
        std_dev = np.std(estimate_list)
        estimate_error = std_dev / \
                        math.sqrt(len(estimate_list))
        # estimate_error is std deviation of sample mean
        # given the number of estimates in the sample
        print('No tests in estimate list = ', 
            len(estimate_list))

        return estimate_mean, std_dev, estimate_error


    def final_estimate(self):
        initial_time = time.time()
        result = self.get_results()
    # Considering distrubution of the sample mean (from sum
    # of normal distributions) can get it so that sample 
    # mean has standard deviation of 0.005/3 so there's a 
    # 99.7% chance of mean bwing within 0.005
    # Only worthwhile if can do a decent number of 
    # calculations in the max_runtime
        if time.time() < initial_time + 30:
            print('Additional time used')
            # i.e. less than 30s passed
            multiplier = ( 3 * result[2] / 0.005)**2
            self.no_estimates *= multiplier
            result = self.get_results()

        print('E(v_gap)/n estimate:       ', 
                                    result[0])
        print('sample standard deviation: ', 
                                    result[1])
        print('estimate error:            ', 
                                    result[2])  


if __name__ == '__main__':
    # For first part of Question 8

    n = 100
    max_runtime = 60
    no_estimates = 15
    # 15 tests will give good idea of error of standard  
    # deviation (for reasonably large n otherwise increase). 
    # If runtime too high then will use time instead

    estimator = vgap_estimator(-3, 1/2, n, no_estimates,
                                            max_runtime)
    estimator.final_estimate()
    
