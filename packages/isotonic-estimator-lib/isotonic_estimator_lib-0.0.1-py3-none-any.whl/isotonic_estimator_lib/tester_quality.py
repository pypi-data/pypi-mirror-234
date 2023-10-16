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


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        
        self.l0=Label(master,text="Here you can test the isotonic estimator.")
        self.l0.pack()
        self.l3=Label(master,text="Type below the chosen hidden distrbution to test. Choose between:")
        self.l3.pack()
        self.l3=Label(master,text="gamma, chi, betaprime, pareto, lognormal, truncnorm, arcsine, fatiguelife, weibull.")
        self.l3.pack()
        self.l4=Label(master,text="____________________________________________________________________________________________")
        self.l4.pack() 
        self.l=Label(master,text="Insert name hidden distribution F:")
        self.l.pack()
        self.e=Entry(master)
        self.e.pack()
        self.l1=Label(master,text="Number observed samples (suggested btw 10-1000):")
        self.l1.pack()
        self.e1=Entry(master)
        self.e1.pack()
        self.b=Button(master,text='Ok',command=self.cleanup)
        self.b.pack()

        
    def cleanup(self):
        global distribution
        global N_samples
        distribution = self.e.get()
        N_samples = self.e1.get()
        self.master.destroy()


def find_nearest(array, value):
    idx = (np.abs(array - value)).argmin()
    return idx

def biased_F(F,xs):
    biased_F_res = np.zeros(len(F))

    for n in range(1,len(F)):
        if xs[n] <= 0.01:
            biased_F_res[n] = 0
        else:
            biased_F_res[n] = ((np.sqrt(xs[n-1]) + np.sqrt(xs[n]))/2)*(F[n]-F[n-1]) + biased_F_res[n-1]

    return biased_F_res/biased_F_res[-1]

def g(z_vec,F,xs):
    Fb = biased_F(F,xs)
    res = np.zeros(len(z_vec))
    for j in range(len(z_vec)):
        z=z_vec[j]
        idx = find_nearest(xs,z)
        res[j] = 0
        
        for n in range(idx+2,len(xs)):
            if xs[n] <= 0.02:
                res[j] += 0
            else:
                res[j] += ((1/(4*np.sqrt(xs[n-1]**2 - xs[n-1]*z))) + (1/(4*np.sqrt(xs[n]**2 - xs[n]*z))))*(Fb[n]-Fb[n-1])
        
    return res


def batch_sample(num_samples, xmin, xmax, ymax, ymin,xs,F, batch=1000):
    #xs = np.arange(0,5, 0.01)
    #F = gamma.cdf(xs, a = 2, loc = 0, scale = 0.5)
    samples = []
    while len(samples) < num_samples:
        x = np.random.uniform(low=xmin, high=xmax, size=batch)
        y = np.random.uniform(low=ymin, high=ymax, size=batch)
        samples += x[y < g(x,F,xs)].tolist()
    return samples[:num_samples]

# this function implements the PAVA algorithm to
# find greatest convex minorant (gcm) or  
# least concave majorant (lcm)


 # input:  y       measured values in a regression setting
 #         w       weights
 # output: ghat    vector containing estimated (isotonic) values
 

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



def unbiased_F(F,xs):
    unbiased_F_res = np.zeros(len(F))

    for n in range(1,len(F)):
        if xs[n] <= 0.02:
            unbiased_F_res[n] = 0
        else:
            unbiased_F_res[n] = ((1/np.sqrt(xs[n-1]) + 1/np.sqrt(xs[n]))/2)*(F[n]-F[n-1]) + unbiased_F_res[n-1]

    return unbiased_F_res/unbiased_F_res[-1]

def U_n(x, Z):
    Z_minus_x_plus = np.where(Z-x > 0, Z-x, 0)
    res = np.array([2*(np.sqrt(Z[i]) - np.sqrt(Z_minus_x_plus[i]))  for i in range(len(Z))])
    return np.mean(res)


