import numpy as np
from scipy.stats import rv_discrete, norm, cauchy, gamma, chi, betaprime, pareto, lognorm, weibull_min, fatiguelife, arcsine, truncnorm
import matplotlib.pyplot as plt
from turtle import color
import scipy.stats as stats
import scipy.special
import scipy.integrate as integrate
import math as m
import shapely.geometry
from shapely.geometry import Polygon, Point
import random
import pandas as pd
import copy
from numpy import inf
import sys
from scipy import interpolate
from tkinter import *
import tkinter as tk
import matplotlib as mpl
mpl.rc('font', **{'family': 'serif', 'sans-serif': ['Computer Modern Sans serif']})
mpl.rc('text', usetex=True)

def isomean(y,w): 
    n = len(y) #maximal number of slopes, n+1 points
    k = np.zeros(len(y))
    gew = np.zeros(len(y)) #distance between points of accepted slopes
    ghat = np.zeros(len(y)) #accepted slopes
    c=0 #counter of accepted slopes 
    gew[c] = w[0] #we accept the first step on x axis by default
    ghat[c] = y[0] #we accept the first slope by default  

    for j in range(1,n):
        c = c+1
        k[c] = j
        gew[c] = w[j]
        ghat[c] = y[j]
        
        while (ghat[c-1] >= ghat[c]):
    
            neu = gew[c]+gew[c-1]
            ghat[c-1] = ghat[c-1]+(gew[c]/neu)*(ghat[c]-ghat[c-1])
            gew[c-1] = neu
            c = c-1

            if (c==0):
                #print("reached 0") 
                break
    
    while n >= 1:
        for j in range(int(k[c]),n):
            ghat[j] = ghat[c]
    
        n = int(k[c])
        c = c-1

    return ghat




def gcmlcm(x,y,type,max_xs):

    if all(x[i] <= x[i+1] for i in range(len(x) - 1)) == False:
        print("The x values must be arranged in sorted order!")
        return 0
    if len(x) != len(set(x)) == False:
        print("No duplicated x values allowed!")
        return 0
    
    dx = np.diff(x)
    dy = np.diff(y)

    rawslope = dy/dx

    rawslope = np.nan_to_num(rawslope, neginf=sys.float_info.min) 
    rawslope = np.nan_to_num(rawslope, posinf=sys.float_info.max) 

    if type == "gcm":
        slope = isomean(rawslope, dx)
    if type == "lcm":
        slope = -isomean(-rawslope, dx)


    slope_knots,keep = np.unique(slope, return_index=True)
    slope_knots = np.sort(slope_knots)[::-1]
    keep = np.sort(keep)
    x_knots = np.append(x[keep],x[-1])
    dx_knots = np.diff(x_knots)
    
    y_knots = y[0]+np.cumsum(dx_knots*slope_knots)

    y_knots = np.append(y[0],y_knots)

    y_knots = np.append(y_knots,y[-1])
    x_knots = np.append(x_knots,max_xs)

    return x_knots, y_knots,slope_knots


def U_n(x, Z):
    Z_minus_x_plus = np.where(Z-x > 0, Z-x, 0)
    res = np.array([2*(np.sqrt(Z[i]) - np.sqrt(Z_minus_x_plus[i]))  for i in range(len(Z))])
    return np.mean(res)

def estimator(max_xs,Z):
    xs = np.arange(0,max_xs, 0.01)

    U = np.array([U_n(xs[i],Z) for i in range(len(xs))])
    U_n_at_Z = np.array([U_n(Z[i],Z) for i in range(len(Z))])

    support_lcm, lcm, slopes = gcmlcm(np.sort(np.append(0,Z)),np.sort(np.append(0,U_n_at_Z)),"lcm", max_xs)

    figure, axis = plt.subplots(2, figsize=(6,8))
    axis[0].plot(xs, U, color = "green", label = r"$U_n(x)$")
    axis[0].scatter(np.sort(Z), np.sort(U_n_at_Z), s=10)
    axis[0].plot(support_lcm, lcm, color = "blue", label = r"least concave majorant $U_n(x)$")
    axis[0].set_xlabel("x", fontsize = 12)
    axis[0].legend(fontsize= 14)


    dx_U = np.diff(support_lcm)
    dy_U = np.diff(lcm)

    rhs_dU = dy_U/dx_U
    norm_rhs_dU = rhs_dU/rhs_dU[0]

    estimator_F = 1-norm_rhs_dU
    axis[1].step(support_lcm[1:],estimator_F,where = "post", label = r"Isotonic estimator of $F$")
    axis[1].hist(Z, bins=50, density=True, alpha=0.6, label=r"Sampled observations from $g$")
    axis[1].set_xlabel("x", fontsize = 12)
    axis[1].legend(loc = "lower right", fontsize=16)
    #plt.savefig('estimator.svg', format='svg', dpi=1200)
    plt.show()

    return estimator_F