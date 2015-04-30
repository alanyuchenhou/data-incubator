#!/usr/bin/env python

import numpy as np

def roll(M):
    roll_sum = 0
    roll_count = 0
    samples = []
    while roll_sum < M:
        new_value = np.random.randint(1, high=7)
        samples.append(new_value)
        roll_sum += new_value
        roll_count += 1
    return roll_sum - M, roll_count

def calculate(m):
    experiments = [roll(m) for i in range(10000)]
    sums, counts = zip(*experiments)
    sum_samples = np.array(sums)
    count_samples = np.array(counts)
    results = [sum_samples.mean(), sum_samples.std(),
               count_samples.mean(), count_samples.std()]
    return results

if __name__ == '__main__':
    for m in [20, 10000]:
        print calculate(m)
