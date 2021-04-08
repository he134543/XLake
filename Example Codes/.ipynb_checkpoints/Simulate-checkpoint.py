from __future__ import division
import pandas as pd
import numpy as np
from scipy.integrate import solve_ivp

def Predict_WQ(t_span, initial_values, method, t_eval, W, Tem_path, Light_path, V_path, Parapath):
    
    
    V = pd.read_csv(V_path, index_col=0, parse_dates = True)
    WatTem = pd.read_csv(Tem_path, index_col=0, parse_dates = True)
    Light = pd.read_csv(Light_path, index_col=0, parse_dates = True)
    Parameters = pd.read_csv(Parapath, index_col=0)
    W_tp, W_tkn, W_chla = W
    
    def conc_change(t, w, *args):
        # loading, temp and light, and model parameters are passed into the function
        W_tp, W_tkn, W_chla, T, Light, V, Parameters = args
        
        # initial value of each indicators
        N,P,Chl = w
        
        # read all the parameters
        umax,Topt,kl,ksn,ksp,dn,dp,upt_n_max,upt_p_max,Rmax,dchl = Parameters.loc['Value',:].astype('float')
        
        
        # The limitation of N and P
        Fnp = 2/(N/(ksn + N) + P/(ksp + P))
        Fn = N/(ksn+N)
        Fp = P/(ksp+P)
        
        
        # The limitation of Light and Temperature
        
        Fl = Light[int(t)]/(Light[int(t)] + kl)
        
        Ft = np.exp(-2.3/15 * np.abs(T[int(t)] - Topt))
        
        
        # Growth of algae
        u = umax * Fl * Fnp
        
        # Death rate of chl
        R = Rmax * Ft * Fnp
        
        # uptake
        upt_n = upt_n_max * Fn
        upt_p = upt_p_max * Fp
        
        # func of variation of N and P
        S_n = W_tkn[int(t)]/V[int(t)] - dn * N - upt_n * N
        S_p = W_tp[int(t)]/V[int(t)] - dp * P - upt_p * P
        S_chl = W_chla[int(t)]/V[int(t)] - R * Chl + u * Chl - dchl * Chl
        
        return S_n, S_p, S_chl
    
    result = solve_ivp(conc_change, t_span, initial_values,  method = method, t_eval = t_eval, args = (W_tp.values, W_tkn.values, W_chla.values, WatTem.values.flatten(), Light.values.flatten(), V.values.flatten(), Parameters))
    
    N,P,chl = result.y
    
    return N,P,chl