import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def cal_Nash(obs_path, predict_array):
    obs = pd.read_csv(obs_path, index_col=0, parse_dates = True)
    obs_chl = obs['chla'].iloc[:-1]
    