from scipy.interpolate import make_interp_spline
import numpy as np
def suav_dados(x,y,n):
    X_Y_spline = make_interp_spline(x,y)
    X_ = np.linspace(x.min(),x.max(),n)
    Y_ = X_Y_spline(X_)
    return(X_,Y_)