def main(N_observations,max_xs,theta_true,k_true, distribution):
    
    figure, axis = plt.subplots(2, 2, figsize=(11,9)) 

    xs = np.arange(0,max_xs, 0.01)
    if distribution == "gamma":
        F = gamma.cdf(xs, a = k_true, loc = 0, scale = theta_true)
        Fb = biased_F(F,xs)
        axis[0,0].plot(xs, F, color = "orange", label = r"cdf $F$ debiased hidden $X \sim$ " + "Ga({0},{1})".format(k_true,theta_true))
        axis[0,0].plot(xs, Fb, color = "red", label = r"cdf $F^{(b)}$ biased hidden $X^b$")
        axis[0,0].set_xlabel("x", fontsize = 12)
        axis[0,0].legend(loc = "lower right", fontsize=13)
    elif distribution == "chi":
        F = chi.cdf(xs, theta_true)
        Fb = biased_F(F,xs)
        axis[0,0].plot(xs, F, color = "orange", label = r"cdf $F$ debiased hidden $X \sim$ " + "Chi({0})".format(theta_true))
        axis[0,0].plot(xs, Fb, color = "red", label = r"cdf $F^{(b)}$ biased hidden $X^b$")
        axis[0,0].set_xlabel("x", fontsize = 12)
        axis[0,0].legend(loc = "lower right", fontsize=8)
    elif distribution == "betaprime": 
        F = betaprime.cdf(xs, a = k_true, b = theta_true)
        Fb = biased_F(F,xs)
        axis[0,0].plot(xs, F, color = "orange", label = r"cdf $F$ debiased hidden $X \sim$ " + "Be_prime({0},{1})".format(k_true,theta_true))
        axis[0,0].plot(xs, Fb, color = "red", label = r"cdf $F^{(b)}$ biased hidden $X^b$")
        axis[0,0].set_xlabel("x", fontsize = 12)
        axis[0,0].legend(loc = "lower right", fontsize=8)
    elif distribution == "pareto":
        F = pareto.cdf(xs, b = theta_true)
        Fb = biased_F(F,xs)
        axis[0,0].plot(xs, F, color = "orange", label = r"cdf $F$ debiased hidden $X \sim$ " + "Pareto({0})".format(theta_true))
        axis[0,0].plot(xs, Fb, color = "red", label = r"cdf $F^{(b)}$ biased hidden $X^b$")
        axis[0,0].set_xlabel("x", fontsize = 12)
        axis[0,0].legend(loc = "lower right", fontsize=8)
    elif distribution == "lognormal":
        F = lognorm.cdf(xs, s = theta_true)
        Fb = biased_F(F,xs)
        axis[0,0].plot(xs, F, color = "orange", label = r"cdf $F$ debiased hidden $X \sim$ " + "Lognorm({0})".format(theta_true))
        axis[0,0].plot(xs, Fb, color = "red", label = r"cdf $F^{(b)}$ biased hidden $X^b$")
        axis[0,0].set_xlabel("x", fontsize = 12)
        axis[0,0].legend(loc = "lower right", fontsize=8)
    elif distribution == "weibull":
        F = weibull_min.cdf(xs, c = theta_true)
        Fb = biased_F(F,xs)
        axis[0,0].plot(xs, F, color = "orange", label = r"cdf $F$ debiased hidden $X \sim$ " + "Weibull({0})".format(theta_true))
        axis[0,0].plot(xs, Fb, color = "red", label = r"cdf $F^{(b)}$ biased hidden $X^b$")
        axis[0,0].set_xlabel("x", fontsize = 12)
        axis[0,0].legend(loc = "lower right", fontsize=8)
    elif distribution == "fatiguelife":
        F = fatiguelife.cdf(xs, c = theta_true)
        Fb = biased_F(F,xs)
        axis[0,0].plot(xs, F, color = "orange", label = r"cdf $F$ debiased hidden $X \sim$ " + "Fatiguelife({0})".format(theta_true))
        axis[0,0].plot(xs, Fb, color = "red", label = r"cdf $F^{(b)}$ biased hidden $X^b$")
        axis[0,0].set_xlabel("x", fontsize = 12)
        axis[0,0].legend(loc = "lower right", fontsize=8)
    elif distribution == "arcsine":
        F = arcsine.cdf(xs)
        Fb = biased_F(F,xs)
        axis[0,0].plot(xs, F, color = "orange", label = r"cdf $F$ debiased hidden $X \sim$ " + "Arcsine")
        axis[0,0].plot(xs, Fb, color = "red", label = r"cdf $F^{(b)}$ biased hidden $X^b$")
        axis[0,0].set_xlabel("x", fontsize = 12)
        axis[0,0].legend(loc = "lower right", fontsize=8)
    elif distribution == "truncnorm":
        F = truncnorm.cdf(xs, a = k_true, b = theta_true)
        Fb = biased_F(F,xs)
        axis[0,0].plot(xs, F, color = "orange", label = r"cdf $F$ debiased hidden $X \sim$ " + "Truncnorm({0},{1})".format(k_true,theta_true))
        axis[0,0].plot(xs, Fb, color = "red", label = r"cdf $F^{(b)}$ biased hidden $X^b$")
        axis[0,0].set_xlabel("x", fontsize = 12)
        axis[0,0].legend(loc = "lower right", fontsize=8)

    poly = Polygon([(0.01, 0), (max_xs, 0),(1, max_xs),(0.01, 1)]) 
    min_x, min_y, max_x, max_y = poly.bounds

    samps = batch_sample(N_observations, min_x,max_x,max_y,min_y,xs,F)
    
    xs_g = np.linspace(min_x, max_x, 1000)
    ys = g(xs_g,F,xs)
    
    axis[0,1].plot(xs_g, ys, label=r"density $g(z)$")
    axis[0,1].hist(samps, bins=50, density=True, alpha=0.6, label=r"Sampled observations from $g$")
    axis[0,1].set_xlabel("z", fontsize = 12) 
    #axis[0,1].set_ylabel("g(z)", fontsize = 14)
    axis[0,1].legend(fontsize= 16)

    Z = np.asarray(samps)
    xs = np.arange(0,max_xs, 0.01)

    U = np.array([U_n(xs[i],Z) for i in range(len(xs))])
    U_n_at_Z = np.array([U_n(Z[i],Z) for i in range(len(Z))])

    support_lcm, lcm, slopes = gcmlcm(np.sort(np.append(0,Z)),np.sort(np.append(0,U_n_at_Z)),"lcm", max_xs)


    axis[1,0].plot(xs, U, color = "green", label = r"$U_n(x)$")
    axis[1,0].scatter(np.sort(Z), np.sort(U_n_at_Z), s=10)
    axis[1,0].plot(support_lcm, lcm, color = "blue", label = r"least concave majorant $U_n(x)$")
    axis[1,0].set_xlabel("x", fontsize = 12)
    axis[1,0].legend(fontsize= 14)


    dx_U = np.diff(support_lcm)
    dy_U = np.diff(lcm)

    rhs_dU = dy_U/dx_U
    norm_rhs_dU = rhs_dU/rhs_dU[0]

    estimator_F = 1-norm_rhs_dU

    
    if distribution == "gamma":        
        axis[1,1].step(support_lcm[1:],estimator_F,where = "post", label = r"Isotonic estimator of $F$")
        axis[1,1].plot(xs, F, color = "red", label = r"cdf $F$, $X \sim$ " + "Ga({0},{1})".format(k_true,theta_true))
        axis[1,1].set_xlabel("x", fontsize = 12)
        axis[1,1].legend(loc = "lower right", fontsize=16)
        plt.savefig('estimator.svg', format='svg', dpi=1200)
        plt.show()
    elif distribution == "chi":
        axis[1,1].step(support_lcm[1:],estimator_F,where = "post", label = r"Isotonic estimator of $F$")
        axis[1,1].plot(xs, F, color = "red", label = r"cdf $F$ hidden $X \sim$ " + "Chi({0})".format(theta_true))
        axis[1,1].set_xlabel("x", fontsize = 12)
        axis[1,1].legend(loc = "lower right", fontsize=8)
        plt.savefig('estimator.svg', format='svg', dpi=1200)
        plt.show()
    elif distribution == "betaprime": 
        axis[1,1].step(support_lcm[1:],estimator_F,where = "post", label = r"Isotonic estimator of $F$")
        axis[1,1].plot(xs, F, color = "red", label = r"cdf $F$ hidden $X \sim$ " + "Be_prime({0},{1})".format(k_true,theta_true))
        axis[1,1].set_xlabel("x", fontsize = 12)
        axis[1,1].legend(loc = "lower right", fontsize=8)
        plt.savefig('estimator.svg', format='svg', dpi=1200)
        plt.show()
    elif distribution == "pareto":
        axis[1,1].step(support_lcm[1:],estimator_F,where = "post", label = r"Isotonic estimator of $F$")
        axis[1,1].plot(xs, F, color = "red", label = r"cdf $F$ hidden $X \sim$ " + "Pareto({0})".format(theta_true))
        axis[1,1].set_xlabel("x", fontsize = 12)
        axis[1,1].legend(loc = "lower right", fontsize=8)
        plt.savefig('estimator.svg', format='svg', dpi=1200)
        plt.show()
    elif distribution == "lognormal":
        axis[1,1].step(support_lcm[1:],estimator_F,where = "post", label = r"Isotonic estimator of $F$")
        axis[1,1].plot(xs, F, color = "red", label = r"cdf $F$ hidden $X \sim$ " + "Lognorm({0})".format(theta_true))
        axis[1,1].set_xlabel("x", fontsize = 12)
        axis[1,1].legend(loc = "lower right", fontsize=8)
        plt.savefig('estimator.svg', format='svg', dpi=1200)
        plt.show()
    elif distribution == "weibull":
        axis[1,1].step(support_lcm[1:],estimator_F,where = "post", label = r"Isotonic estimator of $F$")
        axis[1,1].plot(xs, F, color = "red", label = r"cdf $F$ hidden $X \sim$ " + "Weibull({0})".format(theta_true))
        axis[1,1].set_xlabel("x", fontsize = 12)
        axis[1,1].legend(loc = "lower right", fontsize=8)
        plt.savefig('estimator.svg', format='svg', dpi=1200)
        plt.show()
    elif distribution == "fatiguelife":
        axis[1,1].step(support_lcm[1:],estimator_F,where = "post", label = r"Isotonic estimator of $F$")
        axis[1,1].plot(xs, F, color = "red", label = r"cdf $F$ hidden $X \sim$ " + "Fatiguelife({0})".format(theta_true))
        axis[1,1].set_xlabel("x", fontsize = 12)
        axis[1,1].legend(loc = "lower right", fontsize=8)
        plt.savefig('estimator.svg', format='svg', dpi=1200)
        plt.show()
    elif distribution == "arcsine":
        axis[1,1].step(support_lcm[1:],estimator_F,where = "post", label = r"Isotonic estimator of $F$")
        axis[1,1].plot(xs, F, color = "red", label = r"cdf $F$ hidden $X \sim$ " + "Arcsine")
        axis[1,1].set_xlabel("x", fontsize = 12)
        axis[1,1].legend(loc = "lower right", fontsize=8)
        plt.savefig('estimator.svg', format='svg', dpi=1200)
        plt.show()
    elif distribution == "truncnorm":
        axis[1,1].step(support_lcm[1:],estimator_F,where = "post", label = r"Isotonic estimator of $F$")
        axis[1,1].plot(xs, F, color = "red", label = r"cdf $F$ hidden $X \sim$ " + "Truncnorm({0},{1})".format(k_true,theta_true))
        axis[1,1].set_xlabel("x", fontsize = 12)
        axis[1,1].legend(loc = "lower right", fontsize=8)
        plt.savefig('estimator.svg', format='svg', dpi=1200)
        plt.show()
    
    
def tester():
    max_xs = 5 #upper bound grid x's for the plots of the cdf's

    #parameters of the true biased hidden distribution, e.g. gamma distribution Ga(k_true,theta_true) generating the observations
    k_true = 2
    theta_true = 0.5
    #2, 0.5
    #worst: lognormal, betaprime, truncated normal (not all parameters work mind upper lower bounds)

    root = tk.Tk()
    myapp = App(root)
    res = myapp.mainloop()
    
    distribution_chosen = distribution
    N_observations = int(N_samples) #size sample Z_1,...,Z_N

    main(N_observations, max_xs, theta_true, k_true, distribution)


    



