import pandas as pd
import numpy as np
from glob import glob

def Net_Loading(inflows_path, outflows_path):
    # inflows_path = 'Inflows'
    g_inflow_path = inflows_path + '/*.csv'
    g_outflow_path = outflows_path + '/*.csv'
    
    inflows_names = glob(g_inflow_path)
    outflows_names = glob(g_outflow_path)
    
    inflows = [i for i in range(len(inflows_names))]
    outflows = [i for i in range(len(outflows_names))]
    
    for i in range(len(inflows_names)):
        inflows[i] = pd.read_csv(inflows_names[i], encoding='utf-8', index_col=0, parse_dates = True)
        
    for j in range(len(outflows_names)):
        outflows[j] = pd.read_csv(outflows_names[j], encoding = 'utf-8', index_col=0, parse_dates = True)

    def cal_loading(WQ, inflows, outflows): #input the parameter name,'TP','TKN','chla'
        W_in = 0
        
        for inflow in inflows:
            W_in = inflow['Flow'] * inflow[WQ] + W_in
        W_out = 0
        
        for outflow in outflows:
            W_out = outflow['Flow'] * outflow[WQ]
        
        W = W_in - W_out
        return W

    W_tkn = cal_loading('TKN', inflows, outflows)
    W_tp = cal_loading('TP', inflows, outflows)
    W_chl = cal_loading('chla', inflows, outflows)
    
    return W_tkn, W_tp, W_chl