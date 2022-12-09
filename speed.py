#! /bin/python

import numpy as np
import time
import matplotlib.pyplot as plt
from statistics import fmean
from scipy.interpolate import make_interp_spline, BSpline


import random

def smooth(x, y, err, samples = 300):
    x = np.array(x)
    y = np.array(y)
    err = np.array(err)

    xnew = np.linspace(x.min(), x.max(), samples)

    spl = make_interp_spline(x, y, k=3)
    spl_err = make_interp_spline(x, err, k=3)

    ynew = spl(xnew)
    err_new = spl_err(xnew)

    return xnew, ynew, err_new

def plot(x, y, err, label = ""):
    plt.fill_between(x, y+err, y-err, alpha = .3)
    plt.plot(x, y, label = label)


mean_times = 100
ns = [i*10 for i in range(1,5)]

py_times_1 = []
py_errors_1 = []

np_times_1 = []
np_errors_1 = []


for n in ns:
    # define section
    py_list_1 = []
    py_list_2 = []
    py_list_res = []

    np_list_1 = np.empty(n)
    np_list_2 = np.empty(n)
    np_list_res = np.empty(n)

    for i in range(n):
        py_list_1.append(random.random())
        py_list_2.append(random.random())

        np_list_1[i] = random.random()
        np_list_2[i] = random.random()

    # test python section
    py_time = []

    for _ in range(mean_times):
        start = time.time()

        for i in range(n):
            py_list_res.append( py_list_1[i] * py_list_2[i] )

        finish = time.time()

        py_time.append(finish - start)

    py_times_1.append(np.mean(py_time))
    py_errors_1.append(np.std(py_time))

    np_time = []

    for _ in range(mean_times):
        start = time.time()

        np_list_res = np_list_1 * np_list_2

        finish = time.time()

        np_time.append(finish - start)

    np_times_1.append(np.mean(np_time))
    np_errors_1.append(np.std(np_time))



py_times_2 = []
py_errors_2 = []

np_times_2 = []
np_errors_2 = []


for n in ns:
    # define section
    py_list_1 = [[random.random() for _ in range(n)] for _ in range(n)]
    py_list_2 = [[random.random() for _ in range(n)] for _ in range(n)]
    py_list_res = [[]]

    np_list_1 = np.empty((n, n))
    np_list_2 = np.empty((n, n))
    np_list_res = np.empty((n, n))

    for i in range(n):
        for k in range(n):
            np_list_1[i][k] = random.random()
            np_list_2[i][k] = random.random()

    # test python section
    py_time = []

    for _ in range(mean_times):
        start = time.time()

        for i in range(n):
            py_list_res.append([])

            for k in range(n):
                py_list_res[i].append( py_list_1[i][k] * py_list_2[i][k] )

        finish = time.time()

        py_time.append(finish - start)

    py_times_2.append(np.mean(py_time))
    py_errors_2.append(np.std(py_time))

    np_time = []

    for _ in range(mean_times):
        start = time.time()

        np_list_res = np_list_1 * np_list_2

        finish = time.time()

        np_time.append(finish - start)

    np_times_2.append(np.mean(np_time))
    np_errors_2.append(np.std(np_time))


py_times_3 = []
py_errors_3 = []

np_times_3 = []
np_errors_3 = []


for n in ns:
    # define section
    py_list_1 = [[[random.random() for _ in range(n)] for _ in range(n)] for _ in range(n)]
    py_list_2 = [[[random.random() for _ in range(n)] for _ in range(n)] for _ in range(n)]
    py_list_res = [[[]]]

    np_list_1 = np.empty((n, n, n))
    np_list_2 = np.empty((n, n, n))
    np_list_res = np.empty((n, n, n))

    for i in range(n):
        for k in range(n):
            for j in range(n):
                np_list_1[i][k][j] = random.random()
                np_list_2[i][k][j] = random.random()

    # test python section
    py_time = []

    for _ in range(mean_times):
        start = time.time()

        for i in range(n):
            py_list_res.append([])

            for k in range(n):
                py_list_res[i].append([])

                for j in range(n):
                    py_list_res[i][k].append( py_list_1[i][k][j] * py_list_2[i][k][j] )

        finish = time.time()

        py_time.append(finish - start)

    py_times_3.append(np.mean(py_time))
    py_errors_3.append(np.std(py_time))

    np_time = []

    for _ in range(mean_times):
        start = time.time()

        np_list_res = np_list_1 * np_list_2

        finish = time.time()

        np_time.append(finish - start)

    np_times_3.append(np.mean(np_time))
    np_errors_3.append(np.std(np_time))



plt.subplot(1, 2, 1)

x, y, err = smooth(ns, py_times_1, py_errors_1)
plot(x, y, err, "dim = 1")

x, y, err = smooth(ns, py_times_2, py_errors_2)
plot(x, y, err, "dim = 2")

x, y, err = smooth(ns, py_times_3, py_errors_3)
plot(x, y, err, "dim = 3")

plt.yscale('log')
plt.xlabel("length of array")
plt.ylabel("seconds")
plt.legend()
plt.grid()



plt.subplot(1, 2, 2)

x, y, err = smooth(ns, np_times_1, np_errors_1)
plot(x, y, err, "dim = 1")

x, y, err = smooth(ns, np_times_2, np_errors_2)
plot(x, y, err, "dim = 2")

x, y, err = smooth(ns, np_times_3, np_errors_3)
plot(x, y, err, "dim = 3")

plt.yscale('log')
plt.xlabel("length of array")
plt.ylabel("seconds")
plt.legend()
plt.grid()


plt.show()
