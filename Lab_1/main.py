#!/usr/bin/env python
# coding: utf-8

# In[27]:


import matplotlib.pyplot as plt
import numpy as np

def my_plotter(ax, data1, data2, param_dict):
    out = ax.plot(data1, data2, **param_dict)
    return out

#input points of triangle
a = np.array([1, 1]) 
b = np.array([1, 4])
c = np.array([4, 4])

#getting figure
figure = np.array([a, b, c])

#converting figure into axis
x = np.array([figure[0][0], figure[1][0], figure[2][0], figure[0][0]])
y = np.array([figure[0][1], figure[1][1], figure[2][1], figure[0][1]])

#plotting
fig, ax = plt.subplots()
my_plotter(ax, x, y, {'marker' : 'o'})

#transformation matrix
T = np.array([[1, 0], [0, 1]])
T = T * np.array([-1, -1])

#transforming
figure = figure @ T

#converting figure into axis
x = np.array([figure[0][0], figure[1][0], figure[2][0], figure[0][0]])
y = np.array([figure[0][1], figure[1][1], figure[2][1], figure[0][1]])

my_plotter(ax, x, y, {'marker' : 'o'})






