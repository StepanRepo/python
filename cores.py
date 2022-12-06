#! /bin/python3

from multiprocessing import Pool
import time
import matplotlib.pyplot as plt
import numpy as np



def f(x):
    return x

mean_len = 10
max_cores = 10

times_mean = np.zeros(max_cores)

for _ in range(mean_len):
    times = np.empty(max_cores)

    for cores in range(1, max_cores + 1):
        start_time = time.time()

        with Pool(cores) as p:
            p.map(f, (range(1_000)))

        finish_time = time.time()

        times[cores-1] = finish_time - start_time

    times_mean += times

print(f"number of cores: {np.argmin(times_mean) + 1}")

plt.plot(range(1, max_cores+1), times_mean)
plt.show()
